from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np

from engineering_homeostasis_24 import CHANNELS_24


N_WIN = 128
DT = 1.0
LAG_5_32 = int(N_WIN * 5 / 32)  # 20


@dataclass
class System:
    state_names: list[str]
    L: np.ndarray
    U: np.ndarray
    G: np.ndarray
    W_h: np.ndarray
    rho: float


def build_system(state_names: list[str]) -> System:
    n = len(state_names)
    lap = np.zeros((n, n), dtype=float)
    for i in range(n):
        lap[i, i] = 2.0
        lap[i, (i - 1) % n] = -1.0
        lap[i, (i + 1) % n] = -1.0
    L = 0.11 * lap + 0.04 * np.eye(n)

    U = np.zeros((n, len(CHANNELS_24)), dtype=float)
    for j in range(len(CHANNELS_24)):
        U[j % n, j] = 0.8
        U[(j + 2) % n, j] += 0.2
        U[(j + 5) % n, j] += 0.1

    G = 0.07 * np.eye(n)
    W_h = 0.12 * np.eye(n)
    return System(state_names=state_names, L=L, U=U, G=G, W_h=W_h, rho=0.7)


def build_target_orbit(state_names: list[str]) -> np.ndarray:
    n = len(state_names)
    x = np.zeros((N_WIN, n), dtype=float)
    base = 1.0
    for k in range(N_WIN):
        ang = 2.0 * np.pi * k / N_WIN
        for i in range(n):
            phase = 0.17 * i
            amp = 0.12 + 0.03 * (i % 4)
            x[k, i] = base + amp * np.sin(ang + phase) + 0.04 * np.cos(2 * ang - phase)
    return x


def hysteresis_from_target(sys: System, x_star: np.ndarray) -> np.ndarray:
    n = x_star.shape[1]
    h = np.zeros((N_WIN, n), dtype=float)
    for k in range(N_WIN):
        prev = h[k - 1] if k > 0 else h[-1]
        lagged = x_star[(k - LAG_5_32) % N_WIN]
        h[k] = sys.rho * prev + sys.W_h @ lagged
    return h


def idx_map(names: list[str]) -> dict[str, int]:
    return {name: i for i, name in enumerate(names)}


def latent_ph_embed(x: np.ndarray, h: np.ndarray, names: list[str]) -> tuple[float, float]:
    idx = idx_map(names)
    p_hat = (
        0.34 * x[idx["quark"]]
        + 0.26 * x[idx["neutrino"]]
        + 0.24 * x[idx["neutron"]]
        + 0.10 * x[idx["self"]]
        + 0.12 * np.linalg.norm(h)
    )
    h_hat = (
        0.40 * x[idx["photon"]]
        + 0.20 * x[idx["muon"]]
        + 0.20 * x[idx["tau"]]
        + 0.10 * x[idx["self"]]
        + 0.10 * np.linalg.norm(h)
    )
    return float(p_hat), float(h_hat)


def explicit_ph(x: np.ndarray, names: list[str]) -> tuple[float, float]:
    idx = idx_map(names)
    return float(x[idx["proton"]]), float(x[idx["higgs"]])


def spark_schedule(mode: str, x_star: np.ndarray, h_star: np.ndarray, names: list[str]) -> np.ndarray:
    cp, ch = 1.0, 1.0
    s = np.zeros(N_WIN, dtype=float)
    for k in range(N_WIN):
        if mode == "embed":
            p_hat, h_hat = latent_ph_embed(x_star[k], h_star[k], names)
        else:
            p_hat, h_hat = explicit_ph(x_star[k], names)
        s[k] = cp * p_hat + ch * h_hat
    return s


def solve_u(sys: System, x_star: np.ndarray, h_star: np.ndarray, spark: np.ndarray, mode: str) -> np.ndarray:
    n = x_star.shape[1]
    u = np.zeros((N_WIN, len(CHANNELS_24)), dtype=float)
    u_pinv = np.linalg.pinv(sys.U)
    for k in range(N_WIN):
        xk = x_star[k]
        xk1 = x_star[(k + 1) % N_WIN]
        dx_target = (xk1 - xk) / DT
        if mode == "embed":
            p_hat, h_hat = latent_ph_embed(xk, h_star[k], sys.state_names)
        else:
            p_hat, h_hat = explicit_ph(xk, sys.state_names)
        residual = (p_hat + h_hat) - spark[k]
        rhs = dx_target + sys.L @ xk - sys.G @ h_star[k] + residual * np.ones(n)
        u[k] = u_pinv @ rhs
    return u


