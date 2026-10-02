"""Minimal smoke-test / demo for the canonical engine.

Run:
    python -m canonical_engine.simulate
"""
from __future__ import annotations

import numpy as np

from .fusion_clean import CanonicalEngine
from .fusion_core import RAW_COUNT


def main() -> None:
    rng = np.random.default_rng(42)

    engine = CanonicalEngine()

    X24 = rng.uniform(-0.1, 0.1, size=24)
    r8 = np.zeros(8)

    n_steps = 20
    for t in range(n_steps):
        c24 = rng.uniform(0.0, 1.0, size=RAW_COUNT)
        # exogenous risk scalar: small most of the time, spike occasionally
        d_risk = 0.8 if t == 10 else 0.05

        nor = rng.uniform(0.0, 0.1)
        plp = rng.uniform(0.0, 0.1)

        X24, r8, diag = engine.step(X24, r8, c24, d_risk, nor=nor, plp=plp, dt=0.1)

        print(
            f"t={t:02d} gate={diag['gate']:.4f} d_risk={diag['d_risk']:.3f} "
            f"|X|={np.linalg.norm(X24):.4f} |r|={np.linalg.norm(r8):.4f} "
            f"rebranched={[p for p, v in diag['rebranch_flags'].items() if v]}"
        )


if __name__ == "__main__":
    main()
