#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
export_128_personality_grid_trajectories.py
------------------------------------------
Exports the 128 personality trajectories from the existing MBTI/Blood/Gender
physics grid engine (no per-type hand-drawing).

This is the "grid you meant" pipeline:
  - uses 128GIRD_MBTI_PHYSICS.py generate_trajectory_pure()
  - exports raw point lists so rendering can be fast and reproducible

Outputs:
  - out/mbti128_grid_trajectories.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _as_float_pairs(pts: list[tuple[float, float]]) -> list[list[float]]:
    return [[float(x), float(y)] for x, y in pts]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", type=float, default=None, help="Override area (optional)")
    ap.add_argument("--outdir", type=str, default="out")
    ap.add_argument("--limit", type=int, default=0, help="If >0, export only first N personalities (debug)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # The engine filename starts with a digit, so import it by path.
    import importlib.util

    engine_path = Path("128GIRD_MBTI_PHYSICS.py").resolve()
    if not engine_path.exists():
        raise SystemExit(f"Missing {engine_path}")
    spec = importlib.util.spec_from_file_location("mbti_grid_engine", engine_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Failed to import {engine_path}")
    eng = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eng)

    out: dict[str, Any] = {
        "schema": "mbti128_grid_trajectories_v1",
        "engine": "128GIRD_MBTI_PHYSICS.generate_trajectory_pure",
        "area_override": args.area,
        "items": [],
    }

    count = 0
    for mbti in eng.ALL_MBTI:
        for blood in eng.BLOODS:
            for gender in eng.GENDERS:
                if args.limit and count >= args.limit:
                    break
                sr = eng.generate_trajectory_pure(mbti, blood, gender, "sunrise", args.area)
                ss = eng.generate_trajectory_pure(mbti, blood, gender, "sunset", args.area)
                out["items"].append(
                    {
                        "mbti": mbti,
                        "blood": blood,
                        "gender": gender,
                        "sunrise": _as_float_pairs(sr),
                        "sunset": _as_float_pairs(ss),
                    }
                )
                count += 1

    path = outdir / "mbti128_grid_trajectories.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
