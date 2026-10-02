from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def to_float(x: str) -> float:
    return float(x.strip())


def percentile(xs: list[float], p: float) -> float:
    if not xs:
        return float("nan")
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    i = (len(ys) - 1) * p
    lo = int(math.floor(i))
    hi = int(math.ceil(i))
    if lo == hi:
        return ys[lo]
    t = i - lo
    return ys[lo] * (1 - t) + ys[hi] * t


def lin_map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    if not (math.isfinite(x) and math.isfinite(x0) and math.isfinite(x1) and math.isfinite(y0) and math.isfinite(y1)):
        return float("nan")
    if x1 == x0:
        return (y0 + y1) / 2
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Map LHD edge-cluster vectors onto the project's universal bridge-vector scale (gap_dist/contact_score/drift_factor_used)."
    )
    ap.add_argument("--edges", default="LHD_QUANT_HALPHA_BOLO_EDGES.csv")
    ap.add_argument("--universal", default="BRIDGE_VECTORS_FINAL.csv")
    ap.add_argument("--out-prefix", default="LHD_TO_UNIVERSAL")
    args = ap.parse_args(argv)

    edges_path = Path(args.edges)
    uni_path = Path(args.universal)

    edges = read_csv(edges_path)
    uni = read_csv(uni_path)
    if not edges:
        raise SystemExit(f"No edges in {edges_path}")
    if not uni:
        raise SystemExit(f"No rows in {uni_path}")

    # Universal ranges (target scale)
    uni_gap = [to_float(r["gap_dist"]) for r in uni if r.get("gap_dist")]
    uni_contact = [to_float(r["contact_score"]) for r in uni if r.get("contact_score")]
    uni_drift = [to_float(r["drift_factor_used"]) for r in uni if r.get("drift_factor_used")]

    gap_min, gap_max = min(uni_gap), max(uni_gap)
    contact_min, contact_max = min(uni_contact), max(uni_contact)
    drift_min, drift_max = min(uni_drift), max(uni_drift)

    # LHD edge raw distributions
    scores = [to_float(r["score"]) for r in edges if r.get("score")]
    stabs = [to_float(r["phase_stability"]) for r in edges if r.get("phase_stability")]
    bias_abs = [abs(to_float(r["phase_bias"])) for r in edges if r.get("phase_bias")]

    # Robust anchors (avoid outliers)
    s_lo, s_hi = percentile(scores, 0.05), percentile(scores, 0.95)
    stab_lo, stab_hi = percentile(stabs, 0.05), percentile(stabs, 0.95)
    bias_lo, bias_hi = percentile(bias_abs, 0.05), percentile(bias_abs, 0.95)

    # Heuristic mapping:
    # - contact_score ~ normalized score on universal contact range
    # - gap_dist ~ inverse contact (higher contact => smaller gap) scaled to universal gap range
    # - drift_factor_used ~ inverse phase_stability (less stable => more drift) scaled to universal drift range,
    #   modulated by phase_bias strength (bias closer to 0 => more drift).
    by_cluster: dict[int, list[dict[str, str]]] = defaultdict(list)
    for r in edges:
        by_cluster[int(r["cluster"])].append(r)

    out_rows: list[dict[str, object]] = []
    for cid, rows in sorted(by_cluster.items()):
        s = [to_float(r["score"]) for r in rows]
        c = [to_float(r["coh_avg"]) for r in rows]
        st = [to_float(r["phase_stability"]) for r in rows]
        b = [abs(to_float(r["phase_bias"])) for r in rows]
        ph = [to_float(r["phase_mean_rad"]) for r in rows]

        s_mean = float(sum(s) / len(s))
        coh_mean = float(sum(c) / len(c))
        stab_mean = float(sum(st) / len(st))
        bias_mean = float(sum(b) / len(b))
        # circular mean for phase
        z = complex(0.0, 0.0)
        for ang in ph:
            z += complex(math.cos(ang), math.sin(ang))
        ph_mean = math.atan2(z.imag, z.real) if abs(z) > 0 else 0.0

        contact = lin_map(s_mean, s_lo, s_hi, contact_min, contact_max)
        contact = float(max(min(contact, contact_max), contact_min))
        gap = lin_map(1.0 - contact, 1.0 - contact_max, 1.0 - contact_min, gap_min, gap_max)
        gap = float(max(min(gap, gap_max), gap_min))

        # drift proxy: higher when stability low or bias weak
        stab_norm = lin_map(stab_mean, stab_lo, stab_hi, 0.0, 1.0)
        bias_norm = lin_map(bias_mean, bias_lo, bias_hi, 0.0, 1.0)
        drift_raw = (1.0 - stab_norm) * (1.0 + (1.0 - bias_norm))
        drift = lin_map(drift_raw, 0.0, 2.0, drift_min, drift_max)
        drift = float(max(min(drift, drift_max), drift_min))

        out_rows.append(
            {
                "cluster": cid,
                "edges_n": len(rows),
                "score_mean": s_mean,
                "coh_mean": coh_mean,
                "phase_stability_mean": stab_mean,
                "phase_bias_abs_mean": bias_mean,
                "phase_mean_rad": ph_mean,
                # mapped to your universal vector scale
                "mapped_contact_score": contact,
                "mapped_gap_dist": gap,
                "mapped_drift_factor_used": drift,
            }
        )

    out_csv = Path(f"{args.out_prefix}_CLUSTER_TO_UNIVERSAL.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    out_json = Path(f"{args.out_prefix}_MAPPING_META.json")
    out_json.write_text(
        json.dumps(
            {
                "inputs": {"edges": str(edges_path), "universal": str(uni_path)},
                "universal_ranges": {
                    "gap_min": gap_min,
                    "gap_max": gap_max,
                    "contact_min": contact_min,
                    "contact_max": contact_max,
                    "drift_min": drift_min,
                    "drift_max": drift_max,
                },
                "lhd_anchors": {
                    "score_p05": s_lo,
                    "score_p95": s_hi,
                    "phase_stability_p05": stab_lo,
                    "phase_stability_p95": stab_hi,
                    "phase_bias_abs_p05": bias_lo,
                    "phase_bias_abs_p95": bias_hi,
                },
                "notes": [
                    "This is an isomorphic *scale mapping* onto the project's existing bridge-vector fields, not a claim that LHD edges are literally the same nodes as synthetic_alpha/core_center.",
                    "If you want stricter quantization to specific constants (e.g., 1/28, pi/20), provide the constant list file and we can snap mapped_gap_dist / phase_mean to nearest bins and report residuals.",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(str(out_csv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
