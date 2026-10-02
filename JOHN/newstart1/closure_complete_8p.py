from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd

from engineering_homeostasis_24 import CHANNELS_24


N_WIN = 128
DT = 1.0
OMEGA = 7.4
LAG_5_32 = int(N_WIN * 5 / 32)
STATE8 = ["quark", "electron", "neutrino", "gluon", "photon", "muon", "tau", "neutron"]


@dataclass
class Closure8P:
    L: np.ndarray
    U: np.ndarray
    G: np.ndarray
    rho: float
    W_h: np.ndarray
    a_p: np.ndarray
    a_h: np.ndarray
    b_p: float
    b_h: float
    c_p: float
    c_h: float
    v: float


def build_model() -> Closure8P:
    n = len(STATE8)
    lap = np.zeros((n, n), dtype=float)
    for i in range(n):
        lap[i, i] = 2.0
        lap[i, (i - 1) % n] = -1.0
        lap[i, (i + 1) % n] = -1.0
    L = 0.12 * lap + 0.05 * np.eye(n)

    U = np.zeros((n, len(CHANNELS_24)), dtype=float)
    for j in range(len(CHANNELS_24)):
        U[j % n, j] = 0.85
        U[(j + 3) % n, j] = 0.25
        U[(j + 5) % n, j] = 0.12

    G = 0.08 * np.eye(n)
    rho = 0.72
    W_h = 0.14 * np.eye(n)

    a_p = np.array([0.35, 0.04, 0.28, 0.22, 0.06, 0.02, 0.01, 0.30], dtype=float)
    a_h = np.array([0.04, 0.08, 0.10, 0.03, 0.42, 0.15, 0.14, 0.04], dtype=float)
    b_p = 0.18
    b_h = 0.16
    c_p = 1.0
    c_h = 1.0
    v = 1.0
    return Closure8P(L=L, U=U, G=G, rho=rho, W_h=W_h, a_p=a_p, a_h=a_h, b_p=b_p, b_h=b_h, c_p=c_p, c_h=c_h, v=v)


def build_target_orbit() -> np.ndarray:
    n = len(STATE8)
    orbit = np.zeros((N_WIN, n), dtype=float)
    base = OMEGA / np.sqrt(n)
    for k in range(N_WIN):
        ang = 2.0 * np.pi * k / N_WIN
        orbit[k, 0] = base + 0.22 * np.sin(ang)
        orbit[k, 1] = base + 0.16 * np.cos(ang + 0.30)
        orbit[k, 2] = base + 0.20 * np.sin(ang - 0.15)
        orbit[k, 3] = base + 0.18 * np.cos(ang + 0.50)
        orbit[k, 4] = base + 0.14 * np.sin(2.0 * ang)
        orbit[k, 5] = base + 0.08 * np.cos(2.0 * ang + 0.20)
        orbit[k, 6] = base + 0.06 * np.sin(3.0 * ang - 0.40)
        orbit[k, 7] = base + 0.21 * np.cos(ang - 0.25)
    return orbit


def hysteresis_field(model: Closure8P, x_star: np.ndarray) -> np.ndarray:
    n = x_star.shape[1]
    H = np.zeros((N_WIN, n), dtype=float)
    for k in range(N_WIN):
        prev = H[k - 1] if k > 0 else H[-1]
        lagged = x_star[(k - LAG_5_32) % N_WIN]
        H[k] = model.rho * prev + model.W_h @ lagged
    return H


