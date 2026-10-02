from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v
from fusion_clean import sovereign_dynamics_step


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\sovereign_dynamics_validation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\sovereign_dynamics_validation.md")


def explained_fraction(y_true: np.ndarray, y_hat: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_hat = np.asarray(y_hat, dtype=float)
    num = float(np.mean((y_true - y_hat) ** 2))
    den = float(np.var(y_true) + 1.0e-12)
    return float(1.0 - num / den)


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd

    states = v.causal_state_embed(y)

    n = states.shape[0]
    preds = np.zeros_like(states[:-1])
    conscious = np.zeros(n - 1, dtype=float)
    phase_gate = np.zeros(n - 1, dtype=float)
    spark = np.zeros(n - 1, dtype=float)
    is_tunnel = np.zeros(n - 1, dtype=float)

    for i in range(n - 1):
        fill = float(i / max(n - 2, 1))
        minute = int((i % 96) * 15)
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        step = sovereign_dynamics_step(states[i], phase_fill=fill, clock_hhmm=clock, dt=1.0)
        preds[i] = np.asarray(step["state_next"], dtype=float)
        conscious[i] = float(step["conscious_ratio"])
        phase_gate[i] = float(step["phase_gate"])
        spark[i] = float(step["spark"])
        base = step["base"] or {}
        is_tunnel[i] = float(base.get("is_tunnel", 0.0))

    true_next = np.asarray(states[1:], dtype=float)
    err = true_next - preds

    overall = explained_fraction(true_next.reshape(-1), preds.reshape(-1))
    per_dim = [explained_fraction(true_next[:, j], preds[:, j]) for j in range(true_next.shape[1])]

    # Day vs hysteresis-window split.
    mask_t = is_tunnel >= 0.5
    mask_d = ~mask_t
    day_score = explained_fraction(true_next[mask_d].reshape(-1), preds[mask_d].reshape(-1)) if np.any(mask_d) else float("nan")
    night_score = explained_fraction(true_next[mask_t].reshape(-1), preds[mask_t].reshape(-1)) if np.any(mask_t) else float("nan")

    # Worst residual timestamps (by L2 norm).
    norms = np.linalg.norm(err, axis=1)
    worst_idx = np.argsort(norms)[-10:][::-1].tolist()
    worst = []
    for i in worst_idx:
        minute = int((i % 96) * 15)
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        worst.append(
            {
                "i": int(i),
                "clock": clock,
                "is_tunnel": float(is_tunnel[i]),
                "err_norm": float(norms[i]),
                "true_next": true_next[i].tolist(),
                "pred_next": preds[i].tolist(),
            }
        )

    payload = {
        "overall_explained": float(overall),
        "per_dim_explained": [float(x) for x in per_dim],
        "day_explained": float(day_score),
        "night_explained": float(night_score),
        "worst": worst,
        "stats": {
            "mean_conscious_ratio": float(np.mean(conscious)),
            "mean_phase_gate": float(np.mean(phase_gate)),
            "mean_spark": float(np.mean(spark)),
        },
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Sovereign Dynamics Validation",
        "",
        f"- overall_explained (state transition): `{payload['overall_explained']}`",
        f"- per_dim_explained (BM,BW,SM,SW): `{payload['per_dim_explained']}`",
        f"- day_explained: `{payload['day_explained']}`",
        f"- night_explained: `{payload['night_explained']}`",
        "",
        "## Worst 10 Steps",
    ]
    for w in worst:
        lines.append(f"- i={w['i']} clock={w['clock']} tunnel={w['is_tunnel']} err_norm={w['err_norm']:.6f}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

