#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(text).strip().lower())


def parse_bool(value, default: bool = False) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return float(value) != 0.0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on", "enabled", "apply", "applied", "active", "viable"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "disabled", "inactive", "blocked", "nonviable", "not_applied"}:
        return False
    return default


def find_col(df: pd.DataFrame, aliases: Sequence[str]) -> Optional[str]:
    target = {norm(a) for a in aliases}
    candidates = {norm(c): c for c in df.columns}
    for n, original in candidates.items():
        if n in target:
            return original
    for alias in target:
        for n, original in candidates.items():
            if alias and alias in n:
                return original
    return None


def find_endpoint_cols(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str], str]:
    endpoint_pairs = [
        ("u", "v"),
        ("a", "b"),
        ("src", "dst"),
        ("source", "target"),
        ("from", "to"),
        ("patch_a", "patch_b"),
        ("node_a", "node_b"),
        ("sheet_u", "sheet_v"),
        ("sheetid_a", "sheetid_b"),
        ("sheet_a", "sheet_b"),
        ("seam_a", "seam_b"),
    ]
    cols_norm = {norm(c): c for c in df.columns}
    for a, b in endpoint_pairs:
        an = norm(a)
        bn = norm(b)
        if an in cols_norm and bn in cols_norm:
            mode = "sheet" if "sheet" in an or "sheet" in bn else "patch"
            return cols_norm[an], cols_norm[bn], mode
    return None, None, "unknown"


SHEET_RE = re.compile(r"sheet[\s_\-]*id[\s:=_\-]*([0-9]+)", re.IGNORECASE)
INT_RE = re.compile(r"^[0-9]+$")


def extract_sheet_id(text: object) -> Optional[str]:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    s = str(text).strip()
    if not s:
        return None
    m = SHEET_RE.search(s)
    if m:
        return str(int(m.group(1)))
    if INT_RE.match(s):
        return str(int(s))
    return None


def discover_seam_csv(root: Path, explicit: Optional[str]) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = root / p
        if not p.exists():
            raise FileNotFoundError(f"Seam CSV not found: {p}")
        return p
    priority = [
        "MANIFOLD_SEAM_TABLE.csv",
        "SEAM_GLUE_MAP.csv",
        "seam_failure_table.csv",
    ]
    for name in priority:
        p = root / name
        if p.exists():
            return p
    seam_like = sorted(root.glob("*seam*.csv"))
    if seam_like:
        return seam_like[0]
    raise FileNotFoundError("Could not find seam CSV. Use --seam-csv.")


def load_patch_to_sheet_map(root: Path, patch_csv: Optional[str]) -> Dict[str, str]:
    if patch_csv:
        p = Path(patch_csv)
        if not p.is_absolute():
            p = root / p
    else:
        p = root / "MANIFOLD_PATCH_TABLE.csv"
    if not p.exists():
        return {}

    df = pd.read_csv(p)
    patch_col = find_col(df, ["patch_id", "patch", "node", "patch_name", "name"])
    if patch_col is None:
        return {}
    sheet_col = find_col(df, ["sheet_id", "sheet", "sheetid"])

    mapping: Dict[str, str] = {}
    for _, row in df.iterrows():
        patch_raw = row.get(patch_col)
        if patch_raw is None or (isinstance(patch_raw, float) and pd.isna(patch_raw)):
            continue
        patch_key = str(patch_raw).strip()
        if not patch_key:
            continue

        sheet_id = None
        if sheet_col is not None:
            sheet_id = extract_sheet_id(row.get(sheet_col))
        if sheet_id is None:
            for col in df.columns:
                sheet_id = extract_sheet_id(row.get(col))
                if sheet_id is not None:
                    break
        if sheet_id is not None:
            mapping[patch_key] = sheet_id
    return mapping


@dataclass
class Edge:
    u: str
    v: str
    applied: bool
    viable: bool
    edge_type: str
    row_index: int
    contact_score: Optional[float]
    gap_min_dist: Optional[float]
    raw: Dict[str, object]


def to_num(value) -> Optional[float]:
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        return float(value)
    except Exception:
        return None


def resolve_node(raw_node: object, patch_to_sheet: Dict[str, str]) -> str:
    text = str(raw_node).strip()
    if text in patch_to_sheet:
        return patch_to_sheet[text]
    sid = extract_sheet_id(text)
    if sid is not None:
        return sid
    return text


