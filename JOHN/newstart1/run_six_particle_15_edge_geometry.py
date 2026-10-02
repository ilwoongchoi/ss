from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from geometry_package.six_particle_15_edge_geometry import EDGE_LIST_15, PARTICLES_6, geometry_step_15


OUT_DIR = Path(r"d:\Users\user\Documents\newstart\analysis_results")
OUT_JSON = OUT_DIR / "six_particle_15_edge_geometry.json"
OUT_MD = OUT_DIR / "six_particle_15_edge_geometry.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Example seed state in [quark, gluon, neutrino, photon, proton, electron] order.
    state0 = np.array([0.20, 0.16, 0.12, 0.18, 0.19, 0.15], dtype=float)
    out = geometry_step_15(state0, dt=1.0)

    report = {
        "particles": list(PARTICLES_6),
        "edge_count": len(EDGE_LIST_15),
        "edge_keys": [e.key for e in EDGE_LIST_15],
        "state_in": out["state_in"].tolist(),
        "edge_total": np.asarray(out["edge_total"], dtype=float).tolist(),
        "dstate": np.asarray(out["dstate"], dtype=float).tolist(),
        "state_out": np.asarray(out["state_out"], dtype=float).tolist(),
        "laplacian_eigenvalues": np.linalg.eigvalsh(np.asarray(out["laplacian"], dtype=float)).tolist(),
        "weights": {k: float(v) for k, v in out["weights"].items()},
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Six-Particle 15-Edge Geometry",
        "",
        "- model: `6 particles, undirected 15 edges, no self-interaction`",
        f"- particles: `{report['particles']}`",
        f"- edge_count: `{report['edge_count']}`",
        "",
        "## State",
        f"- state_in: `{report['state_in']}`",
        f"- dstate: `{report['dstate']}`",
        f"- state_out: `{report['state_out']}`",
        "",
        "## Spectrum",
        f"- laplacian_eigenvalues: `{report['laplacian_eigenvalues']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"edge_count={report['edge_count']}")
    print(f"json={OUT_JSON}")
    print(f"md={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

