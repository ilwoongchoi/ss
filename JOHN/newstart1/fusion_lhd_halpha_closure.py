from __future__ import annotations

import argparse
import csv
import dataclasses
import json
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
        # Example: Aurora14,ClockSpeed,1000000,4
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3 and parts[1] == "ClockSpeed":
            try:
                return float(parts[2])
            except ValueError:
                return None
    return None


def discover_channels(root: Path) -> list[Channel]:
    # Expect structure like: Halpha-187366-1/Halpha-187366-1/Halpha-187366-1-1.dat
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


class DSU:
    def __init__(self, items: list[int]) -> None:
        self.parent = {i: i for i in items}
        self.size = {i: 1 for i in items}

    def find(self, x: int) -> int:
        p = self.parent[x]
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        self.parent[x] = p
        return p

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def components(self) -> dict[int, list[int]]:
        out: dict[int, list[int]] = defaultdict(list)
        for k in self.parent.keys():
            out[self.find(k)].append(k)
        return dict(out)


def load_downsampled_int16(dat_path: Path, *, stride: int, max_points: int) -> np.ndarray:
    data = np.fromfile(dat_path, dtype="<i2")  # little-endian int16
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
    """
    Some LHD diagnostics store float32 waveforms. Try to load as float32.
    """
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
    """
    Try int16 first (Halpha/Bolometer style), then float32 (Magnetics etc.).
    Ensure deterministic length by enforcing max_points.
    """
    x = load_downsampled_int16(dat_path, stride=stride, max_points=max_points)
    # If int16 interpretation yields a near-constant pattern (std ~ 0), try float32.
    if x.size == 0 or float(np.std(x)) == 0.0:
        xf = load_downsampled_float32(dat_path, stride=stride, max_points=max_points)
        if xf.size:
            return xf
    return x


def corr_edges(X: np.ndarray, *, threshold: float) -> list[tuple[int, int, float]]:
    # X shape: (n_channels, n_time)
    C = np.corrcoef(X)
    edges: list[tuple[int, int, float]] = []
    n = C.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            c = float(C[i, j])
            if np.isfinite(c) and c >= threshold:
                edges.append((i, j, c))
    edges.sort(key=lambda e: e[2], reverse=True)
    return edges


def spectral_signature(x: np.ndarray, *, topk: int) -> tuple[int, ...]:
    if x.size == 0:
        return tuple()
    # Real FFT magnitude; ignore DC
    y = np.fft.rfft(x)
    mag = np.abs(y).astype(np.float64)
    if mag.size <= 2:
        return tuple()
    mag[0] = 0.0
    # pick topk bins
    idx = np.argpartition(mag, -topk)[-topk:]
    idx = idx[np.argsort(mag[idx])[::-1]]
    return tuple(int(i) for i in idx.tolist())


def spectral_edges(signatures: list[tuple[int, ...]], *, min_shared: int) -> list[tuple[int, int, float]]:
    edges: list[tuple[int, int, float]] = []
    n = len(signatures)
    sets = [set(sig) for sig in signatures]
    for i in range(n):
        si = sets[i]
        if not si:
            continue
        for j in range(i + 1, n):
            sj = sets[j]
            if not sj:
                continue
            shared = len(si.intersection(sj))
            if shared >= min_shared:
                # score = shared count normalized by union
                score = shared / len(si.union(sj))
                edges.append((i, j, float(score)))
    edges.sort(key=lambda e: e[2], reverse=True)
    return edges


