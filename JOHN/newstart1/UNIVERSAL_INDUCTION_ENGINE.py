from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

import numpy as np
import pandas as pd

from absolute_constants import C, OMEGA, SPARK_CONSTANT_C, SPARK_ANGLE_RAD

try:
    from geometry_package.absolute_constants import (
        OMEGA_PHI as OBSERVER_HORIZON_19860,
        BETTI_7,
        BETTI_11,
        OMEGA_W7,
        OMEGA_H2,
        OMEGA_SLOTTING_DELTA,
        CRUNCH_LIMIT_T,
        D3_CORRECTION_FACTOR,
        NIGHT_HYSTERESIS,
        GABA_C_R_CAB,
        SPARK_ANGLE_DEG,
    )
except Exception:
    OBSERVER_HORIZON_19860 = 1.9860
    BETTI_7 = 7.0
    BETTI_11 = 11.0
    OMEGA_W7 = np.pi / 20.0
    OMEGA_H2 = 1.0 / 9.0
    OMEGA_SLOTTING_DELTA = 0.076
    CRUNCH_LIMIT_T = 18.42
    D3_CORRECTION_FACTOR = 0.5
    NIGHT_HYSTERESIS = 0.8418
    GABA_C_R_CAB = NIGHT_HYSTERESIS / 10.0
    SPARK_ANGLE_DEG = float(np.rad2deg(SPARK_ANGLE_RAD))

EPS = 1.0e-9


def _sigmoid(v: float) -> float:
    return float(1.0 / (1.0 + np.exp(-float(np.clip(v, -50.0, 50.0)))))


def _as_k8(x: Iterable[float] | None) -> np.ndarray:
    if x is None:
        return np.zeros(8, dtype=float)
    arr = np.asarray(list(x), dtype=float).ravel()
    if arr.size < 8:
        arr = np.pad(arr, (0, 8 - arr.size))
    return arr[:8]


@dataclass
class InductionSnapshot:
    step: int
    z_real: float
    z_imag: float
    radius: float
    spark_gate: float
    confinement: float
    electron_stress: float
    d3: float
    inverse_square: float
    proton_membership: float
    omega_proxy: float
    omega_error: float


