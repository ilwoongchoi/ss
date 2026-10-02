"""Local test for the 5HT1A bridge-break hypothesis.

This script does not modify the main engine. It probes the edge strengths
for an A-type profile during the requested 02:15-03:00 window and reports
what would change if the 5HT1A-related bridge edges were locally suppressed.
"""

from __future__ import annotations

import numpy as np

from geometry_package import universal_equation as ue
from geometry_package.absolute_constants import S_PHOTON


def _profile_for(mbti: str, blood: str, gender: str) -> np.ndarray:
    return np.array(
        [
            1.0 if mbti[0] == "I" else 0.0,
            1.0 if mbti[1] == "N" else 0.0,
            1.0 if mbti[2] == "T" else 0.0,
            1.0 if mbti[3] == "J" else 0.0,
        ],
        dtype=float,
    )


def main():
    mbti = "INTP"
    blood = "A"
    gender = "F"
    t_hours = 2.5  # inside 02:15-03:00
    profile = _profile_for(mbti, blood, gender)

    # Probe the baseline edge strengths through the existing kernel.
    edge_s = ue._edge_strengths_from_receptors(
        r=np.full(len(ue._receptor_names()), 0.5, dtype=float),
        active_particle=ue.active_particle_from_scale(S_PHOTON),
        profile=profile,
        t=t_hours,
        gain=0.5,
        schedule=1.0,
    )

    print("baseline BM_SM:", edge_s.get("BM_SM", 0.0))
    print("baseline SM_SW:", edge_s.get("SM_SW", 0.0))

    # Local-only bridge break, without touching the main engine.
    edge_s_break = dict(edge_s)
    edge_s_break["BM_SM"] = 0.0
    edge_s_break["SM_SW"] = 0.0

    print("broken BM_SM:", edge_s_break.get("BM_SM", 0.0))
    print("broken SM_SW:", edge_s_break.get("SM_SW", 0.0))


if __name__ == "__main__":
    main()