def build_edges(df: pd.DataFrame, patch_to_sheet: Dict[str, str], seam_path: Path) -> List[Edge]:
    u_col, v_col, _ = find_endpoint_cols(df)
    if not u_col or not v_col:
        raise ValueError(
            "Could not detect endpoint columns. Supported aliases include: "
            "u/v, a/b, src/dst, from/to, patch_a/patch_b, node_a/node_b, "
            "sheet_u/sheet_v, sheetid_a/sheetid_b."
        )

    applied_col = find_col(df, ["applied", "enabled", "active", "is_applied", "seam_applied"])
    viable_col = find_col(df, ["viable", "locally_viable", "is_viable", "can_apply", "percolation_candidate_flag"])
    type_col = find_col(df, ["type", "edge_type", "seam_type", "mode"])
    contact_col = find_col(df, ["contact_score", "score", "weight"])
    gap_col = find_col(df, ["gap_min_dist", "gap", "distance", "cut_distance"])

    default_applied = True
    if applied_col is None and (viable_col is not None or find_col(df, ["final_verdict", "blocked_reason"]) is not None):
        default_applied = False
    if "failure" in seam_path.name.lower():
        default_applied = False

    edges: List[Edge] = []
    for i, row in df.iterrows():
        u_raw = row.get(u_col)
        v_raw = row.get(v_col)
        if u_raw is None or v_raw is None:
            continue
        if (isinstance(u_raw, float) and pd.isna(u_raw)) or (isinstance(v_raw, float) and pd.isna(v_raw)):
            continue
        u = resolve_node(u_raw, patch_to_sheet)
        v = resolve_node(v_raw, patch_to_sheet)
        if not u or not v or u == v:
            continue

        applied = parse_bool(row.get(applied_col), default=default_applied) if applied_col else default_applied
        viable = parse_bool(row.get(viable_col), default=False) if viable_col else False
        edge_type = str(row.get(type_col, "unknown")) if type_col else "unknown"
        contact_score = to_num(row.get(contact_col)) if contact_col else None
        gap_min_dist = to_num(row.get(gap_col)) if gap_col else None
        edges.append(
            Edge(
                u=u,
                v=v,
                applied=applied,
                viable=viable,
                edge_type=edge_type,
                row_index=int(i),
                contact_score=contact_score,
                gap_min_dist=gap_min_dist,
                raw={str(c): row.get(c) for c in df.columns},
            )
        )
    return edges


