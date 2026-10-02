"""Earth Cosmic Map — unified Earth→cosmic stem.

Merges 2 scripts:
  1. earth_energy_map     — map all subjects on Earth, compute energy paths
  2. proximal_resonance   — co-location analysis around geological nodes

The stem flows:
  Earth coordinates → subject placement → energy flow paths → proximal resonance

Usage:
  python -m canonical_engine.earth_cosmic_map              # run both
  python -m canonical_engine.earth_cosmic_map --map-only    # just the map
  python -m canonical_engine.earth_cosmic_map --resonance-only
"""
from __future__ import annotations

import pathlib
import sys

from . import earth_energy_map as emap
from . import proximal_resonance as pres

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)


def run_all():
    """Run earth map then proximal resonance."""
    print("=== Step 1: Earth Energy Map ===")
    emap.main()

    print("\n=== Step 2: Proximal Resonance ===")
    pres.main()

    print("\n=== Earth Cosmic Map stem complete ===")
    print(f"  Map:     {GEN_DIR / 'earth_energy_map.png'}")
    print(f"  Paths:   {GEN_DIR / 'earth_energy_paths.json'}")
    print(f"  Report:  {GEN_DIR / 'earth_energy_report.txt'}")
    print(f"  Resonance: {GEN_DIR / 'proximal_resonance_map.png'}")
    print(f"  ResData:   {GEN_DIR / 'proximal_resonance.json'}")
    print(f"  ResReport: {GEN_DIR / 'proximal_resonance_report.txt'}")


if __name__ == "__main__":
    if "--map-only" in sys.argv:
        emap.main()
    elif "--resonance-only" in sys.argv:
        pres.main()
    else:
        run_all()
