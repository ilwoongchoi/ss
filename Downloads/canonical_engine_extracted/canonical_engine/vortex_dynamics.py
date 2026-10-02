"""Vortex Body Dynamics — unified spatial→dynamic stem.

Merges 2 scripts:
  1. generate_4_vortex_body_nodes  — 1000 nodes via 4-vortex spiral
  2. plot_vortex_dynamics           — stress pair curves across nodes

The stem flows:
  4 vortex centers → log spiral → 1000 nodes → 8D vectors → stress pair curves

Usage:
  python -m canonical_engine.vortex_dynamics              # generate + plot
  python -m canonical_engine.vortex_dynamics --plot-only   # plot from existing data
"""
from __future__ import annotations

import pathlib
import runpy
import sys

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)


def _run_module(mod_name: str):
    """Run a module's __main__ block in-process."""
    runpy.run_module(mod_name, run_name="__main__")


def run_all():
    """Generate nodes then plot dynamics."""
    print("=== Step 1: Generate 4-vortex body nodes ===")
    _run_module("canonical_engine.generate_4_vortex_body_nodes")

    print("\n=== Step 2: Plot vortex dynamics ===")
    _run_module("canonical_engine.plot_vortex_dynamics")

    print("\n=== Vortex Dynamics stem complete ===")
    print(f"  Nodes:  {GEN_DIR / 'vortex_body_nodes.json'}")
    print(f"  CSV:    {GEN_DIR / 'vortex_body_nodes.csv'}")
    print(f"  Plot:   {GEN_DIR / 'vortex_dynamics.png'}")
    print(f"  Data:   {GEN_DIR / 'vortex_dynamics_data.json'}")
    print(f"  Report: {GEN_DIR / 'vortex_dynamics_summary.txt'}")


if __name__ == "__main__":
    if "--plot-only" in sys.argv:
        _run_module("canonical_engine.plot_vortex_dynamics")
    else:
        run_all()
