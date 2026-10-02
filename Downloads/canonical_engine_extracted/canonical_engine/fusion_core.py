"""Raw-channel → edge ontology derived directly from circuitfile-rewritten.md.

The final circuit absorbs earlier K8 / 64-node drafts; this module now uses
whatever particle / element / group labels the rewritten circuit declares.
No external particle basis is enforced.

The module deliberately contains *no* update logic – it is a pure
declaration layer that higher-level code can import.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# 1. Final-circuit channel set
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 2. Raw 24-channel vector (final-circuit master/control nodes)
# ---------------------------------------------------------------------------
from canonical_engine.circuit_loader import NODES  # generated from markdown

C26_CHANNELS: Tuple[str, ...] = (
    "observer_leftd2",
    "observer_left_endorphin_electron_antineutrino",
    "nonobserver_left_d2",
    "left_endorphin_non_observer",
    "left_genital_d2",
    "right_sole_dopamine",
    "mc1r",
    "carbon",
    "co2",
    "water_vapour",
    "clay_gouge",
    "steel",
    "heme",
    "cytochrome_c_oxidase",
    "sulforaphane",
    "cysteine",
    "memory_entropy",
    "aurora",
    "fold_belt",
    "subduction_zone",
    "plume",
    "lower_mantle",
    "basin",
    "actomyosin",
)
CHANNEL_INDEX: Dict[str, int] = {c: i for i, c in enumerate(C26_CHANNELS)}
RAW_COUNT = len(C26_CHANNELS)  # 24

# ---------------------------------------------------------------------------
# 3. Edge ontology  (particle_i, group_j) -> list[channel]
#     Uses the circuit's own particle and chemical-group labels as-is.
# ---------------------------------------------------------------------------
from collections import defaultdict
_EDGE_MAP: Dict[Tuple[str, str], List[str]] = defaultdict(list)

for ch in C26_CHANNELS:
    node = NODES[ch]
    src = node.particle or "unknown"
    dst = node.group.lower() if node.group else "unknown"
    _EDGE_MAP[(src, dst)].append(ch)

EDGE_MAP: Dict[Tuple[str, str], Tuple[str, ...]] = {
    k: tuple(v) for k, v in _EDGE_MAP.items()
}

# Utility --------------------------------------------------------------------

def list_channels_for_edge(p_src: str, p_dst: str) -> Tuple[str, ...]:
    """Return tuple of raw channels that couple (p_src → p_dst)."""
    return EDGE_MAP.get((p_src, p_dst), ())


def channel_index(name: str) -> int:
    """Return integer index of raw channel in the 24-channel vector."""
    return CHANNEL_INDEX[name]


def list_particles() -> Tuple[str, ...]:
    """Return all distinct particle labels used by the 24 channels."""
    return tuple(sorted({NODES[ch].particle for ch in C26_CHANNELS}))


__all__ = [
    "C26_CHANNELS",
    "EDGE_MAP",
    "list_channels_for_edge",
    "channel_index",
    "list_particles",
]