def coherence_edges(
    X: np.ndarray,
    *,
    sample_rate_hz: float,
    window_size: int,
    step_size: int,
    band_hz: tuple[float, float],
    coherence_threshold: float,
    phase_stability_threshold: float,
) -> list[tuple[int, int, float]]:
    """
    Edge = strong shared oscillatory content with stable relative phase.

    - coherence: magnitude-squared coherence averaged over windows in band
    - phase stability: |mean(exp(i*phase))| averaged over band over windows
      (close to 1 => stable phase; close to 0 => random phase)
    """
    n_ch, n_t = X.shape
    if n_t < window_size:
        return []

    f = np.fft.rfftfreq(window_size, d=1.0 / sample_rate_hz)
    fmin, fmax = band_hz
    band_mask = (f >= fmin) & (f <= fmax)
    if not np.any(band_mask):
        return []

    # Collect per-window spectra
    windows: list[np.ndarray] = []
    for start in range(0, n_t - window_size + 1, step_size):
        seg = X[:, start : start + window_size]
        # Hann window to reduce leakage
        w = np.hanning(window_size).astype(np.float32)
        segw = seg * w[None, :]
        Y = np.fft.rfft(segw, axis=1)  # (n_ch, n_f)
        windows.append(Y)
    if not windows:
        return []

    edges: list[tuple[int, int, float]] = []
    # Precompute autospectra per window
    autos = [np.abs(Y) ** 2 for Y in windows]  # list of (n_ch, n_f)

    for i in range(n_ch):
        for j in range(i + 1, n_ch):
            coh_vals: list[float] = []
            ph_stab_vals: list[float] = []
            for Y, P in zip(windows, autos):
                Pxx = P[i]
                Pyy = P[j]
                Pxy = Y[i] * np.conj(Y[j])
                # coherence per frequency
                denom = Pxx * Pyy
                valid = denom > 0
                mask = band_mask & valid
                if not np.any(mask):
                    continue
                coh = (np.abs(Pxy[mask]) ** 2) / denom[mask]
                coh_mean = float(np.mean(coh))

                phase = np.angle(Pxy[mask])
                ph_stab = float(np.abs(np.mean(np.exp(1j * phase))))

                coh_vals.append(coh_mean)
                ph_stab_vals.append(ph_stab)

            if not coh_vals:
                continue

            coh_avg = float(np.mean(coh_vals))
            ph_stab_avg = float(np.mean(ph_stab_vals)) if ph_stab_vals else 0.0
            if coh_avg >= coherence_threshold and ph_stab_avg >= phase_stability_threshold:
                # score prioritizes coherence but penalizes phase instability
                score = coh_avg * ph_stab_avg
                edges.append((i, j, score))

    edges.sort(key=lambda e: e[2], reverse=True)
    return edges


