"""Canonical schema for circuit representation.
Provides dataclasses `Port` and `Node` used across the math engine.
All parser/generator code should emit JSON that conforms to this schema.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, List, Tuple

PortKind = Literal["in", "out", "ctrl"]


@dataclass
class Port:
    kind: PortKind
    name: str  # e.g. "in0", "out1", "ctrl0"
    link: str  # fully-qualified endpoint string "other_node.port"


@dataclass
class Node:
    name: str
    element: str  # periodic symbol with atomic number, e.g. "Na(11)"
    particle: str  # e.g. "w_boson"
    group: str  # chemical/functional group label
    color: str  # color tag as used in prose (RED, BLUE, ...)
    music_dims: Tuple[str, ...]  # subset of {r,h,d,p,s,gamma,g,nu}
    location: str = ""  # inferred anatomical/physical coordinate
    ports: List[Port] = field(default_factory=list)