class UniversalInductionEngine:
    """
    Origin-recursive induction engine.

    This is not a rock-bottom proof.
    It is the first executable bridge from:
        origin recursion -> confinement/electron D3 -> proton membership -> 7.4 error

    It uses:
    - canonical root constants from `absolute_constants.py`
    - observer horizon candidate from `geometry_package.absolute_constants.py` if available
    """

    def __init__(
        self,
        c: float = C,
        spark_c: complex = SPARK_CONSTANT_C,
        observer_horizon: float = OBSERVER_HORIZON_19860,
    ) -> None:
        self.c = float(c)
        self.spark_c = complex(spark_c)
        self.observer_horizon = float(observer_horizon)

    def origin_step(self, z: complex) -> complex:
        return (complex(z) ** 2 + self.spark_c) * (1.0 - self.c)

    def spark_gate(self, z: complex) -> float:
        phase = float(np.angle(z if abs(z) > EPS else self.spark_c))
        return float(0.5 + 0.5 * np.cos(phase - SPARK_ANGLE_RAD))

    def infer_k8_seed(self, z: complex, x_k8: Iterable[float] | None = None) -> np.ndarray:
        amp = float(abs(z))
        phase = float(np.angle(z if abs(z) > EPS else self.spark_c))
        q = amp * abs(np.cos(phase))
        g = amp * abs(np.sin(phase))
        nu = amp * abs(np.cos(phase + self.c))
        ph = amp * abs(np.cos(phase - np.pi / 4.0))
        el = amp * abs(np.sin(phase + np.pi / 4.0))
        hi = self.c * amp
        w = 0.5 * (q + g)
        zb = 0.5 * (nu + el)
        derived = np.array([q, g, nu, ph, el, hi, w, zb], dtype=float)
        x = _as_k8(x_k8)
        if np.linalg.norm(x) <= EPS:
            return derived
        return 0.5 * x + 0.5 * derived

    def confinement(self, x_k8: np.ndarray) -> float:
        q, g = float(x_k8[0]), float(x_k8[1])
        return float(np.clip(q, 0.0, None)) * float(np.clip(g, 0.0, None)) * (1.0 + self.c)

    def electron_stress(self, x_k8: np.ndarray, gate: float) -> float:
        el = float(x_k8[4])
        return float(np.clip(el, 0.0, None)) * (1.0 - float(np.clip(gate, 0.0, 1.0)))

    def d3(self, x_k8: np.ndarray, gate: float) -> tuple[float, float, float]:
        confinement = self.confinement(x_k8)
        electron_stress = self.electron_stress(x_k8, gate)
        d3 = 0.6 * confinement + 0.4 * electron_stress
        return d3, confinement, electron_stress

    def inverse_square(self, z: complex) -> float:
        dz = complex(self.observer_horizon, 0.0) - complex(z)
        return float(1.0 / max(abs(dz) ** 2, EPS))

    def proton_membership(self, x_k8: np.ndarray, gate: float, d3: float) -> float:
        q, g = float(x_k8[0]), float(x_k8[1])
        bw = q + 2.0 * self.c * g
        return _sigmoid(1.25 * gate * (1.0 + d3) * abs(bw) - self.c)

    def omega_proxy(self, x_k8: np.ndarray) -> float:
        return float(np.linalg.norm(np.asarray(x_k8, dtype=float)))

    def snapshot(
        self,
        step: int,
        z: complex,
        x_k8: Iterable[float] | None = None,
    ) -> InductionSnapshot:
        x = self.infer_k8_seed(z, x_k8)
        gate = self.spark_gate(z)
        d3, conf, e_stress = self.d3(x, gate)
        omega_proxy = self.omega_proxy(x)
        return InductionSnapshot(
            step=int(step),
            z_real=float(np.real(z)),
            z_imag=float(np.imag(z)),
            radius=float(abs(z)),
            spark_gate=gate,
            confinement=conf,
            electron_stress=e_stress,
            d3=d3,
            inverse_square=self.inverse_square(z),
            proton_membership=self.proton_membership(x, gate, d3),
            omega_proxy=omega_proxy,
            omega_error=float(omega_proxy - OMEGA),
        )

    def run(
        self,
        steps: int = 128,
        z0: complex = 0j,
        x0: Iterable[float] | None = None,
    ) -> pd.DataFrame:
        z = complex(z0)
        x = self.infer_k8_seed(z, x0)
        rows: list[dict[str, float | int]] = []
        for step in range(int(steps)):
            z = self.origin_step(z)
            snap = self.snapshot(step=step, z=z, x_k8=x)
            rows.append(asdict(snap))
            x = self.infer_k8_seed(z, x)
        return pd.DataFrame(rows)

    def derivation_report(self) -> pd.DataFrame:
        sqrt2 = float(np.sqrt(2.0))
        c_unit_square = sqrt2 / 5.0
        spark_from_claim = float(np.rad2deg(np.arctan(OMEGA_W7 / OMEGA_H2) * (BETTI_11 / BETTI_7)))
        d3_at_crunch = float(OMEGA_SLOTTING_DELTA * CRUNCH_LIMIT_T * BETTI_11)
        deception_delta_at_crunch = float(OMEGA_SLOTTING_DELTA * CRUNCH_LIMIT_T * (BETTI_11 - 1.0))
        electron_scale = 1.0 / 8.0
        electron_d3 = float(electron_scale * self.c * BETTI_11)

        rows = [
            {
                "quantity": "C_from_unit_square",
                "formula": "sqrt(2) / 5",
                "value": c_unit_square,
                "canonical": self.c,
                "abs_error": abs(c_unit_square - self.c),
                "status": "exact_restatement",
            },
            {
                "quantity": "observer_horizon_candidate",
                "formula": "OMEGA_PHI",
                "value": float(OBSERVER_HORIZON_19860),
                "canonical": float(OBSERVER_HORIZON_19860),
                "abs_error": 0.0,
                "status": "geometry_candidate",
            },
            {
                "quantity": "spark_angle_claim_from_betti",
                "formula": "deg(atan(OMEGA_W7 / OMEGA_H2) * (BETTI_11 / BETTI_7))",
                "value": spark_from_claim,
                "canonical": float(SPARK_ANGLE_DEG),
                "abs_error": abs(spark_from_claim - float(SPARK_ANGLE_DEG)),
                "status": "unsupported_if_error_large",
            },
            {
                "quantity": "d3_correction_factor",
                "formula": "KAPPA_H3 / KAPPA_H2",
                "value": float(D3_CORRECTION_FACTOR),
                "canonical": float(D3_CORRECTION_FACTOR),
                "abs_error": 0.0,
                "status": "geometry_candidate",
            },
            {
                "quantity": "d3_at_crunch_candidate",
                "formula": "OMEGA_SLOTTING_DELTA * CRUNCH_LIMIT_T * BETTI_11",
                "value": d3_at_crunch,
                "canonical": np.nan,
                "abs_error": np.nan,
                "status": "candidate_not_canonical",
            },
            {
                "quantity": "deception_delta_at_crunch_candidate",
                "formula": "OMEGA_SLOTTING_DELTA * CRUNCH_LIMIT_T * (BETTI_11 - 1)",
                "value": deception_delta_at_crunch,
                "canonical": np.nan,
                "abs_error": np.nan,
                "status": "candidate_not_canonical",
            },
            {
                "quantity": "electron_d3_candidate",
                "formula": "(1/8) * C * BETTI_11",
                "value": electron_d3,
                "canonical": np.nan,
                "abs_error": np.nan,
                "status": "candidate_not_canonical",
            },
            {
                "quantity": "gaba_mask_candidate",
                "formula": "GABA_C_R_CAB",
                "value": float(GABA_C_R_CAB),
                "canonical": np.nan,
                "abs_error": np.nan,
                "status": "geometry_candidate",
            },
        ]
        return pd.DataFrame(rows)


if __name__ == "__main__":
    engine = UniversalInductionEngine()
    df = engine.run(steps=64)
    out_csv = "UNIVERSAL_INDUCTION_ENGINE_TRACE.csv"
    df.to_csv(out_csv, index=False)
    report = engine.derivation_report()
    report_csv = "ROCK_BOTTOM_DERIVATION_REPORT.csv"
    report.to_csv(report_csv, index=False)
    last = df.iloc[-1]
    print(f"trace: {out_csv}")
    print(f"derivation_report: {report_csv}")
    print(f"final_radius={last['radius']:.6f}")
    print(f"final_d3={last['d3']:.6f}")
    print(f"final_proton_membership={last['proton_membership']:.6f}")
    print(f"final_omega_proxy={last['omega_proxy']:.6f}")
    print(f"final_omega_error={last['omega_error']:.6f}")
