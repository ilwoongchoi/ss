from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConstRow:
    name: str
    raw_value: str
    source_file: str
    level: str
    classification: str
    description: str
    value_num: float | None


def _to_float(raw: str) -> float | None:
    s = (raw or "").strip()
    if not s:
        return None
    # normalize common tokens
    s = s.replace("π", "pi")
    s = s.replace("PI", "pi")
    s = s.replace("~", "")
    s = s.replace("≈", "")
    s = s.replace(" ", "")
    s = s.replace("?/20", "pi/20")
    # allow simple fractions and pi fractions
    if re.fullmatch(r"-?\d+/\d+", s):
        a, b = s.split("/", 1)
        return float(a) / float(b)
    if re.fullmatch(r"pi/\d+", s):
        _, d = s.split("/", 1)
        return math.pi / float(d)
    if re.fullmatch(r"-?\d+(\.\d+)?(e-?\d+)?", s, flags=re.IGNORECASE):
        try:
            return float(s)
        except ValueError:
            return None
    return None


def load_constants(path: Path) -> list[ConstRow]:
    rows: list[ConstRow] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            name = (row.get("Constant") or "").strip()
            raw_value = (row.get("Value") or "").strip()
            if not name:
                continue
            rows.append(
                ConstRow(
                    name=name,
                    raw_value=raw_value,
                    source_file=(row.get("Source File") or "").strip(),
                    level=(row.get("Level") or "").strip(),
                    classification=(row.get("Classification") or "").strip(),
                    description=(row.get("Description") or "").strip(),
                    value_num=_to_float(raw_value),
                )
            )
    return rows


def load_lhd_edges(path: Path) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                out.append(
                    {
                        "coh": float(row["coh_avg"]),
                        "stab": float(row["phase_stability"]),
                        "bias_abs": abs(float(row["phase_bias"])),
                        "phase": float(row["phase_mean_rad"]),
                        "score": float(row["score"]),
                        "cluster": float(row["cluster"]),
                    }
                )
            except Exception:
                continue
    return out


def nearest(xs: list[float], v: float) -> tuple[float, float]:
    # returns (best_x, abs_diff)
    best_x = xs[0]
    best_d = abs(xs[0] - v)
    for x in xs[1:]:
        d = abs(x - v)
        if d < best_d:
            best_d = d
            best_x = x
    return best_x, best_d


