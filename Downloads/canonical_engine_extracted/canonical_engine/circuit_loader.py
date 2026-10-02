"""Lazy loader for circuit topology generated from markdown.
Provides dict `NODES` keyed by node name, each value is `circuit_schema.Node`.
"""
from __future__ import annotations

import json
import pathlib
from typing import Dict

from .circuit_schema import Node, Port

GEN_PATH = pathlib.Path(__file__).parent / "generated" / "circuit.json"

_raw = json.loads(GEN_PATH.read_text(encoding="utf-8"))

NODES: Dict[str, Node] = {
    d["name"]: Node(
        name=d["name"],
        element=d["element"],
        particle=d["particle"],
        group=d["group"],
        color=d["color"],
        music_dims=tuple(d["music_dims"]),
        location=d.get("location", ""),
        ports=[Port(**p) for p in d["ports"]],
    )
    for d in _raw
}
