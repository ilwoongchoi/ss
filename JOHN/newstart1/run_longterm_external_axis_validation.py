from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from fusion_clean import BINDING_IMPEDANCE, ENTROPY_DEBT, OMEGA_TARGET


ROOT = Path(__file__).resolve().parent
SOLAR_PATH = ROOT / "datasets" / "solar" / "raw" / "SN_m_tot_V2.0.txt"
NINA34_PATH = ROOT / "datasets" / "enso" / "raw" / "nina34.data"
SOI_PATH = ROOT / "datasets" / "enso" / "raw" / "soi.data"

OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "exogenous_axis_34y.csv"
OUT_JSON = OUT_DIR / "exogenous_axis_34y_report.json"
OUT_MD = OUT_DIR / "exogenous_axis_34y_report.md"


def load_solar() -> pd.DataFrame:
    df = pd.read_csv(
        SOLAR_PATH,
        sep=r"\s+",
        header=None,
        names=["year", "month", "decimal_year", "sunspot", "std", "n_obs"],
        usecols=[0, 1, 3],
    )
    df["year"] = df["year"].astype(int)
    df["month"] = df["month"].astype(int)
    return df[["year", "month", "sunspot"]]


def load_enso_data(path: Path, value_name: str) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        lines = [line.strip() for line in f if line.strip()]
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 13:
            continue
        year = int(parts[0])
        vals = [float(v) for v in parts[1:13]]
        for month, value in enumerate(vals, start=1):
            rows.append({"year": year, "month": month, value_name: value})
    df = pd.DataFrame(rows)
    df[value_name] = df[value_name].replace(-99.99, np.nan)
    return df


def zscore_train_test(values: np.ndarray, split_idx: int) -> np.ndarray:
    train = values[:split_idx]
    mean = float(np.nanmean(train))
    std = float(np.nanstd(train))
    if std < 1.0e-12:
        std = 1.0
    return (values - mean) / std


def simulate_omega(df: pd.DataFrame) -> pd.DataFrame:
    n = len(df)
    omega = np.zeros(n, dtype=float)
    omega[0] = OMEGA_TARGET
    for idx in range(n - 1):
        exogenous_drive = (
            (1.0 / 128.0) * df.iloc[idx]["solar_z"]
            + (1.0 / 64.0) * df.iloc[idx]["nina34_z"]
            - (1.0 / 256.0) * df.iloc[idx]["soi_z"]
        )
        omega[idx + 1] = (
            omega[idx]
            + BINDING_IMPEDANCE * (OMEGA_TARGET - omega[idx])
            + exogenous_drive
        )
    out = df.copy()
    out["omega_calc"] = omega
    out["omega_error"] = out["omega_calc"] - OMEGA_TARGET
    out["omega_abs_error"] = out["omega_error"].abs()
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    solar = load_solar()
    nina34 = load_enso_data(NINA34_PATH, "nina34")
    soi = load_enso_data(SOI_PATH, "soi")

    merged = solar.merge(nina34, on=["year", "month"], how="inner").merge(soi, on=["year", "month"], how="inner")
    merged = merged.dropna().copy()
    merged["date"] = pd.to_datetime(dict(year=merged["year"], month=merged["month"], day=1))
    merged = merged.sort_values("date").reset_index(drop=True)

    # Last 34 years (408 months), long axis instead of short 2016 slice.
    n_months = 34 * 12
    if len(merged) < n_months:
        raise RuntimeError(f"Not enough merged rows for 34 years: {len(merged)}")
    data = merged.tail(n_months).reset_index(drop=True)

    split_idx = int(0.7 * len(data))
    data["solar_z"] = zscore_train_test(data["sunspot"].to_numpy(dtype=float), split_idx)
    data["nina34_z"] = zscore_train_test(data["nina34"].to_numpy(dtype=float), split_idx)
    data["soi_z"] = zscore_train_test(data["soi"].to_numpy(dtype=float), split_idx)

    sim = simulate_omega(data)
    sim.to_csv(OUT_CSV, index=False)

    train = sim.iloc[:split_idx]
    test = sim.iloc[split_idx:]
    train_mae = float(train["omega_abs_error"].mean())
    test_mae = float(test["omega_abs_error"].mean())
    train_rmse = float(np.sqrt(np.mean(np.square(train["omega_error"]))))
    test_rmse = float(np.sqrt(np.mean(np.square(test["omega_error"]))))

    report = {
        "source_files": {
            "solar": str(SOLAR_PATH),
            "enso_nina34": str(NINA34_PATH),
            "enso_soi": str(SOI_PATH),
        },
        "range_start": sim.iloc[0]["date"].strftime("%Y-%m-%d"),
        "range_end": sim.iloc[-1]["date"].strftime("%Y-%m-%d"),
        "n_months": int(len(sim)),
        "split_index": int(split_idx),
        "constants": {
            "omega_target": OMEGA_TARGET,
            "binding_impedance_1_4": BINDING_IMPEDANCE,
            "entropy_debt_1_64_plus_1_256": ENTROPY_DEBT,
        },
        "metrics": {
            "train_mae": train_mae,
            "test_mae": test_mae,
            "train_rmse": train_rmse,
            "test_rmse": test_rmse,
            "mean_abs_error_full": float(sim["omega_abs_error"].mean()),
            "error_minus_debt_target": float(sim["omega_abs_error"].mean() - ENTROPY_DEBT),
            "omega_min": float(sim["omega_calc"].min()),
            "omega_max": float(sim["omega_calc"].max()),
            "omega_final": float(sim.iloc[-1]["omega_calc"]),
        },
        "outputs": {
            "csv": str(OUT_CSV),
            "json": str(OUT_JSON),
            "md": str(OUT_MD),
        },
    }

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 34Y Exogenous Axis Validation",
        "",
        f"- Range: `{report['range_start']} -> {report['range_end']}`",
        f"- Months: `{report['n_months']}`",
        f"- Split index: `{report['split_index']}`",
        "",
        "## Constants",
        f"- `OMEGA_TARGET = {OMEGA_TARGET}`",
        f"- `Binding = 1/4 = {BINDING_IMPEDANCE}`",
        f"- `Debt(1/64+1/256) = {ENTROPY_DEBT}`",
        "",
        "## Out-of-sample Metrics",
        f"- `train_mae = {train_mae:.6f}`",
        f"- `test_mae = {test_mae:.6f}`",
        f"- `train_rmse = {train_rmse:.6f}`",
        f"- `test_rmse = {test_rmse:.6f}`",
        f"- `mean_abs_error_full = {report['metrics']['mean_abs_error_full']:.6f}`",
        f"- `error_minus_debt_target = {report['metrics']['error_minus_debt_target']:.6f}`",
        "",
        "## Files",
        f"- `{OUT_CSV}`",
        f"- `{OUT_JSON}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
