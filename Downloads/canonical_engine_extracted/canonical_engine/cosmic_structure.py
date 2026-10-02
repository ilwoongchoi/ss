"""Cosmic Structure — unified time→structure stem.

Merges 2 scripts:
  1. sphere_history  — 5-sphere historical cosmology (13.8 Gyr leakage settlement)
  2. domain_13       — 13 domains with isomorphic structure + leakage

The stem flows:
  13.8 Gyr history → 5 sphere epochs → leakage settlement → 13 domains → spiral space

Both share the same conceptual framework:
  - Leakage from one epoch/domain creates the space of the next
  - All domains share isomorphic R₄=0.2828 structure
  - 5 spheres ↔ 13 domains mapping
  - Pyramid closure: (11+1)/(5+7) = 1.0

Usage:
  python -m canonical_engine.cosmic_structure              # run both
  python -m canonical_engine.cosmic_structure --history-only
  python -m canonical_engine.cosmic_structure --domains-only
"""
from __future__ import annotations

import pathlib
import sys

from . import sphere_history as sph
from . import domain_13 as dom

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)


def run_all():
    """Run sphere history then domain 13 analysis."""
    print("=== Step 1: 5-Sphere Historical Cosmology ===")
    sph.main()

    print("\n=== Step 2: 13-Domain Universe Structure ===")
    dom.main()

    print("\n=== Cosmic Structure stem complete ===")
    print(f"  Timeline:  {GEN_DIR / 'sphere_history_timeline.png'}")
    print(f"  HistData:  {GEN_DIR / 'sphere_history.json'}")
    print(f"  HistReport:{GEN_DIR / 'sphere_history_report.txt'}")
    print(f"  Domains:   {GEN_DIR / 'domain_13_spiral.png'}")
    print(f"  DomData:   {GEN_DIR / 'domain_13.json'}")
    print(f"  DomReport: {GEN_DIR / 'domain_13_report.txt'}")


if __name__ == "__main__":
    if "--history-only" in sys.argv:
        sph.main()
    elif "--domains-only" in sys.argv:
        dom.main()
    else:
        run_all()
