from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

import fusion_core as k8
import sovereign_128 as sov


def _mix_strength(U: np.ndarray) -> float:
    # 0 => identity-like, larger => more off-diagonal mixing
    U = np.asarray(U, dtype=float)
    off = float(np.sum(np.abs(U)) - np.sum(np.abs(np.diag(U))))
    return off


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze (gluon, neutrino, photon) massless-sector mixing per window.")
    ap.add_argument("--age", type=float, default=25.0)
    ap.add_argument("--dt-window", type=float, default=float(sov.SUBSTEPS * sov.DT))
    ap.add_argument("--out", type=str, default="analysis_results/massless_sector_mix_windows.csv")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, float | int | str]] = []
    for w in range(int(sov.N_WINDOWS)):
        ch = sov.get_channels(w)
        wts = sov.apply_channels(ch, age=float(args.age))
        L = sov.laplacian(wts)
        Lm = k8.massless_submatrix(L)
        U = k8.massless_mix_matrix(L, dt=float(args.dt_window))
        evals = np.linalg.eigvalsh(Lm)
        evals = np.sort(np.clip(evals, 0.0, None))

        rows.append(
            {
                "w": int(w),
                "time": sov.window_to_hhmm(w),
                "age": float(args.age),
                "dt_window": float(args.dt_window),
                "mix_strength_l1": _mix_strength(U),
                # eigen-spectrum of the restricted generator
                "lambda_0": float(evals[0]),
                "lambda_1": float(evals[1]),
                "lambda_2": float(evals[2]),
                # U entries (order: gluon, neutrino, photon)
                "U_g_g": float(U[0, 0]),
                "U_g_nu": float(U[0, 1]),
                "U_g_ph": float(U[0, 2]),
                "U_nu_g": float(U[1, 0]),
                "U_nu_nu": float(U[1, 1]),
                "U_nu_ph": float(U[1, 2]),
                # photon becomes a mix: ph_next = U_ph_g*g + U_ph_nu*nu + U_ph_ph*ph
                "U_ph_g": float(U[2, 0]),
                "U_ph_nu": float(U[2, 1]),
                "U_ph_ph": float(U[2, 2]),
                # channel states that directly touch the massless edge (neutrino, photon)
                "ch_left_temporalis_5ht1a": str(ch.get("left_temporalis_5ht1a", "no_control")),
                "ch_right_occipitalis_gaba_a": str(ch.get("right_occipitalis_gaba_a", "no_control")),
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