def latent_proton_higgs(model: Closure8P, x: np.ndarray, H: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p_hat = x @ model.a_p + model.b_p * np.linalg.norm(H, axis=1)
    h_hat = x @ model.a_h + model.b_h * np.linalg.norm(H, axis=1)
    return p_hat, h_hat


def solve_controls(model: Closure8P, x_star: np.ndarray, H: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p_hat, h_hat = latent_proton_higgs(model, x_star, H)
    spark = model.c_p * p_hat + model.c_h * h_hat
    omega_calc = np.linalg.norm(x_star, axis=1)
    residual = omega_calc - OMEGA
    u = np.zeros((N_WIN, len(CHANNELS_24)), dtype=float)
    U_pinv = np.linalg.pinv(model.U)
    for k in range(N_WIN):
        xk = x_star[k]
        xk1 = x_star[(k + 1) % N_WIN]
        desired_dx = (xk1 - xk) / DT
        rhs = desired_dx + model.L @ xk - model.G @ H[k] + model.v * residual[k] * np.ones_like(xk)
        u[k] = U_pinv @ rhs
    return u, spark, residual, omega_calc


def simulate(model: Closure8P, x0: np.ndarray, H: np.ndarray, u: np.ndarray, residual: np.ndarray) -> np.ndarray:
    x = np.zeros((N_WIN + 1, len(STATE8)), dtype=float)
    x[0] = x0
    for k in range(N_WIN):
        dx = -model.L @ x[k] + model.U @ u[k] + model.G @ H[k] - model.v * residual[k] * np.ones(len(STATE8))
        x[k + 1] = x[k] + DT * dx
    return x


def node_states(u_row: np.ndarray) -> list[str]:
    z = (u_row - np.mean(u_row)) / (np.std(u_row) + 1e-9)
    states: list[str] = []
    for val in z:
        if val >= 0.35:
            states.append("on")
        elif val <= -0.35:
            states.append("off")
        else:
            states.append("idle")
    return states


def export_outputs(
    x_star: np.ndarray,
    H: np.ndarray,
    u: np.ndarray,
    spark: np.ndarray,
    residual: np.ndarray,
    omega_calc: np.ndarray,
    x_sim: np.ndarray,
) -> None:
    periodic_error = float(np.linalg.norm(x_sim[-1] - x_sim[0]))
    tracking_error = float(np.linalg.norm(x_sim[:-1] - x_star) / N_WIN)
    max_residual = float(np.max(np.abs(residual)))
    residual_target = (1.0 / 64.0) + (1.0 / 256.0)
    residual_mean_abs = float(np.mean(np.abs(residual)))
    residual_target_delta = float(residual_mean_abs - residual_target)

    records: list[dict] = []
    for k in range(N_WIN):
        row = {
            "window": k,
            "hour": 24.0 * k / N_WIN,
            "spark": float(spark[k]),
            "residual": float(residual[k]),
            "omega_calc": float(omega_calc[k]),
            "hysteresis_norm": float(np.linalg.norm(H[k])),
        }
        for idx, s in enumerate(STATE8):
            row[f"x_{s}"] = float(x_star[k, idx])
            row[f"u_{CHANNELS_24[idx]}"] = float(u[k, idx])
        states = node_states(u[k])
        for channel_name, state in zip(CHANNELS_24, states):
            row[f"state_{channel_name}"] = state
        records.append(row)
    pd.DataFrame(records).to_csv("CLOSURE_8P_128_SCHEDULE.csv", index=False)

    metrics = {
        "equation": "x_{k+1}=x_k+dt[-Lx_k+Uu_k+G H_k-v r_k], H_k=rho H_{k-1}+W_h x_{k-20}, r_k=||x_k||-7.4",
        "lag_5_32_in_128": LAG_5_32,
        "periodic_error_l2": periodic_error,
        "tracking_error_l2_per_window": tracking_error,
        "max_abs_residual": max_residual,
        "residual_mean_abs": residual_mean_abs,
        "residual_target_1_64_plus_1_256": residual_target,
        "residual_target_delta": residual_target_delta,
    }
    with open("CLOSURE_8P_METRICS.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    lines = [
        "# 8-Particle Closure Equation (Proton/Higgs Embedded)",
        "",
        "State: x_k = [quark, electron, neutrino, gluon, photon, muon, tau, neutron]^T",
        f"5/32 over 128 windows = lag {LAG_5_32}",
        "",
        "H_k = rho*H_{k-1} + W_h*x_{k-20}",
        "p_hat = a_p^T x_k + b_p ||H_k||",
        "h_hat = a_h^T x_k + b_h ||H_k||",
        "S_k = c_p p_hat + c_h h_hat",
        "Omega_calc(k) = ||x_k||",
        "Error(k) = Omega_calc(k) - 7.4",
        "x_{k+1} = x_k + dt[-Lx_k + Uu_k + G H_k - v r_k]",
    ]
    with open("CLOSURE_8P_EQUATION.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    model = build_model()
    x_star = build_target_orbit()
    H = hysteresis_field(model, x_star)
    u, spark, residual, omega_calc = solve_controls(model, x_star, H)
    x_sim = simulate(model, x_star[0], H, u, residual)
    export_outputs(x_star, H, u, spark, residual, omega_calc, x_sim)
    print("Wrote CLOSURE_8P_EQUATION.md")
    print("Wrote CLOSURE_8P_128_SCHEDULE.csv")
    print("Wrote CLOSURE_8P_METRICS.json")


if __name__ == "__main__":
    main()
