from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


@dataclasses.dataclass(frozen=True)
class Channel:
    channel_index: int
    dat_path: Path
    prm_path: Path
    clock_hz: float | None


def parse_clock_hz(prm_path: Path) -> float | None:
    try:
        txt = prm_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in txt:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3 and parts[1] == "ClockSpeed":
            try:
                return float(parts[2])
            except ValueError:
                return None
    return None


def discover_channels(root: Path) -> list[Channel]:
    dat_files = sorted(root.rglob("*.dat"))
    chans: list[Channel] = []
    for dat_path in dat_files:
        m = re.search(r"-(\d+)\.dat$", dat_path.name)
        if not m:
            continue
        idx = int(m.group(1))
        prm_path = dat_path.with_suffix(".prm")
        clock = parse_clock_hz(prm_path) if prm_path.exists() else None
        chans.append(Channel(channel_index=idx, dat_path=dat_path, prm_path=prm_path, clock_hz=clock))
    chans.sort(key=lambda c: c.channel_index)
    return chans


def load_downsampled_int16(dat_path: Path, *, stride: int, max_points: int) -> np.ndarray:
    data = np.fromfile(dat_path, dtype="<i2")
    if data.size == 0:
        return np.array([], dtype=np.float32)
    if stride > 1:
        data = data[::stride]
    if data.size > max_points:
        data = data[:max_points]
    x = data.astype(np.float32)
    x -= float(x.mean())
    std = float(x.std())
    if std > 0:
        x /= std
    return x


def load_downsampled_float32(dat_path: Path, *, stride: int, max_points: int) -> np.ndarray:
    data = np.fromfile(dat_path, dtype="<f4")
    if data.size == 0:
        return np.array([], dtype=np.float32)
    if stride > 1:
        data = data[::stride]
    if data.size > max_points:
        data = data[:max_points]
    x = data.astype(np.float32)
    x -= float(x.mean())
    std = float(x.std())
    if std > 0:
        x /= std
    return x


def load_waveform_auto(dat_path: Path, *, stride: int, max_points: int) -> np.ndarray:
    x = load_downsampled_int16(dat_path, stride=stride, max_points=max_points)
    if x.size == 0 or float(np.std(x)) == 0.0:
        xf = load_downsampled_float32(dat_path, stride=stride, max_points=max_points)
        if xf.size:
            return xf
    return x


@dataclasses.dataclass(frozen=True)
class EdgeMetrics:
    a: int
    b: int
    coh_avg: float
    ph_stab_avg: float
    ph_bias: float
    ph_mean: float  # circular mean angle in radians, [-pi, pi]
    score: float