def snap_ratio(observed: float, step: float) -> tuple[float, float, float]:
    """
    Return (snapped, ratio=observed/snapped, residual=observed-snapped) snapping to nearest non-zero multiple of step.
    """
    if step == 0 or not math.isfinite(step):
        return float("nan"), float("nan"), float("nan")
    k = int(round(observed / step))
    if k == 0:
        k = 1 if observed >= 0 else -1
    snapped = k * step
    ratio = observed / snapped
    resid = observed - snapped
    return float(snapped), float(ratio), float(resid)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Use *all* geometry-package constants and map them onto LHD edge observables (snaps + detuning)."
    )
    ap.add_argument("--constants", default="TOTAL_CONSTANT_TABLE.csv")
    ap.add_argument("--lhd-edges", default="LHD_QUANT_HALPHA_BOLO_EDGES.csv")
    ap.add_argument("--out-prefix", default="GEOMETRY_PACKAGE_CONSTANTS_TO_LHD")
    args = ap.parse_args(argv)

    const_rows = load_constants(Path(args.constants))
    edges = load_lhd_edges(Path(args.lhd_edges))
    if not edges:
        raise SystemExit(f"No LHD edges loaded from {args.lhd_edges}")

    phases = [e["phase"] for e in edges if math.isfinite(e["phase"])]
    stabs = [e["stab"] for e in edges if math.isfinite(e["stab"])]
    bias_abs = [e["bias_abs"] for e in edges if math.isfinite(e["bias_abs"])]
    scores = [e["score"] for e in edges if math.isfinite(e["score"])]

    # duplicate detection by numeric value (tight)
    by_value: dict[float, list[str]] = defaultdict(list)
    for c in const_rows:
        if c.value_num is None:
            continue
        by_value[round(c.value_num, 12)].append(c.name)

    dupes = {v: names for v, names in by_value.items() if len(names) >= 2}

    mapped_rows: list[dict[str, object]] = []
    for c in const_rows:
        v = c.value_num
        status = "unmapped"
        mapping = ""
        evidence = {}

        if v is None:
            status = "non_numeric"
        else:
            # Heuristic mapping rules:
            # - If value in radians-ish range (0..pi): try snap phase to multiples of v.
            # - If value in degrees-ish range (>2*pi and <= 360): treat as degrees and map to phase by radians.
            # - If value in (0..1): try nearest on stab/bias_abs/score; also treat as candidate gate step for phase ratio via v*(pi) is nonsense, so skip.
            if 0 < abs(v) <= math.pi:
                # compute detuning ratios for all edges: observed/snapped_to_multiple_of_v
                ratios = []
                resids = []
                for ph in phases[:5000]:
                    snapped, ratio, resid = snap_ratio(ph, v)
                    ratios.append(ratio)
                    resids.append(resid)
                # summarize: how tightly ratios cluster around 1
                ratios_abs = [abs(r - 1.0) for r in ratios if math.isfinite(r)]
                res_abs = [abs(r) for r in resids if math.isfinite(r)]
                ratios_abs.sort()
                res_abs.sort()
                p50 = ratios_abs[len(ratios_abs) // 2] if ratios_abs else float("nan")
                p90 = ratios_abs[int(len(ratios_abs) * 0.9)] if ratios_abs else float("nan")
                status = "phase_snap_candidate"
                mapping = "phase_mean_rad ~= k*const (radians); detuning=observed/snapped"
                evidence = {"ratio_abs_p50": p50, "ratio_abs_p90": p90}
            elif 2 * math.pi < abs(v) <= 360.0:
                vr = math.radians(v)
                ratios = []
                for ph in phases[:5000]:
                    snapped, ratio, _ = snap_ratio(ph, vr)
                    ratios.append(ratio)
                ratios_abs = sorted(abs(r - 1.0) for r in ratios if math.isfinite(r))
                p50 = ratios_abs[len(ratios_abs) // 2] if ratios_abs else float("nan")
                p90 = ratios_abs[int(len(ratios_abs) * 0.9)] if ratios_abs else float("nan")
                status = "phase_snap_candidate_deg"
                mapping = "phase_mean_rad ~= k*rad(const_deg)"
                evidence = {"ratio_abs_p50": p50, "ratio_abs_p90": p90}
            elif 0 < abs(v) < 1.0:
                # nearest comparisons
                best_stab, d_stab = nearest(stabs, v)
                best_bias, d_bias = nearest(bias_abs, v)
                best_score, d_score = nearest(scores, v)
                status = "scalar_candidate"
                mapping = "nearest(stability/bias_abs/score)"
                evidence = {
                    "nearest_stability": best_stab,
                    "stability_abs_diff": d_stab,
                    "nearest_bias_abs": best_bias,
                    "bias_abs_diff": d_bias,
                    "nearest_score": best_score,
                    "score_abs_diff": d_score,
                }
            else:
                status = "out_of_lhd_range"
                mapping = "no direct LHD edge observable chosen"

        mapped_rows.append(
            {
                "Constant": c.name,
                "Value_raw": c.raw_value,
                "Value_num": v,
                "Source": c.source_file,
                "Level": c.level,
                "Class": c.classification,
                "Status": status,
                "Mapping": mapping,
                "Evidence_json": json.dumps(evidence, ensure_ascii=False),
                "DupGroup": ";".join(dupes.get(round(v, 12), [])) if v is not None and round(v, 12) in dupes else "",
            }
        )

    out_csv = Path(f"{args.out_prefix}.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(mapped_rows[0].keys()))
        w.writeheader()
        w.writerows(mapped_rows)

    # Decide "keep vs discard" at the package level:
    # - keep if numeric and either phase_snap_candidate/deg or scalar_candidate
    # - discard if non_numeric or out_of_lhd_range (for this LHD mapping run)
    keep = []
    discard = []
    for r in mapped_rows:
        st = str(r["Status"])
        if st in ("phase_snap_candidate", "phase_snap_candidate_deg", "scalar_candidate"):
            keep.append(r["Constant"])
        else:
            discard.append({"Constant": r["Constant"], "Reason": st})

    out_json = Path(f"{args.out_prefix}_KEEP_DISCARD.json")
    out_json.write_text(
        json.dumps({"keep": keep, "discard": discard, "dupes": dupes}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(str(out_csv))
    print(str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