def directed_phase_edges(
    X: np.ndarray,
    *,
    sample_rate_hz: float,
    window_size: int,
    step_size: int,
    band_hz: tuple[float, float],
    coherence_threshold: float,
    phase_stability_threshold: float,
    phase_bias_threshold: float,
) -> list[tuple[int, int, float]]:
    """
    Build directed edges i->j if i tends to lead j with stable sign of phase difference in-band.
    Score = coherence_avg * phase_stability_avg * |phase_bias|

    phase_bias = mean(sign(sin(phase))) across band+windows
    - positive => i leads j (phase mostly +)
    - negative => j leads i
    """
    n_ch, n_t = X.shape
    if n_t < window_size:
        return []

    f = np.fft.rfftfreq(window_size, d=1.0 / sample_rate_hz)
    fmin, fmax = band_hz
    band_mask = (f >= fmin) & (f <= fmax)
    if not np.any(band_mask):
        return []

    windows: list[np.ndarray] = []
    for start in range(0, n_t - window_size + 1, step_size):
        seg = X[:, start : start + window_size]
        w = np.hanning(window_size).astype(np.float32)
        Y = np.fft.rfft(seg * w[None, :], axis=1)
        windows.append(Y)
    autos = [np.abs(Y) ** 2 for Y in windows]

    directed: list[tuple[int, int, float]] = []
    for i in range(n_ch):
        for j in range(i + 1, n_ch):
            coh_vals: list[float] = []
            ph_stab_vals: list[float] = []
            bias_vals: list[float] = []
            for Y, P in zip(windows, autos):
                Pxx = P[i]
                Pyy = P[j]
                Pxy = Y[i] * np.conj(Y[j])
                denom = Pxx * Pyy
                valid = denom > 0
                mask = band_mask & valid
                if not np.any(mask):
                    continue
                coh = (np.abs(Pxy[mask]) ** 2) / denom[mask]
                coh_mean = float(np.mean(coh))
                phase = np.angle(Pxy[mask])
                ph_stab = float(np.abs(np.mean(np.exp(1j * phase))))
                bias = float(np.mean(np.sign(np.sin(phase))))
                coh_vals.append(coh_mean)
                ph_stab_vals.append(ph_stab)
                bias_vals.append(bias)
            if not coh_vals:
                continue
            coh_avg = float(np.mean(coh_vals))
            ph_stab_avg = float(np.mean(ph_stab_vals))
            bias_avg = float(np.mean(bias_vals))
            if coh_avg < coherence_threshold or ph_stab_avg < phase_stability_threshold:
                continue
            if abs(bias_avg) < phase_bias_threshold:
                continue
            score = coh_avg * ph_stab_avg * abs(bias_avg)
            if bias_avg > 0:
                directed.append((i, j, score))
            else:
                directed.append((j, i, score))
    directed.sort(key=lambda e: e[2], reverse=True)
    return directed


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="LHD Halpha pilot: closure-grammar test using channel-correlation graph.")
    ap.add_argument("--root", default="Halpha-187366-1", help="Directory containing extracted LHD diagnostic zip contents.")
    ap.add_argument("--base-topk", type=int, default=20, help="Base/internal universe = top-K channels by variance proxy.")
    ap.add_argument("--stride", type=int, default=128, help="Downsample stride for each channel time series.")
    ap.add_argument("--max-points", type=int, default=4096, help="Cap time points after downsampling.")
    ap.add_argument("--metric", choices=["corr", "spectral", "coherence"], default="coherence")
    ap.add_argument("--corr-threshold", type=float, default=0.80, help="Used when --metric=corr")
    ap.add_argument("--spectral-topk", type=int, default=5, help="Used when --metric=spectral")
    ap.add_argument("--spectral-min-shared", type=int, default=1, help="Used when --metric=spectral")
    ap.add_argument("--coh-window", type=int, default=1024, help="Used when --metric=coherence (samples after downsampling)")
    ap.add_argument("--coh-step", type=int, default=512, help="Used when --metric=coherence (samples after downsampling)")
    ap.add_argument("--coh-fmin", type=float, default=5_000.0, help="Used when --metric=coherence (Hz)")
    ap.add_argument("--coh-fmax", type=float, default=80_000.0, help="Used when --metric=coherence (Hz)")
    ap.add_argument("--coh-threshold", type=float, default=0.20, help="Used when --metric=coherence (avg magnitude-squared coherence)")
    ap.add_argument("--phase-stability", type=float, default=0.60, help="Used when --metric=coherence")
    ap.add_argument("--phase-bias", type=float, default=0.10, help="Used when --metric=coherence (directed edge sign threshold)")
    ap.add_argument("--out-prefix", default="LHD_HALPHA_CLOSURE")
    args = ap.parse_args(argv)

    root = Path(args.root)
    channels = discover_channels(root)
    if not channels:
        raise SystemExit(f"No .dat channels found under {root}")

    # Load all channels (downsampled) and compute a simple variance proxy to rank.
    series: dict[int, np.ndarray] = {}
    var_proxy: list[tuple[int, float]] = []
    for ch in channels:
        x = load_waveform_auto(ch.dat_path, stride=args.stride, max_points=args.max_points)
        if x.size == 0:
            continue
        series[ch.channel_index] = x
        var_proxy.append((ch.channel_index, float(np.var(x))))

    var_proxy.sort(key=lambda t: t[1], reverse=True)
    if not var_proxy:
        raise SystemExit("All channels empty after load.")

    base_ids = [cid for cid, _ in var_proxy[: args.base_topk]]
    ext_ids = sorted(series.keys())

    def build_graph(ids: list[int]) -> tuple[int, list[tuple[int, int, float]], DSU]:
        # Ensure equal lengths (some diagnostics differ slightly). Truncate to min length.
        mats = [series[i] for i in ids]
        min_len = min(m.size for m in mats)
        if min_len <= 0:
            return len(ids), [], DSU(ids)
        X = np.stack([m[:min_len] for m in mats], axis=0)
        if args.metric == "corr":
            edges_idx = corr_edges(X, threshold=args.corr_threshold)
        else:
            if args.metric == "spectral":
                sigs = [spectral_signature(X[k], topk=args.spectral_topk) for k in range(X.shape[0])]
                edges_idx = spectral_edges(sigs, min_shared=args.spectral_min_shared)
            else:
                # sample rate: prefer from prm clock if consistent, otherwise default 1 MHz (Aurora14 in prm)
                clock_vals = [c.clock_hz for c in channels if c.channel_index in ids and c.clock_hz]
                sr = float(np.median(clock_vals)) if clock_vals else 1_000_000.0
                sr = sr / float(args.stride)
                edges_idx = coherence_edges(
                    X,
                    sample_rate_hz=sr,
                    window_size=args.coh_window,
                    step_size=args.coh_step,
                    band_hz=(args.coh_fmin, args.coh_fmax),
                    coherence_threshold=args.coh_threshold,
                    phase_stability_threshold=args.phase_stability,
                )
        # map back to channel ids
        edges = [(ids[i], ids[j], c) for i, j, c in edges_idx]
        dsu = DSU(ids)
        for a, b, _c in edges:
            dsu.union(a, b)
        return len(dsu.components()), edges, dsu

    base_components, base_edges, base_dsu = build_graph(base_ids)
    ext_components, ext_edges, ext_dsu = build_graph(ext_ids)
    base_components_inside_extended = len({ext_dsu.find(i) for i in base_ids})

    # Directionality / chirality proxy: directed phase-lead edges (computed on extended set only, using same SR/band params)
    directed_edges_count = 0
    directed_balance = 0.0
    if args.metric == "coherence":
        mats = [series[i] for i in ext_ids]
        min_len = min(m.size for m in mats) if mats else 0
        if min_len > 0:
            Xext = np.stack([m[:min_len] for m in mats], axis=0)
        else:
            Xext = np.zeros((0, 0), dtype=np.float32)
        clock_vals = [c.clock_hz for c in channels if c.channel_index in ext_ids and c.clock_hz]
        sr = float(np.median(clock_vals)) if clock_vals else 1_000_000.0
        sr = sr / float(args.stride)
        if Xext.size:
            d_edges = directed_phase_edges(
                Xext,
                sample_rate_hz=sr,
                window_size=args.coh_window,
                step_size=args.coh_step,
                band_hz=(args.coh_fmin, args.coh_fmax),
                coherence_threshold=args.coh_threshold,
                phase_stability_threshold=args.phase_stability,
                phase_bias_threshold=args.phase_bias,
            )
            directed_edges_count = len(d_edges)
            # simple asymmetry measure: outdegree-in degree summed absolute normalized
            outdeg = defaultdict(int)
            indeg = defaultdict(int)
            for a_idx, b_idx, _s in d_edges:
                outdeg[ext_ids[a_idx]] += 1
                indeg[ext_ids[b_idx]] += 1
            nodes = set(ext_ids)
            denom = max(1, sum(outdeg.values()))
            directed_balance = float(sum(abs(outdeg[n] - indeg[n]) for n in nodes) / denom)

    # Mediator channels = channels not in base that connect (touch) 2+ DISTINCT base components
    # where base components are computed in the BASE graph (internal universe).
    base_root = {bid: base_dsu.find(bid) for bid in base_ids}
    base_roots_set = set(base_root.values())
    ext_adj: dict[int, set[int]] = defaultdict(set)
    for a, b, _ in ext_edges:
        ext_adj[a].add(b)
        ext_adj[b].add(a)

    mediators: list[dict[str, object]] = []
    for mid in ext_ids:
        if mid in base_ids:
            continue
        touched = {base_root[n] for n in ext_adj.get(mid, set()) if n in base_root}
        if len(touched) >= 2:
            mediators.append({"mediator_channel": mid, "touched_base_components": len(touched)})
    mediators.sort(key=lambda r: int(r["touched_base_components"]), reverse=True)

    out_summary = Path(f"{args.out_prefix}_SUMMARY.json")
    out_report = Path(f"{args.out_prefix}_REPORT.md")
    out_mediators = Path(f"{args.out_prefix}_MEDIATORS.csv")

    summary = {
        "input_root": str(root),
        "params": {
            "base_topk": args.base_topk,
            "stride": args.stride,
            "max_points": args.max_points,
            "metric": args.metric,
            "corr_threshold": args.corr_threshold,
            "spectral_topk": args.spectral_topk,
            "spectral_min_shared": args.spectral_min_shared,
            "coh_window": args.coh_window,
            "coh_step": args.coh_step,
            "coh_fmin": args.coh_fmin,
            "coh_fmax": args.coh_fmax,
            "coh_threshold": args.coh_threshold,
            "phase_stability": args.phase_stability,
            "phase_bias": args.phase_bias,
        },
        "counts": {
            "channels_total_found": len(channels),
            "channels_loaded": len(series),
            "base_channels": len(base_ids),
            "extended_channels": len(ext_ids),
        },
        "closure": {
            "base_components": base_components,
            "extended_components": ext_components,
            "base_components_inside_extended": base_components_inside_extended,
            "base_edges": len(base_edges),
            "extended_edges": len(ext_edges),
            "mediator_channels_found": len(mediators),
            "directed_edges_count": directed_edges_count,
            "directed_balance": directed_balance,
            "base_top_component_sizes": sorted((len(v) for v in base_dsu.components().values()), reverse=True)[:10],
            "extended_top_component_sizes": sorted((len(v) for v in ext_dsu.components().values()), reverse=True)[:10],
        },
    }
    out_summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with out_mediators.open("w", newline="", encoding="utf-8") as f:
        if mediators:
            w = csv.DictWriter(f, fieldnames=list(mediators[0].keys()))
            w.writeheader()
            w.writerows(mediators[:200])
        else:
            f.write("")

    report = [
        "# LHD Halpha — Channel-Graph Closure Pilot",
        "",
        f"- Input: `{root}`",
        f"- Base/internal universe: top `{args.base_topk}` channels by variance proxy",
        f"- Extended universe: all loaded channels",
        f"- Edge rule: correlation ≥ `{args.corr_threshold}` on z-scored downsampled signals",
        "",
        "## Results",
        f"- Base components: `{base_components}`",
        f"- Extended components: `{ext_components}`",
        f"- Base components inside extended: `{base_components_inside_extended}`",
        f"- Mediator channels (non-base touching ≥2 base components): `{len(mediators)}` (`{out_mediators}`)",
        "",
        "## Note",
        "- This is a *fast* structural closure check (channel connectivity graph). It does not claim a full physics interpretation by itself.",
        "",
    ]
    out_report.write_text("\n".join(report), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
