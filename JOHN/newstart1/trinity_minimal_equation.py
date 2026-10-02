from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Trinity:
    """Three-primitives minimal kernel.

    Interpretation (user mapping):
      - quark  (5HT1A)        -> Re(z)
      - gluon  (left D2)      -> Im(z)
      - higgs  (right cortisol) -> constant mass term h (can be slow drift)

    Minimal universe equation (Mandelbrot kernel):
      z_{n+1} = z_n^2 + h
      where z_n = q_n + i g_n
    """

    h: complex


def step(z: complex, trinity: Trinity) -> complex:
    return z * z + trinity.h


def iterate(z0: complex, trinity: Trinity, n: int) -> list[complex]:
    zs: list[complex] = [complex(z0)]
    z = complex(z0)
    for _ in range(int(n)):
        z = step(z, trinity)
        zs.append(z)
    return zs


def observables(z: complex) -> dict[str, float]:
    q = float(z.real)
    g = float(z.imag)
    z2 = z * z
    return {
        "q": q,
        "g": g,
        "radius": float(abs(z)),
        "phase_deg": float(math.degrees(math.atan2(g, q))),
        # Re–Im mixing term produced automatically by the square:
        # Im(z^2) = 2 * Re(z) * Im(z)
        "bridge_re_im": float(z2.imag),
    }


def _write_csv(path: Path, zs: list[complex], trinity: Trinity) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["n", "z_re", "z_im", "h_re", "h_im", "q", "g", "radius", "phase_deg", "bridge_re_im"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for i, z in enumerate(zs):
            obs = observables(z)
            w.writerow(
                {
                    "n": i,
                    "z_re": float(z.real),
                    "z_im": float(z.imag),
                    "h_re": float(trinity.h.real),
                    "h_im": float(trinity.h.imag),
                    **obs,
                }
            )


def main() -> None:
    ap = argparse.ArgumentParser(description="Trinity minimal equation: z_{n+1} = z_n^2 + h")
    ap.add_argument("--q0", type=float, default=0.0, help="Initial quark (Re) value.")
    ap.add_argument("--g0", type=float, default=0.0, help="Initial gluon (Im) value.")
    ap.add_argument("--h-re", type=float, default=0.0, help="Higgs mass term real part.")
    ap.add_argument("--h-im", type=float, default=0.0, help="Higgs mass term imag part (optional).")
    ap.add_argument("--n", type=int, default=256, help="Number of iterations.")
    ap.add_argument("--out", type=str, default="analysis_results/trinity_minimal_equation.csv")
    args = ap.parse_args()

    trinity = Trinity(h=complex(float(args.h_re), float(args.h_im)))
    zs = iterate(complex(float(args.q0), float(args.g0)), trinity, int(args.n))
    _write_csv(Path(args.out), zs, trinity)
    print(str(Path(args.out)))


if __name__ == "__main__":
    main()