def edge_metrics_matrix(
    X: np.ndarray,
    *,
    sample_rate_hz: float,
    window_size: int,
    step_size: int,
    band_hz: tuple[float, float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns per-pair aggregated metrics matrices:
      coh_avg[i,j], ph_stab_avg[i,j], ph_bias[i,j], ph_mean[i,j]
    """
    n_ch, n_t = X.shape
    f = np.fft.rfftfreq(window_size, d=1.0 / sample_rate_hz)
    fmin, fmax = band_hz
    band_mask = (f >= fmin) & (f <= fmax)
    if n_t < window_size or not np.any(band_mask):
        z = np.zeros((n_ch, n_ch), dtype=np.float32)
        return z, z, z, z

    hann = np.hanning(window_size).astype(np.float32)
    starts = list(range(0, n_t - window_size + 1, step_size))
    if not starts:
        z = np.zeros((n_ch, n_ch), dtype=np.float32)
        return z, z, z, z

    # Accumulators
    coh_sum = np.zeros((n_ch, n_ch), dtype=np.float64)
    stab_sum = np.zeros((n_ch, n_ch), dtype=np.float64)
    bias_sum = np.zeros((n_ch, n_ch), dtype=np.float64)
    mean_vec = np.zeros((n_ch, n_ch), dtype=np.complex128)
    counts = np.zeros((n_ch, n_ch), dtype=np.int32)

    for s in starts:
        seg = X[:, s : s + window_size] * hann[None, :]
        Y = np.fft.rfft(seg, axis=1)  # (n_ch, n_f)
        P = (np.abs(Y) ** 2).astype(np.float64)

        # Precompute band indices once
        band_idx = np.where(band_mask)[0]
        # Pairwise: O(n^2 * band) — OK for ~126 channels and small band
        for i in range(n_ch):
            Pxx = P[i]
            Yi = Y[i]
            for j in range(i + 1, n_ch):
                Pyy = P[j]
                denom = Pxx[band_idx] * Pyy[band_idx]
                valid = denom > 0
                if not np.any(valid):
                    continue
                idx = band_idx[valid]
                Pxy = Yi[idx] * np.conj(Y[j][idx])

                coh = (np.abs(Pxy) ** 2) / denom[valid]
                coh_m = float(np.mean(coh))

                phase = np.angle(Pxy)
                stab = float(np.abs(np.mean(np.exp(1j * phase))))
                bias = float(np.mean(np.sign(np.sin(phase))))
                mu = np.mean(np.exp(1j * phase))

                coh_sum[i, j] += coh_m
                stab_sum[i, j] += stab
                bias_sum[i, j] += bias
                mean_vec[i, j] += mu
                counts[i, j] += 1

    # Symmetrize and average
    coh = np.zeros((n_ch, n_ch), dtype=np.float64)
    stab = np.zeros((n_ch, n_ch), dtype=np.float64)
    bias = np.zeros((n_ch, n_ch), dtype=np.float64)
    mean_angle = np.zeros((n_ch, n_ch), dtype=np.float64)
    for i in range(n_ch):
        for j in range(i + 1, n_ch):
            c = counts[i, j]
            if c == 0:
                continue
            coh_ij = coh_sum[i, j] / c
            stab_ij = stab_sum[i, j] / c
            bias_ij = bias_sum[i, j] / c
            mv = mean_vec[i, j] / c
            ang = float(np.angle(mv))

            coh[i, j] = coh[j, i] = coh_ij
            stab[i, j] = stab[j, i] = stab_ij
            bias[i, j] = -bias_ij
            bias[j, i] = bias_ij
            mean_angle[i, j] = -ang
            mean_angle[j, i] = ang

    return coh.astype(np.float32), stab.astype(np.float32), bias.astype(np.float32), mean_angle.astype(np.float32)


def extract_edges(
    ids: list[int],
    coh: np.ndarray,
    stab: np.ndarray,
    bias: np.ndarray,
    mean_angle: np.ndarray,
    *,
    coh_threshold: float,
    stab_threshold: float,
    bias_threshold: float,
) -> list[EdgeMetrics]:
    edges: list[EdgeMetrics] = []
    n = len(ids)
    for i in range(n):
        for j in range(i + 1, n):
            c = float(coh[i, j])
            s = float(stab[i, j])
            if not (math.isfinite(c) and math.isfinite(s)):
                continue
            if c < coh_threshold or s < stab_threshold:
                continue
            b = float(bias[i, j])  # signed for direction
            if abs(b) < bias_threshold:
                continue
            ang = float(mean_angle[i, j])
            score = c * s * abs(b)
            edges.append(EdgeMetrics(a=ids[i], b=ids[j], coh_avg=c, ph_stab_avg=s, ph_bias=b, ph_mean=ang, score=score))
    edges.sort(key=lambda e: e.score, reverse=True)
    return edges


def kmeans(X: np.ndarray, k: int, *, iters: int = 50, seed: int = 0) -> tuple[np.ndarray, np.ndarray, float]:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    if n == 0:
        return np.zeros((0,), dtype=np.int32), np.zeros((k, X.shape[1]), dtype=np.float32), 0.0
    # init: pick random points
    idx = rng.choice(n, size=min(k, n), replace=False)
    centers = X[idx].copy()
    labels = np.zeros((n,), dtype=np.int32)
    for _ in range(iters):
        # assign
        d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        new_labels = np.argmin(d2, axis=1).astype(np.int32)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        # update
        for j in range(k):
            mask = labels == j
            if not np.any(mask):
                centers[j] = X[rng.integers(0, n)]
            else:
                centers[j] = X[mask].mean(axis=0)
    inertia = float(((X - centers[labels]) ** 2).sum())
    return labels, centers, inertia


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Quantize/cluster LHD diagnostic bridge edges from waveform data.")
    ap.add_argument("--root", action="append", required=True, help="Extracted diagnostic root dir (repeatable).")
    ap.add_argument("--stride", type=int, default=64)
    ap.add_argument("--max-points", type=int, default=32768)
    ap.add_argument("--window", type=int, default=2048)
    ap.add_argument("--step", type=int, default=1024)
    ap.add_argument("--fmin", type=float, default=1.0)
    ap.add_argument("--fmax", type=float, default=1000.0)
    ap.add_argument("--coh-threshold", type=float, default=0.05)
    ap.add_argument("--stab-threshold", type=float, default=0.20)
    ap.add_argument("--bias-threshold", type=float, default=0.10)
    ap.add_argument("--kmin", type=int, default=2)
    ap.add_argument("--kmax", type=int, default=12)
    ap.add_argument("--out-prefix", default="LHD_BRIDGE_QUANT")
    args = ap.parse_args(argv)

    all_edge_rows: list[dict[str, object]] = []
    all_feat: list[list[float]] = []

    for root_s in args.root:
        root = Path(root_s)
        diag_name = root.name.split("-")[0]
        chans = discover_channels(root)
        if not chans:
            continue

        series: dict[int, np.ndarray] = {}
        clocks: list[float] = []
        for c in chans:
            x = load_waveform_auto(c.dat_path, stride=args.stride, max_points=args.max_points)
            if x.size == 0:
                continue
            series[c.channel_index] = x
            if c.clock_hz:
                clocks.append(c.clock_hz)

        ids = sorted(series.keys())
        if len(ids) < 3:
            continue

        sr = float(np.median(clocks)) if clocks else 1_000_000.0
        sr = sr / float(args.stride)

        mats = [series[i] for i in ids]
        min_len = min(m.size for m in mats)
        if min_len <= 0:
            continue
        X = np.stack([m[:min_len] for m in mats], axis=0)
        coh, stab, bias, mean_ang = edge_metrics_matrix(
            X,
            sample_rate_hz=sr,
            window_size=args.window,
            step_size=args.step,
            band_hz=(args.fmin, args.fmax),
        )
        edges = extract_edges(
            ids,
            coh,
            stab,
            bias,
            mean_ang,
            coh_threshold=args.coh_threshold,
            stab_threshold=args.stab_threshold,
            bias_threshold=args.bias_threshold,
        )

        for e in edges:
            # Feature vector for clustering: [coh, stab, abs(bias), cos(phase), sin(phase)]
            feat = [e.coh_avg, e.ph_stab_avg, abs(e.ph_bias), math.cos(e.ph_mean), math.sin(e.ph_mean)]
            all_feat.append(feat)
            all_edge_rows.append(
                {
                    "diagnostic": diag_name,
                    "root": str(root),
                    "a": e.a,
                    "b": e.b,
                    "coh_avg": e.coh_avg,
                    "phase_stability": e.ph_stab_avg,
                    "phase_bias": e.ph_bias,
                    "phase_mean_rad": e.ph_mean,
                    "score": e.score,
                }
            )

    out_edges = Path(f"{args.out_prefix}_EDGES.csv")
    out_cluster = Path(f"{args.out_prefix}_CLUSTERS.json")
    out_inertia = Path(f"{args.out_prefix}_INERTIA_SWEEP.csv")

    if not all_edge_rows:
        out_edges.write_text("", encoding="utf-8")
        out_cluster.write_text(json.dumps({"error": "no edges extracted"}, indent=2), encoding="utf-8")
        out_inertia.write_text("", encoding="utf-8")
        print("NO_EDGES")
        return 2

    with out_edges.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_edge_rows[0].keys()))
        w.writeheader()
        w.writerows(all_edge_rows)

    Xf = np.asarray(all_feat, dtype=np.float32)
    # Normalize columns (except sin/cos already bounded)
    mu = Xf.mean(axis=0)
    sig = Xf.std(axis=0)
    sig[sig == 0] = 1.0
    Xn = (Xf - mu) / sig

    inertias: list[dict[str, object]] = []
    best = None
    for k in range(args.kmin, args.kmax + 1):
        labels, centers, inertia = kmeans(Xn, k, iters=60, seed=0)
        inertias.append({"k": k, "inertia": inertia})
        if best is None or inertia < best["inertia"]:
            best = {"k": k, "inertia": inertia, "labels": labels, "centers": centers}

    with out_inertia.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["k", "inertia"])
        w.writeheader()
        w.writerows(inertias)

    # Use best (lowest inertia) as default labeling (simple)
    labels = best["labels"]
    k = int(best["k"])
    # attach labels to edges
    for row, lab in zip(all_edge_rows, labels.tolist()):
        row["cluster"] = int(lab)

    # cluster summary
    counts = defaultdict(int)
    for lab in labels.tolist():
        counts[int(lab)] += 1
    cluster_summary = {
        "params": {
            "roots": args.root,
            "stride": args.stride,
            "max_points": args.max_points,
            "window": args.window,
            "step": args.step,
            "fmin": args.fmin,
            "fmax": args.fmax,
            "coh_threshold": args.coh_threshold,
            "stab_threshold": args.stab_threshold,
            "bias_threshold": args.bias_threshold,
        },
        "edges_total": len(all_edge_rows),
        "k_chosen": k,
        "inertia_sweep": inertias,
        "cluster_counts": dict(sorted(counts.items())),
        "feature_mean": mu.tolist(),
        "feature_std": sig.tolist(),
    }
    out_cluster.write_text(json.dumps(cluster_summary, indent=2), encoding="utf-8")

    # rewrite edges with cluster column
    with out_edges.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(all_edge_rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_edge_rows)

    print(json.dumps(cluster_summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
