from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


ERA5_T2M = Path("datasets/era5/processed/era5_t2m_d2m_tcc_201603-05.nc")
ERA5_STRD_GLOB = Path("datasets/era5/raw/single_levels/stepType=accum/data_stream-oper_stepType-accum_STRD_2016*.nc")
OUT_SERIES = Path("LATENT_TIMELINE_INFERRED.csv")
OUT_CONST = Path("LATENT_CONSTANTS_INFERRED.json")
N_PHASE = 128
LAG = 20  # 5/32 * 128


def build_climate_signal() -> pd.DataFrame:
    ds = xr.open_dataset(ERA5_T2M)
    t2m = np.asarray(ds["t2m"].values, dtype=float)
    d2m = np.asarray(ds["d2m"].values, dtype=float)
    tcc = np.asarray(ds["tcc"].values, dtype=float)
    grad_lat, grad_lon = np.gradient(t2m, axis=(1, 2))
    flow = np.sqrt(grad_lat**2 + grad_lon**2).mean(axis=(1, 2))
    humidity = np.abs(t2m - d2m).mean(axis=(1, 2))
    cloud = tcc.mean(axis=(1, 2))

    frame = pd.DataFrame(
        {
            "time": pd.to_datetime(ds["valid_time"].values),
            "flow": flow,
            "humidity": humidity,
            "cloud": cloud,
        }
    )
    for col in ("flow", "humidity", "cloud"):
        values = frame[col].to_numpy(dtype=float)
        frame[col] = (values - values.mean()) / (values.std() + 1e-9)
    return frame


def periodic_basis(n: int, period: int) -> np.ndarray:
    t = np.arange(n, dtype=float)
    cols = [np.ones(n)]
    for k in range(1, 9):
        cols.append(np.sin(2.0 * np.pi * k * t / period))
        cols.append(np.cos(2.0 * np.pi * k * t / period))
    return np.column_stack(cols)


def infer_latent(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    y = frame["flow"].to_numpy(dtype=float)
    n = len(y)
    B = periodic_basis(n, N_PHASE)
    y_lag1 = np.roll(y, 1)
    y_lag1[0] = y_lag1[1]
    y_lag20 = np.roll(y, LAG)
    y_lag20[:LAG] = y_lag20[LAG]
    h = frame["humidity"].to_numpy(dtype=float)
    c = frame["cloud"].to_numpy(dtype=float)

    # joint model: y_t = a y_{t-1} + b y_{t-20} + d1 h + d2 c + g^T B_t
    X = np.column_stack([y_lag1, y_lag20, h, c, B])
    lam = 1e-2
    XtX = X.T @ X + lam * np.eye(X.shape[1])
    beta = np.linalg.solve(XtX, X.T @ y)
    y_hat = X @ beta
    residual = y - y_hat
    r2 = 1.0 - (np.sum(residual**2) / (np.sum((y - y.mean()) ** 2) + 1e-9))

    latent = B @ beta[4:]
    latent = (latent - latent.mean()) / (latent.std() + 1e-9)

    out = frame.copy()
    out["flow_hat"] = y_hat
    out["latent_inferred"] = latent
    out["residual"] = residual

    metrics = {
        "model": "flow_t = a*flow_{t-1} + b*flow_{t-20} + d1*humidity + d2*cloud + periodic128_latent",
        "lag_5_32_of_128": LAG,
        "coefficients": {
            "alpha_lag1": float(beta[0]),
            "beta_lag20": float(beta[1]),
            "delta_humidity": float(beta[2]),
            "delta_cloud": float(beta[3]),
        },
        "r2": float(r2),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "n_samples": int(n),
    }
    return out, metrics


def main() -> None:
    frame = build_climate_signal()
    out, metrics = infer_latent(frame)
    out.to_csv(OUT_SERIES, index=False)
    with open(OUT_CONST, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"Wrote {OUT_SERIES}")
    print(f"Wrote {OUT_CONST}")


if __name__ == "__main__":
    main()
