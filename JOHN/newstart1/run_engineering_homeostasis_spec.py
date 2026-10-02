from __future__ import annotations

from pathlib import Path

import numpy as np

from geometry_package.engineering_homeostasis_equation import (
    TERM_ORDER_15,
    EngineeringHomeostasisSpec,
    control_step,
    engineering_equation_string,
    linear_trajectory_128,
)


OUT_DIR = Path(r"d:\Users\user\Documents\newstart\analysis_results")
OUT_MD = OUT_DIR / "engineering_homeostasis_spec.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = EngineeringHomeostasisSpec()

    # Deterministic seed: equal terms with slight asymmetry
    t0 = np.linspace(0.35, 0.55, 15, dtype=float)
    step = control_step(t0, dt=1.0, spec=p)

    # 128-agent linear trajectory demo
    x0 = np.zeros(128, dtype=float)
    A = 0.98 * np.eye(128, dtype=float)
    B = np.ones(128, dtype=float) / 128.0
    residuals = np.full(10, float(step["residual"]), dtype=float)
    traj = linear_trajectory_128(x0, steps=10, A=A, B=B, residual_series=residuals)

    lines = [
        "# Engineering Homeostasis Spec",
        "",
        f"- equation: `{engineering_equation_string()}`",
        f"- target(H): `{p.homeostasis_target}`",
        f"- tolerance: `{p.closure_tolerance}`",
        f"- control_gain(K): `{p.control_gain}`",
        "",
        "## 15 Terms",
    ]
    for i, name in enumerate(TERM_ORDER_15, start=1):
        lines.append(f"- `{i}. {name}`")
    lines += [
        "",
        "## One Control Step",
        f"- omega_in: `{float(np.sum(t0))}`",
        f"- residual_in(H-omega): `{step['residual']}`",
        f"- omega_out: `{step['omega_out']}`",
        "",
        "## 128 Linear Trajectory Demo",
        f"- steps: `10`",
        f"- x0_norm: `{float(np.linalg.norm(traj[0]))}`",
        f"- x10_norm: `{float(np.linalg.norm(traj[-1]))}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

