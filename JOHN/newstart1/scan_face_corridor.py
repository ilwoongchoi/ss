import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import math
import csv
import os

from geometry_package.chart_operators import plp_spine_manifold
from geometry_package.regime1.shader2d_core import sample_core_fields_xy


@dataclass(frozen=True)
class PointScore:
    x: float
    y: float
    score: float


def _load_const() -> Dict[str, float]:
    g = importlib.import_module("128GIRD_MBTI_PHYSICS")
    return g.CONST


def _mirror_x(x: float, center: float) -> float:
    return center + (center - x)


def _dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def main() -> int:
    const = _load_const()
    n_rows = int(const.get("n_rows", 16))
    n_cols = int(const.get("n_cols", 16))
    center_x = n_cols / 2.0

    # Anchors from locked config (no new constants)
    cortisol_center = const.get("cortisol_center", [6.5, 5.0])
    gravity_center = const.get("gravity_sensor_center", [8.0, 14.5])
    darkness_gate = const.get("darkness_gate", {"x": 6.0, "y": 10.0, "width": 4.0, "height": 1.5})

    # Brow line (midpoints of eyebrows): use gravity sensor y as brow band
    brow_y = float(gravity_center[1])
    # Under-eye impedance line: slightly under the eye band
    under_eye_y = float(darkness_gate["y"]) - 0.5 * float(darkness_gate["height"])

    # Midpoints (medial under each eye)
    left_eye_medial = (center_x - 1.5, under_eye_y)
    right_eye_medial = (center_x + 1.5, under_eye_y)
    left_brow_mid = (center_x - 1.5, brow_y)
    right_brow_mid = (center_x + 1.5, brow_y)

    # Right D2: use existing D2 placement from 128 grid comments (right D2 ~ x=14, y=6)
    right_d2 = (14.0, 6.0)
    left_d2 = (_mirror_x(right_d2[0], center_x), right_d2[1])

    # Right cortisol: mirror left cortisol center to right side
    right_cortisol = (_mirror_x(float(cortisol_center[0]), center_x), float(cortisol_center[1]))
    left_cortisol = (float(cortisol_center[0]), float(cortisol_center[1]))

    band_y_min = min(brow_y, under_eye_y)
    band_y_max = max(brow_y, under_eye_y)

    # Build candidate scores on grid (0.5 step)
    step = 0.5
    candidates: List[PointScore] = []
    for xi in range(int(n_cols / step) + 1):
        x = xi * step
        if x < 0 or x > n_cols:
            continue
        for yi in range(int(n_rows / step) + 1):
            y = yi * step
            if y < band_y_min or y > band_y_max:
                continue

            # Scoring: right-dominant docking + corridor continuity
            d2_score = 1.0 / (1.0 + _dist((x, y), right_d2))
            cortisol_above = 1.0 if y >= right_cortisol[1] else 0.0
            right_bias = 1.0 if x >= center_x else 0.5
            medial_bonus = 1.0 / (1.0 + _dist((x, y), right_eye_medial))

            # Corridor continuity: distance to midline between the two parallel lines
            band_mid_y = 0.5 * (band_y_min + band_y_max)
            corridor_bonus = 1.0 / (1.0 + abs(y - band_mid_y))

            score = (d2_score * 0.4) + (medial_bonus * 0.3) + (corridor_bonus * 0.2) + (cortisol_above * 0.1)
            score *= right_bias
            candidates.append(PointScore(x, y, score))

    # Corridor: best contiguous strip (choose best point per x, then longest contiguous region by score threshold)
    by_x: Dict[float, PointScore] = {}
    for p in candidates:
        if p.x not in by_x or p.score > by_x[p.x].score:
            by_x[p.x] = p

    ordered = [by_x[x] for x in sorted(by_x.keys())]
    # threshold at 70th percentile
    scores = [p.score for p in ordered]
    scores_sorted = sorted(scores)
    if not scores_sorted:
        return 1
    thr = scores_sorted[int(0.7 * (len(scores_sorted) - 1))]

    best_segment: List[PointScore] = []
    current: List[PointScore] = []
    last_x = None
    for p in ordered:
        if p.score >= thr and (last_x is None or abs(p.x - last_x) <= step + 1e-6):
            current.append(p)
        else:
            if len(current) > len(best_segment):
                best_segment = current
            current = [p] if p.score >= thr else []
        last_x = p.x
    if len(current) > len(best_segment):
        best_segment = current

    # Right dock: highest score inside corridor, right side
    corridor_points = best_segment if best_segment else ordered
    right_candidates = [p for p in corridor_points if p.x >= center_x and p.y >= right_cortisol[1]]
    if right_candidates:
        right_dock = max(right_candidates, key=lambda p: p.score)
    else:
        right_dock = max(corridor_points, key=lambda p: p.score)

    # Left dock: mirrored weak candidate
    left_dock = PointScore(_mirror_x(right_dock.x, center_x), right_dock.y, right_dock.score * 0.5)

    # Use locked coordinates if present (no new constants).
    lock_path = Path("FACE_CORRIDOR_LOCK.json")
    if lock_path.exists():
        out = json.loads(lock_path.read_text(encoding="utf-8"))
        out["anchors"] = {
            "brow_mid_left": left_brow_mid,
            "brow_mid_right": right_brow_mid,
            "under_eye_left": left_eye_medial,
            "under_eye_right": right_eye_medial,
            "right_d2": right_d2,
            "left_d2": left_d2,
            "right_cortisol": right_cortisol,
        }
        out["note"] = "Locked terminals + corridor; anchors provided for reference."
    else:
        out = {
            "anchors": {
                "brow_mid_left": left_brow_mid,
                "brow_mid_right": right_brow_mid,
                "under_eye_left": left_eye_medial,
                "under_eye_right": right_eye_medial,
                "right_d2": right_d2,
                "left_d2": left_d2,
                "right_cortisol": right_cortisol,
            },
            "band": {"y_min": band_y_min, "y_max": band_y_max},
            "corridor": [(p.x, p.y, p.score) for p in corridor_points],
            "right_dock": [right_dock.x, right_dock.y, right_dock.score],
            "left_dock": [left_dock.x, left_dock.y, left_dock.score],
            "note": "Corridor from brow-mid line to under-eye impedance line; right dock prioritized above right cortisol."
        }

    Path("FACE_CORRIDOR_SCAN.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Avoid clobber if file is locked; write to a new name if needed.
    out_csv = "FACE_CORRIDOR_POINTS.csv"
    if Path(out_csv).exists():
        out_csv = "FACE_CORRIDOR_POINTS_v2.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "score"])
        for p in corridor_points:
            w.writerow([p.x, p.y, p.score])

    # --- Choke band scan (left eye-under to nose bridge to alar/upper cheek) ---
    # Define a left-side band using existing anchors only.
    left_band_y_min = min(under_eye_y, left_cortisol[1])
    left_band_y_max = brow_y
    left_x_min = 0.0
    left_x_max = center_x

    def darkness_axis_score(x: float, y: float) -> float:
        # Proximity to the darkness gate rectangle centerline.
        gx = float(darkness_gate["x"])
        gy = float(darkness_gate["y"])
        return 1.0 / (1.0 + _dist((x, y), (gx, gy)))

    def plp_score(x: float, y: float) -> float:
        # PLP spine gate from chart_operators (already locked).
        return float(plp_spine_manifold((x, y), n_rows=float(n_rows), n_cols=float(n_cols)))

    def cortisol_boundary_score(x: float, y: float) -> float:
        # Favor points above left cortisol, and within the left band.
        return 1.0 if y >= left_cortisol[1] else 0.0

    choke_candidates: List[PointScore] = []
    for xi in range(int(n_cols / step) + 1):
        x = xi * step
        if x < left_x_min or x > left_x_max:
            continue
        for yi in range(int(n_rows / step) + 1):
            y = yi * step
            if y < left_band_y_min or y > left_band_y_max:
                continue

            # Choke band = overlap of PLP stress bridge, darkness/ROS axis, and boundary seam.
            s = (plp_score(x, y) * 0.45) + (darkness_axis_score(x, y) * 0.35) + (cortisol_boundary_score(x, y) * 0.20)
            choke_candidates.append(PointScore(x, y, s))

    # Keep top contiguous band by percentile.
    if choke_candidates:
        scores_c = sorted([p.score for p in choke_candidates])
        thr_c = scores_c[int(0.85 * (len(scores_c) - 1))]
        choke_band = [p for p in choke_candidates if p.score >= thr_c]
    else:
        choke_band = []

    choke_out = {
        "band": {"y_min": left_band_y_min, "y_max": left_band_y_max, "x_min": left_x_min, "x_max": left_x_max},
        "points": [(p.x, p.y, p.score) for p in choke_band],
        "note": "Choke band: PLP stress bridge + darkness axis + left boundary seam overlap."
    }
    Path("FACE_CHOKE_BAND_SCAN.json").write_text(json.dumps(choke_out, indent=2), encoding="utf-8")
    choke_csv = "FACE_CHOKE_BAND_POINTS.csv"
    if Path(choke_csv).exists():
        choke_csv = "FACE_CHOKE_BAND_POINTS_v2.csv"
    with open(choke_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "score"])
        for p in choke_band:
            w.writerow([p.x, p.y, p.score])

    # --- ROI scan (4 axes) ---
    step_roi = 0.25  # higher resolution for ROI mask scan
    roi_results = {}

    def scan_roi(name: str, mask_fn):
        pts = []
        for xi in range(int(n_cols / step_roi) + 1):
            x = xi * step_roi
            for yi in range(int(n_rows / step_roi) + 1):
                y = yi * step_roi
                if not mask_fn(x, y):
                    continue
                core = sample_core_fields_xy(x, y, n_rows=n_rows, n_cols=n_cols)
                # peak signal proxy: w_gate * kappa_eff (no new constants)
                score = float(core["w_gate"]) * float(core["kappa_eff"])
                pts.append((x, y, score, core["kappa_eff"], core["w_gate"], core["in_sh_band"]))

        pts_sorted = sorted(pts, key=lambda p: p[2], reverse=True)
        topk = pts_sorted[:10]
        # symmetry: compare left-right mirror scores for top 10
        sym = []
        for x, y, s, *_ in topk:
            mx = _mirror_x(x, center_x)
            # find closest mirrored point in list
            m = min(pts, key=lambda p: abs(p[0] - mx) + abs(p[1] - y)) if pts else None
            if m:
                sym.append(1.0 - abs(s - m[2]))
        sym_score = float(sum(sym) / len(sym)) if sym else 0.0

        roi_results[name] = {
            "count": len(pts),
            "topk": [(x, y, s) for x, y, s, *_ in topk],
            "symmetry_score": sym_score,
        }

        # write CSV per ROI
        out_csv = f"ROI_{name}_POINTS.csv"
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["x", "y", "score", "kappa_eff", "w_gate", "in_sh_band"])
            for row in pts:
                w.writerow(row)

    # ROI 1: Vasopressin neckband seat (Betti-5 ring center) -> use left cortisol y band as proxy
    # neckband: lower half band around y ~ 5.0 to 7.0, centered near midline
    def roi_vasopressin(x, y):
        return (y >= 4.5 and y <= 7.0) and (x >= center_x - 2.0 and x <= center_x + 2.0)

    # ROI 2: flash:center_in ↔ sheet_id:3 anchor
    # use flash corridor band y~9.5..12.5 around mid x
    def roi_flash_anchor(x, y):
        return (y >= 9.5 and y <= 12.5) and (x >= center_x - 1.0 and x <= center_x + 1.0)

    # ROI 3: Right D2 → Nose → Height Bridge vertical transition band
    # right side vertical band near x ~ 13..15 from y ~ 5..14
    def roi_right_d2_nose(x, y):
        return (x >= 12.5 and x <= 15.0) and (y >= 5.0 and y <= 14.5)

    # ROI 4: mediator:synthetic_alpha → sheet_id:4 closure axis
    # left-mid band near x ~ 2..6, y ~ 6..12 (bridge toward D4)
    def roi_mediator_to_d4(x, y):
        return (x >= 2.0 and x <= 6.0) and (y >= 6.0 and y <= 12.5)

    scan_roi("VASOPRESSIN_NECKBAND", roi_vasopressin)
    scan_roi("FLASH_ANCHOR", roi_flash_anchor)
    scan_roi("RIGHT_D2_NOSE_HEIGHT", roi_right_d2_nose)
    scan_roi("MEDIATOR_TO_SHEET4", roi_mediator_to_d4)

    # ROI 5: Depressor supercilii (glabella), slightly left of center
    # Use a tight patch around (center_x - 0.5, y ~ 11.0)
    def roi_glabella_left(x, y):
        return (x >= center_x - 1.0 and x <= center_x) and (y >= 10.5 and y <= 11.5)

    scan_roi("GLABELLA_LEFT", roi_glabella_left)

    # ROI 6: Nose center (strict central vertical)
    def roi_nose_center(x, y):
        return (x >= center_x - 0.25 and x <= center_x + 0.25) and (y >= 9.0 and y <= 12.5)

    scan_roi("NOSE_CENTER", roi_nose_center)

    # ROI 7: PLP cauldron (left brain inner edge, slightly inward from far left)
    # Approximate: left-inner quadrant, upper-mid band
    def roi_plp_cauldron(x, y):
        return (x >= 1.5 and x <= 3.5) and (y >= 11.0 and y <= 14.5)

    scan_roi("PLP_CAULDRON_LEFT", roi_plp_cauldron)

    # ROI 8: PLP cauldron deep (tighter, higher resolution)
    def roi_plp_cauldron_deep(x, y):
        return (x >= 2.0 and x <= 3.0) and (y >= 13.0 and y <= 14.5)

    scan_roi("PLP_CAULDRON_LEFT_DEEP", roi_plp_cauldron_deep)

    # ROI 9: PLP cauldron deeper (ultra-tight, higher resolution)
    def roi_plp_cauldron_deeper(x, y):
        return (x >= 2.0 and x <= 2.5) and (y >= 13.5 and y <= 14.5)

    scan_roi("PLP_CAULDRON_LEFT_DEEPER", roi_plp_cauldron_deeper)

    # ROI 10: PLP cauldron deepest (near-zero band)
    def roi_plp_cauldron_deepest(x, y):
        return (x >= 1.75 and x <= 2.25) and (y >= 14.0 and y <= 15.0)

    scan_roi("PLP_CAULDRON_LEFT_DEEPEST", roi_plp_cauldron_deepest)

    # ROI 11: Left outer orbicularis oculi above Left D2 (mirror of right vasopressin zone)
    # Left D2 is at (2,6); outer = lateral (lower x), above = higher y.
    def roi_left_d2_oculi_outer(x, y):
        return (x >= 0.0 and x <= 2.5) and (y >= 7.0 and y <= 12.0)

    scan_roi("LEFT_D2_OCULI_OUTER", roi_left_d2_oculi_outer)

    # ROI 12: LEFT_D2_OCULI_OUTER_DEEP (tighten around the current peak ~ (2.0, 9.75))
    def roi_left_d2_oculi_outer_deep(x, y):
        return (x >= 1.5 and x <= 2.5) and (y >= 9.25 and y <= 10.25)

    scan_roi("LEFT_D2_OCULI_OUTER_DEEP", roi_left_d2_oculi_outer_deep)

    # ROI 13: Right-side symmetric choke band (mirror of left PLP-Big Woman choke ridge)
    # Right cheek/under-eye/nose-ridge outer corridor: x in [center_x, 16], y in [5.0, 14.5]
    def roi_right_choke_band(x, y):
        return (x >= center_x and x <= n_cols) and (y >= 5.0 and y <= 14.5)

    scan_roi("RIGHT_CHOKE_BAND", roi_right_choke_band)

    # ROI 14: Alopecia point (left brain inner, more central than PLP/vasso; y near vasso)
    # Use relative rule: x more central than plp/vasso (x > 2.0), y ~ 14.2..15.0
    def roi_alopecia_left_inner(x, y):
        return (x >= 2.5 and x <= 4.5) and (y >= 14.2 and y <= 15.0)

    scan_roi("ALOPECIA_LEFT_INNER", roi_alopecia_left_inner)

    # ROI 15: Alopecia deep (tighten around current peak ~ (4.5, 14.75))
    def roi_alopecia_left_inner_deep(x, y):
        return (x >= 4.0 and x <= 5.0) and (y >= 14.5 and y <= 15.0)

    scan_roi("ALOPECIA_LEFT_INNER_DEEP", roi_alopecia_left_inner_deep)

    # ROI 16: Left eye inner to glabella corridor (inner canthus toward brow)
    def roi_left_inner_glabella(x, y):
        return (x >= center_x - 1.5 and x <= center_x - 0.25) and (y >= 9.5 and y <= 12.0)

    scan_roi("LEFT_INNER_GLABELLA", roi_left_inner_glabella)

    # ROI 17: Right eye inner to glabella corridor (mirror of left)
    def roi_right_inner_glabella(x, y):
        return (x >= center_x + 0.25 and x <= center_x + 1.5) and (y >= 9.5 and y <= 12.0)

    scan_roi("RIGHT_INNER_GLABELLA", roi_right_inner_glabella)

    # ROI 18: Time sensor (near gravity sensor y-band, slightly lateral on opposite side)
    # gravity_sensor_center ~ (8.0, 14.5); place time sensor slightly outside on right.
    def roi_time_sensor(x, y):
        return (x >= 9.0 and x <= 10.5) and (y >= 14.0 and y <= 15.5)

    scan_roi("TIME_SENSOR", roi_time_sensor)

    # ROI 19: Left nasalis + under-eye included (user request)
    # Left-side nose ridge + under-eye band
    def roi_left_nasalis_under_eye(x, y):
        return (x >= 4.5 and x <= 8.5) and (y >= 9.0 and y <= 14.5)

    scan_roi("LEFT_NASALIS_UNDEREYE", roi_left_nasalis_under_eye)

    # ROI 20: Left LLSAN (levator labii superioris alaeque nasi)
    # Narrow band along left nose-wing to upper lip junction.
    def roi_left_llsan(x, y):
        return (x >= 5.0 and x <= 7.0) and (y >= 10.0 and y <= 12.5)

    scan_roi("LEFT_LLSAN", roi_left_llsan)

    # ROI 21: Left Levator labii superioris (LLS) slightly lower than LLSAN
    def roi_left_lls(x, y):
        return (x >= 5.5 and x <= 7.5) and (y >= 9.0 and y <= 11.0)

    scan_roi("LEFT_LLS", roi_left_lls)

    # ROI 22: Cosmic ray point (right nostril outer frame / right epinephrine vicinity)
    # Right side nose pillar, slightly lateral to nostril, mid-lower band.
    def roi_cosmic_ray_right_nostril(x, y):
        return (x >= 9.5 and x <= 11.5) and (y >= 8.5 and y <= 11.0)

    scan_roi("COSMIC_RAY_RIGHT_NOSTRIL", roi_cosmic_ray_right_nostril)

    # ROI 23: Cosmic ray deep (tighten around (11.25, 9.0))
    def roi_cosmic_ray_right_nostril_deep(x, y):
        return (x >= 10.75 and x <= 11.75) and (y >= 8.5 and y <= 9.5)

    scan_roi("COSMIC_RAY_RIGHT_NOSTRIL_DEEP", roi_cosmic_ray_right_nostril_deep)

    # ROI 24: GABA-C (rho) bilateral peri-ocular band (retina/eye region proxy)
    # Left eye band
    def roi_gaba_c_left_eye(x, y):
        return (x >= center_x - 4.0 and x <= center_x - 1.0) and (y >= 9.0 and y <= 12.5)

    # Right eye band
    def roi_gaba_c_right_eye(x, y):
        return (x >= center_x + 1.0 and x <= center_x + 4.0) and (y >= 9.0 and y <= 12.5)

    scan_roi("GABA_C_LEFT_EYE", roi_gaba_c_left_eye)
    scan_roi("GABA_C_RIGHT_EYE", roi_gaba_c_right_eye)

    Path("FACE_ROI_SCAN_REPORT.json").write_text(json.dumps(roi_results, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
