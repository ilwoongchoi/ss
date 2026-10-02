"""Load 8-D parameter vectors from CSVs.

Public API
==========
get_vec8(profile_key: str, phase: str) -> Tuple[float, ...]  # len==8
    profile_key  : e.g. "ENFP_F_O"  (same key as music_map.json)
    phase        : "release" | "stress_growth" | "extreme_growth" | "layer1"

Internally caches results in _CACHE dict for speed.
"""
from __future__ import annotations

import csv
import pathlib
from functools import lru_cache
from typing import Dict, Tuple

ROOT = pathlib.Path(__file__).parent.parent
CSV_PRIMARY = ROOT / "128_UNIFIED_MASTER_8D.csv"
CSV_BASELINE = ROOT / "HAPLOGROUP_1318_MASTER.csv"

Vec8 = Tuple[float, float, float, float, float, float, float, float]

# ---------------------------------------------------------------------------
# load helper
# ---------------------------------------------------------------------------

def _load_csv(path: pathlib.Path, phases: Tuple[str, ...]) -> Dict[Tuple[str, str], Vec8]:
    table: Dict[Tuple[str, str], Vec8] = {}
    with path.open(encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            key = row.get("profile_key") or row.get("key") or row.get("slot")
            if not key:
                continue
            key = key.strip()
            for phase in phases:
                if phase not in row:
                    continue
                vec_str = row[phase].strip()
                if not vec_str:
                    continue
                # assume vector stored as comma- or space-sep 8 numbers
                parts = [p for p in re.split(r"[ ,]", vec_str) if p]
                if len(parts) != 8:
                    continue
                vec = tuple(float(x) for x in parts)  # type: ignore[arg-type]
                table[(key, phase)] = vec  # type: ignore[assignment]
    return table

import re

# primary phases present in 128_UNIFIED_MASTER_8D.csv
_PRIMARY_PHASES = ("release", "stress_growth", "extreme_growth")
_BASE_PHASE   = ("layer1",)

_PRIMARY = _load_csv(CSV_PRIMARY, _PRIMARY_PHASES) if CSV_PRIMARY.exists() else {}
_BASE    = _load_csv(CSV_BASELINE, _BASE_PHASE)   if CSV_BASELINE.exists() else {}

# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def get_vec8(profile_key: str, phase: str) -> Vec8:
    profile_key = profile_key.strip()
    phase = phase.strip().lower()
    if phase == "layer1":
        return _BASE.get((profile_key, "layer1"), (0.0,) * 8)  # type: ignore[return-value]
    return _PRIMARY.get((profile_key, phase), (0.0,) * 8)  # type: ignore[return-value]

if __name__ == "__main__":
    # quick sanity
    print(get_vec8("ENFP_F_O", "release"))
