"""Parse `circuitfile-rewritten.md` into canonical JSON.
Run once when the markdown changes.  Outputs `generated/circuit.json`."""
from __future__ import annotations

import json
import pathlib
import re
from typing import Dict, List

from canonical_engine.circuit_schema import Node, Port

MD_PATH = pathlib.Path(__file__).parent.parent / "circuitfile1.md"
OUT_PATH = pathlib.Path(__file__).parent / "generated" / "circuit.json"
OUT_PATH.parent.mkdir(exist_ok=True)

NODE_HEADER_RE = re.compile(r"^([A-Za-z0-9_]+) \[.*$")
PORT_RE = re.compile(r"^\s+([A-Za-z0-9_]+)\s+(<-|->)\s+(.+)$")
PHYSICS_RE = re.compile(r"^\s*#\s*PHYSICS:\s*(.+)$")
MUSIC_RE = re.compile(r"\*\*음악 차원\*\*: (.+)")
LOCATION_RE = re.compile(r"^\s*#\s*LOCATION:\s*(.+)$")

nodes: Dict[str, Node] = {}
current: Node | None = None

with MD_PATH.open(encoding="utf-8") as f:
    for line in f:
        m = NODE_HEADER_RE.match(line)
        if m:
            name = m.group(1)
            current = Node(name=name, element="", particle="", group="", color="", music_dims=())
            nodes[name] = current
            continue
        if current:
            loc = LOCATION_RE.match(line)
            if loc and not current.location:
                current.location = loc.group(1).strip()
                continue
            phys = PHYSICS_RE.match(line)
            if phys and not current.element:
                payload = phys.group(1)
                fields = [f.strip() for f in re.split(r"[|]", payload)]
                kv: Dict[str, str] = {}
                for f in fields:
                    # a field may contain comma-separated key=value pairs, e.g.
                    # element=Mn(25),particle=muon(밤)
                    for pair in f.split(","):
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            kv[k.strip().lower()] = v.strip()
                current.element = kv.get("element", "")
                current.particle = kv.get("particle", "")
                current.color = kv.get("color", "")
                current.group = kv.get("group", "")
                continue
            music = MUSIC_RE.search(line)
            if music and not current.music_dims:
                dims = []
                for token in ("r","h","d","p","s","gamma","g","nu"):
                    if token in music.group(1):
                        dims.append(token)
                current.music_dims = tuple(dims)
                continue
            p = PORT_RE.match(line)
            if p:
                kind_name = p.group(1)
                arrow = p.group(2)
                raw_link = p.group(3).strip()
                if arrow == "->":
                    kind = "out"
                elif kind_name.startswith("ctrl"):
                    kind = "ctrl"
                else:
                    kind = "in"
                # strip inline comment and split comma-separated targets
                raw_link = raw_link.split("#")[0].strip()
                for link in raw_link.split(","):
                    link = link.strip()
                    if not link:
                        continue
                    current.ports.append(Port(kind=kind, name=kind_name, link=link))

serialisable = [node.__dict__ | {"ports": [port.__dict__ for port in node.ports]} for node in nodes.values()]
OUT_PATH.write_text(json.dumps(serialisable, indent=2), encoding="utf-8")
print(f"Wrote {len(nodes)} nodes -> {OUT_PATH}")
