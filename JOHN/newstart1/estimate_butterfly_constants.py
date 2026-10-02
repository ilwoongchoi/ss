from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


TRAJ_PATH = Path("analysis_results/current_trajectory_128.csv")
ERA5_PATH = Path("datasets/era5/processed/era5_t2m_d2m_tcc_201603-05.nc")
COSMO_PATH = Path("PI_GLOBAL_POINT_CLOUD_COSMOLOGY.csv")
OUT_JSON = Path("BUTTERFLY_CONSTANTS_REPORT.json")
OUT_CSV = Path("BUTTERFLY_ALIGNED_SERIES.csv")

HYSTERESIS_LAG = 20  # 5/32 of 128


def load_trajectory_stress() -> np.ndarray:
    trajectory = pd.read_csv(TRAJ_PATH)
    if "closure_err" in trajectory.columns and "spark" in trajectory.columns:
        stress = trajectory["closure_err"].to_numpy(dtype=float) + 0.15 * np.abs(
            trajectory["spark"].to_numpy(dtype=float)
        )
    else:
        numeric = trajectory.select_dtypes(include=[np.number])
        stress = np.nanmean(numeric.to_numpy(dtype=float), axis=1)
    stress = (stress - np.nanmean(stress)) / (np.nanstd(stress) + 1e-9)
    return stress


def load_climate_proxy() -> pd.DataFrame:
    dataset = xr.open_dataset(ERA5_PATH)
    # wind(u10/v10)가 없는 파일이라, 공간구배 기반 flow proxy를 사용
    t2m = dataset["t2m"]
    d2m = dataset["d2m"]
    tcc = dataset["tcc"]

    t2m_values = np.asarray(t2m.values, dtype=float)
    d2m_values = np.asarray(d2m.values, dtype=float)
    tcc_values = np.asarray(tcc.values, dtype=float)

    grad_lat, grad_lon = np.gradient(t2m_values, axis=(1, 2))
    flow_proxy = np.sqrt(grad_lat**2 + grad_lon**2).mean(axis=(1, 2))
    humidity_gap = np.abs(t2m_values - d2m_values).mean(axis=(1, 2))
    cloud = tcc_values.mean(axis=(1, 2))

    frame = pd.DataFrame(
        {
            "time": pd.to_datetime(dataset["valid_time"].values),
            "flow_proxy": flow_proxy,
            "humidity_gap": humidity_gap,
            "cloud": cloud,
        }
    )
    for col in ("flow_proxy", "humidity_gap", "cloud"):
        values = frame[col].to_numpy(dtype=float)
        frame[col] = (values - values.mean()) / (values.std() + 1e-9)
    return frame


def load_cosmo_scalar() -> float:
    cosmos = pd.read_csv(COSMO_PATH)
    numeric = cosmos.select_dtypes(include=[np.number])
    if numeric.empty:
        return 0.0
    values = numeric.to_numpy(dtype=float)
    return float(np.nanmean(values))


def align_series(climate: pd.DataFrame, stress_cycle: np.ndarray) -> pd.DataFrame:
    count = len(climate)
    idx = np.arange(count) % len(stress_cycle)
    stress = stress_cycle[idx]
    lag_idx = (idx - HYSTERESIS_LAG) % len(stress_cycle)
    stress_lag = stress_cycle[lag_idx]
    out = climate.copy()
    out["stress"] = stress
    out["stress_lag20"] = stress_lag
    return out


def fit_constants(frame: pd.DataFrame, cosmo_scalar: float) -> dict:
    y = frame["flow_proxy"].to_numpy(dtype=float)
    y_lag = np.roll(y, 1)
    y_lag[0] = y_lag[1]
    s0 = frame["stress"].to_numpy(dtype=float)
    s20 = frame["stress_lag20"].to_numpy(dtype=float)
    h = frame["humidity_gap"].to_numpy(dtype=float)
    c = frame["cloud"].to_numpy(dtype=float)
    interaction = s0 * cosmo_scalar

    X = np.column_stack(
        [
            np.ones_like(y),
            y_lag,
            s0,
            s20,
            interaction,
            h,
            c,
        ]
    )
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    y_hat = X @ beta
    residual = y - y_hat
    r2 = 1.0 - (np.sum(residual**2) / (np.sum((y - y.mean()) ** 2) + 1e-9))

    names = [
        "bias",
        "alpha_autoregressive",
        "beta_stress_direct",
        "beta_stress_hysteresis_lag20",
        "gamma_stress_cosmo_interaction",
        "eta_humidity_gap",
        "zeta_cloud",
    ]
    coeffs = {k: float(v) for k, v in zip(names, beta)}
    return {
        "coefficients": coeffs,
        "r2": float(r2),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "n_samples": int(len(y)),
    }


def main() -> None:
    stress_cycle = load_trajectory_stress()
    climate = load_climate_proxy()
    cosmo_scalar = load_cosmo_scalar()
    aligned = align_series(climate, stress_cycle)
    metrics = fit_constants(aligned, cosmo_scalar)

    aligned.to_csv(OUT_CSV, index=False)
    report = {
        "data_window": {
            "climate_start": str(aligned["time"].min()),
            "climate_end": str(aligned["time"].max()),
            "n_hours": int(len(aligned)),
        },
        "hysteresis_lag_5_32_of_128": HYSTERESIS_LAG,
        "cosmo_scalar_mean": cosmo_scalar,
        "model": "flow_proxy_t = a*flow_proxy_{t-1} + b0*stress_t + b20*stress_{t-20} + g*(stress_t*cosmo) + e1*humidity + e2*cloud",
        "fit": metrics,
        "limitations": [
            "current ERA5 file has no u10/v10 wind; used gradient-based flow_proxy",
            "current local ERA5 window is 2016-03 to 2016-05, not full 34 years",
            "causal claim requires out-of-sample and confound controls",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
