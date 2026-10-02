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


def fit_basis(y: np.ndarray, cols: list[np.ndarray], names: list[str]) -> dict[str, object]:
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


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    y_all = moving_average(load_series(), window=window)
    gate, x_all, ycoord_all, z_all = post_gate_coords(len(y_all), delta=delta)

    y = y_all[gate]
    x = x_all[gate]
    yc = ycoord_all[gate]
    z = z_all[gate]

    models: list[dict[str, object]] = []

    models.append(
        {"name": "axial_quadratic", **fit_basis(y, [np.ones_like(y), z, z * z], ["bias", "z", "z2"])}
    )
    models.append(
        {
            "name": "quadratic_surface",
            **fit_basis(
                y,
                [np.ones_like(y), x, yc, z, x * z, yc * z, z * z],
                ["bias", "x", "y", "z", "xz", "yz", "z2"],
            ),
        }
    )
    models.append(
        {
            "name": "full_quadratic",
            **fit_basis(
                y,
                [np.ones_like(y), x, yc, z, x * yc, x * z, yc * z, x * x, yc * yc, z * z],
                ["bias", "x", "y", "z", "xy", "xz", "yz", "x2", "y2", "z2"],
            ),
        }
    )
    models.append(
        {
            "name": "cubic_mixed",
            **fit_basis(
                y,
                [np.ones_like(y), x, yc, z, x * z, yc * z, z * z, x * yc * z, x * z * z, yc * z * z],
                ["bias", "x", "y", "z", "xz", "yz", "z2", "xyz", "xz2", "yz2"],
            ),
        }
    )

    models.sort(key=lambda row: row["explained_fraction"], reverse=True)
    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "window": int(window),
        "delta": delta,
        "n_points_total": int(len(y_all)),
        "n_points_post_gate": int(len(y)),
        "gate_fraction_on": float(np.mean(gate)),
        "best_model": models[0],
        "models": models,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Post-Gate Surface Fit",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- delta: `{report['delta']}`",
        f"- n_points_total: `{report['n_points_total']}`",
        f"- n_points_post_gate: `{report['n_points_post_gate']}`",
        f"- gate_fraction_on: `{report['gate_fraction_on']}`",
        "",
        "## Best Model",
        f"- name: `{report['best_model']['name']}`",
        f"- explained_fraction: `{report['best_model']['explained_fraction']}`",
        f"- rmse: `{report['best_model']['rmse']}`",
        "",
        "## Ranking",
    ]
    for row in report["models"]:
        lines.append(
            f"- `{row['name']}`: explained=`{row['explained_fraction']}`, rmse=`{row['rmse']}`"
        )
    lines.extend(["", "## Best Coefficients"])
    for row in report["best_model"]["top_coefficients"]:
        lines.append(f"- `{row['name']}` = `{row['coef']}`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit the post-0.2828 energy-on geometry only.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/post_gate_surface_fit.json")
    parser.add_argument("--out-md", default="analysis_results/post_gate_surface_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"best_model={report['best_model']['name']}")
    print(f"best_explained={report['best_model']['explained_fraction']}")
    print(f"best_rmse={report['best_model']['rmse']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