def components(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[set]:
    graph: Dict[str, set] = {n: set() for n in nodes}
    for u, v in edges:
        graph.setdefault(u, set()).add(v)
        graph.setdefault(v, set()).add(u)
    seen = set()
    comps: List[set] = []
    for start in graph:
        if start in seen:
            continue
        stack = [start]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.add(cur)
            stack.extend(graph[cur] - seen)
        comps.append(comp)
    comps.sort(key=lambda c: (-len(c), sorted(c)))
    return comps


def comp_index_map(comps: List[set]) -> Dict[str, int]:
    out = {}
    for i, comp in enumerate(comps):
        for n in comp:
            out[n] = i
    return out


def disconnected_pairs(comps: List[set]) -> List[Tuple[int, int]]:
    return list(itertools.combinations(range(len(comps)), 2))


def grep_left_right_epi(root: Path) -> List[Dict[str, object]]:
    patterns = [
        re.compile(r"\bleft\b.{0,32}\bepinephrine\b", re.IGNORECASE),
        re.compile(r"\bright\b.{0,32}\bepinephrine\b", re.IGNORECASE),
        re.compile(r"\bL\.?\s*Epi(?:nephrine)?\b", re.IGNORECASE),
        re.compile(r"\bR\.?\s*Epi(?:nephrine)?\b", re.IGNORECASE),
        re.compile(r"left[_\-\s]*epi", re.IGNORECASE),
        re.compile(r"right[_\-\s]*epi", re.IGNORECASE),
    ]
    text_ext = {".py", ".md", ".txt", ".html", ".yaml", ".yml", ".ini"}
    skip_dirs = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        "moveout",
        "out",
        "results",
        "runs",
        "pi_atlas",
        "pythonsim",
        "FINAL_TRACKA_BUNDLE",
        "FROZEN_TRACKA_STATE_20260129",
        "temp_forensic_runs",
        "temp_zip_verify",
        "%SNAP%",
        "analysis_output",
        "analysis_results",
        "arxiv_downloads_targeted",
    }
    max_file_bytes = 2 * 1024 * 1024
    hits: List[Dict[str, object]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() not in text_ext:
                continue
            try:
                if path.stat().st_size > max_file_bytes:
                    continue
            except Exception:
                continue
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as f:
                    for ln, line in enumerate(f, start=1):
                        if any(p.search(line) for p in patterns):
                            hits.append(
                                {
                                    "file": str(path.relative_to(root)),
                                    "line": ln,
                                    "text": line.strip(),
                                }
                            )
            except Exception:
                continue
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description="Graph gluing audit for seam tables.")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--seam-csv", default=None, help="Path to seam table CSV")
    parser.add_argument("--patch-csv", default=None, help="Path to MANIFOLD_PATCH_TABLE.csv (optional)")
    parser.add_argument("--target-sheet-id", default="2", help="Target sheet id for scenario viable application")
    parser.add_argument("--top-k", type=int, default=20, help="Top candidate bridge edges to print")
    parser.add_argument("--out-json", default="geometry_glue_audit_report.json", help="Output JSON report path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    seam_path = discover_seam_csv(root, args.seam_csv)
    seam_df = pd.read_csv(seam_path)

    patch_to_sheet = load_patch_to_sheet_map(root, args.patch_csv)
    mapped_mode = "sheet_id" if patch_to_sheet else "patch"

    edges = build_edges(seam_df, patch_to_sheet, seam_path)
    if not edges:
        raise RuntimeError("No edges parsed from seam table.")

    nodes = sorted(set([e.u for e in edges] + [e.v for e in edges]))
    baseline_edges = [(e.u, e.v) for e in edges if e.applied]
    baseline_comps = components(nodes, baseline_edges)

    target = str(int(args.target_sheet_id)) if str(args.target_sheet_id).strip().isdigit() else str(args.target_sheet_id).strip()
    scenario_edges = []
    for e in edges:
        use = e.applied or (e.viable and (e.u == target or e.v == target))
        if use:
            scenario_edges.append((e.u, e.v))
    scenario_comps = components(nodes, scenario_edges)

    scenario_idx = comp_index_map(scenario_comps)
    dis_pairs = disconnected_pairs(scenario_comps)

    pair_gap_counts: List[Dict[str, object]] = []
    for i, j in dis_pairs:
        comp_i = scenario_comps[i]
        comp_j = scenario_comps[j]
        nonviable_cross = 0
        for e in edges:
            cross = (e.u in comp_i and e.v in comp_j) or (e.u in comp_j and e.v in comp_i)
            if cross and not e.viable:
                nonviable_cross += 1
        pair_gap_counts.append(
            {
                "pair": [i, j],
                "size_i": len(comp_i),
                "size_j": len(comp_j),
                "nonviable_cross_cut_edges": nonviable_cross,
            }
        )

    scenario_edge_set = {tuple(sorted(x)) for x in scenario_edges}
    bridge_candidates = []
    for e in edges:
        same = scenario_idx.get(e.u) == scenario_idx.get(e.v)
        if same:
            continue
        if tuple(sorted((e.u, e.v))) in scenario_edge_set:
            continue
        bridge_candidates.append(e)

    def cand_sort_key(e: Edge):
        gap = e.gap_min_dist if e.gap_min_dist is not None else float("inf")
        score = e.contact_score if e.contact_score is not None else float("-inf")
        return (0 if e.viable else 1, gap, -score, str(e.edge_type), e.row_index)

    bridge_candidates.sort(key=cand_sort_key)
    top_candidates = [
        {
            "u": e.u,
            "v": e.v,
            "viable": e.viable,
            "applied": e.applied,
            "type": e.edge_type,
            "contact_score": e.contact_score,
            "gap_min_dist": e.gap_min_dist,
            "row_index": e.row_index,
        }
        for e in bridge_candidates[: args.top_k]
    ]

    epi_hits = grep_left_right_epi(root)

    report = {
        "root": str(root),
        "seam_csv": str(seam_path),
        "node_mode": mapped_mode,
        "patch_to_sheet_map_size": len(patch_to_sheet),
        "nodes": len(nodes),
        "edges_total": len(edges),
        "baseline": {
            "components": len(baseline_comps),
            "sizes": [len(c) for c in baseline_comps],
            "members": [sorted(list(c)) for c in baseline_comps],
        },
        "scenario": {
            "target_sheet_id": target,
            "components": len(scenario_comps),
            "sizes": [len(c) for c in scenario_comps],
            "members": [sorted(list(c)) for c in scenario_comps],
        },
        "remaining_disconnected_component_pairs": pair_gap_counts,
        "top_candidate_bridging_edges": top_candidates,
        "left_right_epinephrine_hits": epi_hits,
    }

    out_json = Path(args.out_json)
    if not out_json.is_absolute():
        out_json = root / out_json
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] Seam table: {seam_path.name}")
    print(f"[INFO] Node mode: {mapped_mode} (mapping size={len(patch_to_sheet)})")
    print(f"[BASELINE] components={report['baseline']['components']} sizes={report['baseline']['sizes']}")
    print(f"[SCENARIO] components={report['scenario']['components']} sizes={report['scenario']['sizes']} target_sheet_id={target}")
    print(f"[GAP] disconnected_pairs={len(pair_gap_counts)}")
    for row in pair_gap_counts[:20]:
        print(f"  pair={tuple(row['pair'])} nonviable_cross_cut_edges={row['nonviable_cross_cut_edges']}")
    print(f"[CANDIDATES] top={len(top_candidates)}")
    for c in top_candidates[:10]:
        print(
            "  "
            + f"{c['u']} -- {c['v']} viable={c['viable']} applied={c['applied']} "
            + f"type={c['type']} gap_min_dist={c['gap_min_dist']} contact_score={c['contact_score']}"
        )
    print(f"[EPI GREP] hits={len(epi_hits)}")
    for h in epi_hits[:20]:
        print(f"  {h['file']}:{h['line']}  {h['text']}")
    print(f"[INFO] Report written: {out_json}")


if __name__ == "__main__":
    main()
