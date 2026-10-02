from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)


def load_series() -> np.ndarray:
    values: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["k_eff"]))
            except (TypeError, ValueError):
                continue
    x = np.asarray(values, dtype=float)
    return (x - np.mean(x)) / (np.std(x) + 1.0e-12)


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(x, kernel, mode="same")


def post_gate_coords(n: int, delta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    t = np.arange(n, dtype=float)
    fill = t / max(n - 1, 1)
    gate = fill >= delta
    post = np.clip((fill - delta) / max(1.0 - delta, 1.0e-12), 0.0, 1.0)
    theta = 2.0 * math.pi * np.power(post, 1.0 - delta)
    x = np.cos(theta)
    y = np.sin(theta)
    z = delta * post
    return gate, x, y, z


def fit_model(y: np.ndarray, cols: list[np.ndarray], names: list[str]) -> dict[str, object]:
    X = np.column_stack(cols)
    coeffs = np.linalg.pinv(X) @ y
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    order = np.argsort(np.abs(coeffs))[::-1]
    return {
        "basis": names,
        "coefficients": {names[i]: float(coeffs[i]) for i in range(len(names))},
        "top_coefficients": [{"name": names[int(i)], "coef": float(coeffs[int(i)])} for i in order[:8]],
        "rmse": rmse,
        "explained_fraction": explained,
    }


def normalize_columns(H: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = np.mean(H, axis=0)
    std = np.std(H, axis=0) + 1.0e-12
    return (H - mean) / std, mean, std


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    y_all = moving_average(load_series(), window=window)
    gate, x_all, y_all_coords, z_all = post_gate_coords(len(y_all), delta=delta)

    y = y_all[gate]
    x = x_all[gate]
    yc = y_all_coords[gate]
    z = z_all[gate]

    base_cols = [np.ones_like(y), x, yc, z, x * yc, x * z, yc * z, x * x, yc * yc, z * z]
    base_names = ["bias", "x", "y", "z", "xy", "xz", "yz", "x2", "y2", "z2"]
    base_fit = fit_model(y, base_cols, base_names)

    hidden_cols = np.column_stack([x * yc * z, x * z * z, yc * z * z])
    hidden_names = ["xyz", "xz2", "yz2"]
    Hn, _, _ = normalize_columns(hidden_cols)
    _, svals, vt = np.linalg.svd(Hn, full_matrices=False)
    pc1 = vt[0]
    w = Hn @ pc1

    fit_4d = fit_model(y, base_cols + [w], base_names + ["w"])
    fit_cubic_ref = fit_model(y, base_cols + [hidden_cols[:, 0], hidden_cols[:, 1], hidden_cols[:, 2]], base_names + hidden_names)

    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "window": int(window),
        "delta": delta,
        "n_points_total": int(len(y_all)),
        "n_points_post_gate": int(len(y)),
        "gate_fraction_on": float(np.mean(gate)),
        "latent_w": {
            "source_terms": hidden_names,
            "loadings": {hidden_names[i]: float(pc1[i]) for i in range(len(hidden_names))},
            "singular_values": [float(v) for v in svals.tolist()],
            "pc1_energy_fraction": float((svals[0] ** 2) / max(np.sum(svals ** 2), 1.0e-12)),
        },
        "fits": {
            "base_3d_quadratic": base_fit,
            "latent_4d_w": fit_4d,
            "reference_cubic_terms": fit_cubic_ref,
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    latent = report["latent_w"]
    fits = report["fits"]
    lines = [
        "# Post-Gate 4D Axis Fit",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- delta: `{report['delta']}`",
        f"- n_points_total: `{report['n_points_total']}`",
        f"- n_points_post_gate: `{report['n_points_post_gate']}`",
        f"- gate_fraction_on: `{report['gate_fraction_on']}`",
        "",
        "## Latent W",
        f"- pc1_energy_fraction: `{latent['pc1_energy_fraction']}`",
        f"- xyz loading: `{latent['loadings']['xyz']}`",
        f"- xz2 loading: `{latent['loadings']['xz2']}`",
        f"- yz2 loading: `{latent['loadings']['yz2']}`",
        "",
        "## Fit Comparison",
        f"- base_3d_quadratic explained: `{fits['base_3d_quadratic']['explained_fraction']}`",
        f"- latent_4d_w explained: `{fits['latent_4d_w']['explained_fraction']}`",
        f"- reference_cubic_terms explained: `{fits['reference_cubic_terms']['explained_fraction']}`",
        f"- base_3d_quadratic rmse: `{fits['base_3d_quadratic']['rmse']}`",
        f"- latent_4d_w rmse: `{fits['latent_4d_w']['rmse']}`",
        f"- reference_cubic_terms rmse: `{fits['reference_cubic_terms']['rmse']}`",
        "",
        "## Latent 4D Top Coefficients",
    ]
    for row in fits["latent_4d_w"]["top_coefficients"]:
        lines.append(f"- `{row['name']}` = `{row['coef']}`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collapse post-gate cubic terms into one latent 4D axis w.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/post_gate_4d_axis_fit.json")
    parser.add_argument("--out-md", default="analysis_results/post_gate_4d_axis_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"pc1_energy_fraction={report['latent_w']['pc1_energy_fraction']}")
    print(f"base_explained={report['fits']['base_3d_quadratic']['explained_fraction']}")
    print(f"latent_explained={report['fits']['latent_4d_w']['explained_fraction']}")
    print(f"cubic_explained={report['fits']['reference_cubic_terms']['explained_fraction']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