def simulate(sys: System, x0: np.ndarray, h_star: np.ndarray, u: np.ndarray, spark: np.ndarray, mode: str) -> tuple[np.ndarray, np.ndarray]:
    n = len(sys.state_names)
    x = np.zeros((N_WIN + 1, n), dtype=float)
    residuals = np.zeros(N_WIN, dtype=float)
    x[0] = x0.copy()
    for k in range(N_WIN):
        if mode == "embed":
            p_hat, h_hat = latent_ph_embed(x[k], h_star[k], sys.state_names)
        else:
            p_hat, h_hat = explicit_ph(x[k], sys.state_names)
        residual = (p_hat + h_hat) - spark[k]
        residuals[k] = residual
        dx = -sys.L @ x[k] + sys.U @ u[k] + sys.G @ h_star[k] - residual * np.ones(n)
        x[k + 1] = x[k] + DT * dx
    return x, residuals


def evaluate_mode(mode: str, seed: int = 0) -> dict:
    if mode == "embed":
        names = ["quark", "electron", "neutrino", "gluon", "photon", "muon", "tau", "neutron", "self"]
    else:
        names = ["quark", "electron", "neutrino", "gluon", "photon", "muon", "tau", "neutron", "proton", "higgs", "self"]
    sys = build_system(names)
    x_star = build_target_orbit(names)
    h_star = hysteresis_from_target(sys, x_star)
    spark = spark_schedule(mode, x_star, h_star, names)
    u = solve_u(sys, x_star, h_star, spark, mode)

    x_nom, r_nom = simulate(sys, x_star[0], h_star, u, spark, mode)
    periodic_nom = float(np.linalg.norm(x_nom[-1] - x_nom[0]))
    track_nom = float(np.linalg.norm(x_nom[:-1] - x_star) / N_WIN)
    max_res_nom = float(np.max(np.abs(r_nom)))

    rng = np.random.default_rng(seed)
    periodic_list = []
    track_list = []
    max_res_list = []
    for _ in range(50):
        x0 = x_star[0] + rng.normal(0.0, 0.10, size=x_star.shape[1])
        x_sim, r_sim = simulate(sys, x0, h_star, u, spark, mode)
        periodic_list.append(float(np.linalg.norm(x_sim[-1] - x_sim[0])))
        track_list.append(float(np.linalg.norm(x_sim[:-1] - x_star) / N_WIN))
        max_res_list.append(float(np.max(np.abs(r_sim))))

    return {
        "mode": mode,
        "n_state": len(names),
        "lag_5_32_in_128": LAG_5_32,
        "nominal": {
            "periodic_error_l2": periodic_nom,
            "tracking_error_l2_per_window": track_nom,
            "max_abs_residual": max_res_nom,
        },
        "perturbed_50": {
            "periodic_error_l2_mean": float(np.mean(periodic_list)),
            "periodic_error_l2_p95": float(np.percentile(periodic_list, 95)),
            "tracking_error_l2_mean": float(np.mean(track_list)),
            "tracking_error_l2_p95": float(np.percentile(track_list, 95)),
            "max_abs_residual_mean": float(np.mean(max_res_list)),
            "max_abs_residual_p95": float(np.percentile(max_res_list, 95)),
        },
    }


def main() -> None:
    embed = evaluate_mode("embed", seed=7)
    retain = evaluate_mode("retain", seed=7)

    score_embed = (
        embed["perturbed_50"]["periodic_error_l2_mean"]
        + embed["perturbed_50"]["tracking_error_l2_mean"]
        + 0.5 * embed["perturbed_50"]["max_abs_residual_mean"]
    )
    score_retain = (
        retain["perturbed_50"]["periodic_error_l2_mean"]
        + retain["perturbed_50"]["tracking_error_l2_mean"]
        + 0.5 * retain["perturbed_50"]["max_abs_residual_mean"]
    )
    recommendation = "retain_proton_higgs_and_add_self" if score_retain <= score_embed else "embed_proton_higgs_and_add_self"

    out = {
        "embed": embed,
        "retain": retain,
        "scores": {
            "embed_total": float(score_embed),
            "retain_total": float(score_retain),
        },
        "recommendation": recommendation,
    }

    with open("SELF_PH_MODEL_COMPARISON.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote SELF_PH_MODEL_COMPARISON.json")
    print("recommendation:", recommendation)


if __name__ == "__main__":
    main()
