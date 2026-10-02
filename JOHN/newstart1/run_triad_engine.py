from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

import fusion_core as k8

try:
    import sovereign_128 as sov
except Exception:
    sov = None


def _window_to_hhmm_fallback(w: int, n_windows: int) -> str:
    min_per_win = 24 * 60 / float(n_windows)
    total = float(w) * min_per_win
    return f"{int(total // 60):02d}:{int(total % 60):02d}"


def integrate_window(x: np.ndarray, L: np.ndarray, dt: float, substeps: int) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    for _ in range(int(substeps)):
        x = x - float(dt) * (L @ x)
        x = np.clip(x, 1.0e-12, 50.0)
    return x


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Triad-only K8 driver: keep ONLY (left_frontalis_d2, right_cortisol, left_temporalis_5ht1a) "
            "as independent controls and derive the full 8-particle state via Laplacian mixing."
        )
    )
    ap.add_argument("--age", type=float, default=25.0)
    ap.add_argument("--n-windows", type=int, default=128)
    ap.add_argument("--substeps", type=int, default=30)
    ap.add_argument("--dt", type=float, default=0.015)
    ap.add_argument("--out", type=str, default="analysis_results/triad_engine/triad_engine_windows.csv")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    t4_day = k8.day_target()
    x = k8.init_state8_from_target4(t4_day)

    rows: list[dict[str, float | int | str]] = []
    for w in range(int(args.n_windows)):
        # schedule source: reuse sovereign_128 schedule if available; otherwise default "no_control".
        if sov is not None and int(args.n_windows) == int(getattr(sov, "N_WINDOWS", 128)):
            ch_full = sov.get_channels(w)
            time_str = sov.window_to_hhmm(w)
        else:
            ch_full = {}
            time_str = _window_to_hhmm_fallback(w, int(args.n_windows))

        triad = {
            "left_frontalis_d2": str(ch_full.get("left_frontalis_d2", "no_control")),
            "right_cortisol": str(ch_full.get("right_cortisol", "no_control")),
            "left_temporalis_5ht1a": str(ch_full.get("left_temporalis_5ht1a", "no_control")),
        }

        wts = k8.apply_channels(triad, age=float(args.age))
        L = k8.laplacian(wts)
        x = integrate_window(x, L, dt=float(args.dt), substeps=int(args.substeps))

        x4 = k8.project4(x)
        q, g, nu, ph, el, hi, w_b, z_b = map(float, x.tolist())
        bm, bw, sm, sw = map(float, x4.tolist())

        rows.append(
            {
                "w": int(w),
                "time": time_str,
                "age": float(args.age),
                "ch_left_temporalis_5ht1a": triad["left_temporalis_5ht1a"],
                "ch_left_frontalis_d2": triad["left_frontalis_d2"],
                "ch_right_cortisol": triad["right_cortisol"],
                "q": q,
                "g": g,
                "nu": nu,
                "ph": ph,
                "el": el,
                "higgs": hi,
                "w_boson": w_b,
                "z_boson": z_b,
                "BM": bm,
                "BW": bw,
                "SM": sm,
                "SW": sw,
                "omega4": float(np.linalg.norm(x4)),
                "omega8": float(np.linalg.norm(x)),
                # expose the two triad-controlled hinge edges
                "w_nu_photon": float(wts.get(("neutrino", "photon"), 0.0)),
                "w_photon_w": float(wts.get(("photon", "w_boson"), 0.0)),
            }
        )

    fieldnames = list(rows[0].keys()) if rows else []
    with out_path.open("w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=fieldnames)
        wcsv.writeheader()
        wcsv.writerows(rows)

    print(str(out_path))


if __name__ == "__main__":
    main()

