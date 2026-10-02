from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
import math
import sys
from collections import defaultdict
from typing import Any, Iterable


@dataclasses.dataclass(frozen=True)
class QuakeRow:
    row_id: int
    magnitude: float | None
    time_utc: dt.datetime
    latitude: float
    longitude: float
    depth_km: float | None
    gap_deg: float | None
    dmin: float | None
    location: str | None
    title: str | None


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_time(s: str) -> dt.datetime:
    """
    Handles common CSV patterns found in quake exports.
    - '22-11-2022 02:03' (DD-MM-YYYY HH:MM)
    - ISO-8601 (fallback)
    """
    s = s.strip()
    for fmt in ("%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.UTC)
        except ValueError:
            pass
    try:
        # python 3.12: fromisoformat doesn't parse trailing Z reliably without replace
        s2 = s.replace("Z", "+00:00")
        t = dt.datetime.fromisoformat(s2)
        return t.astimezone(dt.UTC) if t.tzinfo else t.replace(tzinfo=dt.UTC)
    except ValueError as e:
        raise ValueError(f"Unsupported date_time format: {s!r}") from e


def read_quake_csv(path: str) -> list[QuakeRow]:
    out: list[QuakeRow] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for idx, row in enumerate(r, start=1):
            lat = _parse_float(row.get("latitude"))
            lon = _parse_float(row.get("longitude"))
            t_raw = row.get("date_time") or row.get("time") or row.get("datetime")
            if lat is None or lon is None or not t_raw:
                continue
            t = _parse_time(t_raw)
            out.append(
                QuakeRow(
                    row_id=idx,
                    magnitude=_parse_float(row.get("magnitude") or row.get("mag")),
                    time_utc=t,
                    latitude=lat,
                    longitude=lon,
                    depth_km=_parse_float(row.get("depth")),
                    gap_deg=_parse_float(row.get("gap")),
                    dmin=_parse_float(row.get("dmin")),
                    location=(row.get("location") or "").strip() or None,
                    title=(row.get("title") or "").strip() or None,
                )
            )
    out.sort(key=lambda q: q.time_utc)
    return out


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


class DSU:
    def __init__(self, items: Iterable[int]) -> None:
        self.parent: dict[int, int] = {i: i for i in items}
        self.size: dict[int, int] = {i: 1 for i in items}

    def find(self, x: int) -> int:
        p = self.parent[x]
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        self.parent[x] = p
        return p

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def components(self) -> dict[int, list[int]]:
        groups: dict[int, list[int]] = defaultdict(list)
        for x in self.parent.keys():
            groups[self.find(x)].append(x)
        return dict(groups)


@dataclasses.dataclass(frozen=True)
class Edge:
    a: int
    b: int
    dist_km: float
    dt_days: float


def build_edges(
    quakes: list[QuakeRow],
    *,
    max_dist_km: float,
    max_dt_days: float | None,
) -> list[Edge]:
    edges: list[Edge] = []
    for i in range(len(quakes)):
        qi = quakes[i]
        for j in range(i + 1, len(quakes)):
            qj = quakes[j]
            dt_days = abs((qj.time_utc - qi.time_utc).total_seconds()) / 86400.0
            if max_dt_days is not None and dt_days > max_dt_days:
                continue
            d_km = _haversine_km(qi.latitude, qi.longitude, qj.latitude, qj.longitude)
            if d_km <= max_dist_km:
                edges.append(Edge(a=qi.row_id, b=qj.row_id, dist_km=d_km, dt_days=dt_days))
    edges.sort(key=lambda e: (e.dist_km, e.dt_days))
    return edges


def closure_components(
    quakes: list[QuakeRow],
    edges: list[Edge],
) -> tuple[int, DSU]:
    dsu = DSU([q.row_id for q in quakes])
    for e in edges:
        dsu.union(e.a, e.b)
    return len(dsu.components()), dsu


def count_base_components_within_extended(*, base_ids: set[int], extended_dsu: DSU) -> int:
    roots = {extended_dsu.find(i) for i in base_ids if i in extended_dsu.parent}
    return len(roots)


def mediator_candidates(
    *,
    base: list[QuakeRow],
    extended: list[QuakeRow],
    max_dist_km: float,
    max_dt_days: float | None,
) -> list[dict[str, Any]]:
    base_ids = {q.row_id for q in base}
    ext_only = [q for q in extended if q.row_id not in base_ids]

    base_edges = build_edges(base, max_dist_km=max_dist_km, max_dt_days=max_dt_days)
    _, base_dsu = closure_components(base, base_edges)
    base_comp_id: dict[int, int] = {}
    for root, members in base_dsu.components().items():
        for m in members:
            base_comp_id[m] = root

    hits: list[dict[str, Any]] = []
    for q in ext_only:
        touched: set[int] = set()
        closest: dict[int, float] = {}
        for b in base:
            dt_days = abs((q.time_utc - b.time_utc).total_seconds()) / 86400.0
            if max_dt_days is not None and dt_days > max_dt_days:
                continue
            d_km = _haversine_km(q.latitude, q.longitude, b.latitude, b.longitude)
            if d_km <= max_dist_km:
                root = base_comp_id[b.row_id]
                touched.add(root)
                prev = closest.get(root)
                if prev is None or d_km < prev:
                    closest[root] = d_km

        if len(touched) >= 2:
            touched_sorted = sorted(((rid, closest[rid]) for rid in touched), key=lambda x: x[1])
            hits.append(
                {
                    "mediator_row_id": q.row_id,
                    "mediator_time_utc": q.time_utc.isoformat(),
                    "mediator_mag": q.magnitude,
                    "mediator_lat": q.latitude,
                    "mediator_lon": q.longitude,
                    "touched_components": len(touched),
                    "closest_component_roots": ";".join(str(r) for r, _ in touched_sorted[:8]),
                    "closest_component_dists_km": ";".join(f"{d:.3f}" for _, d in touched_sorted[:8]),
                    "title": q.title,
                    "location": q.location,
                }
            )
    hits.sort(key=lambda r: (-int(r["touched_components"]), float(r["mediator_mag"] or -999)))
    return hits


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Validate closure-grammar style internal/extended closure on a local earthquake CSV.")
    p.add_argument("--csv", default="earthquake_data.csv")
    p.add_argument("--base-minmag", type=float, default=6.5, help="Use 0 to disable magnitude filtering.")
    p.add_argument("--ext-minmag", type=float, default=6.5, help="Use 0 to disable magnitude filtering.")
    p.add_argument("--base-max-gap", type=float, default=180.0, help="Max azimuthal gap (deg) for base set. Use 0 to disable.")
    p.add_argument("--ext-max-gap", type=float, default=360.0, help="Max azimuthal gap (deg) for extended set. Use 0 to disable.")
    p.add_argument("--max-dist-km", type=float, default=600.0)
    p.add_argument("--max-dt-days", type=float, default=30.0, help="Use 0 to disable time gating (distance-only).")
    p.add_argument("--out-prefix", default="LOCAL_QUAKE_CLOSURE")
    args = p.parse_args(argv)

    max_dt_days: float | None = None if args.max_dt_days == 0 else args.max_dt_days

    quakes = read_quake_csv(args.csv)
    base_minmag = 0.0 if args.base_minmag == 0 else args.base_minmag
    ext_minmag = 0.0 if args.ext_minmag == 0 else args.ext_minmag
    base_max_gap = None if args.base_max_gap == 0 else args.base_max_gap
    ext_max_gap = None if args.ext_max_gap == 0 else args.ext_max_gap

    def _passes(q: QuakeRow, *, minmag: float, max_gap: float | None) -> bool:
        if q.magnitude is None or q.magnitude < minmag:
            return False
        if max_gap is not None:
            if q.gap_deg is None:
                return False
            if q.gap_deg > max_gap:
                return False
        return True

    base = [q for q in quakes if _passes(q, minmag=base_minmag, max_gap=base_max_gap)]
    extended = [q for q in quakes if _passes(q, minmag=ext_minmag, max_gap=ext_max_gap)]

    if not base:
        raise SystemExit(f"No base events found for base-minmag={args.base_minmag}")
    if not extended:
        raise SystemExit(f"No extended events found for ext-minmag={args.ext_minmag}")

    base_edges = build_edges(base, max_dist_km=args.max_dist_km, max_dt_days=max_dt_days)
    ext_edges = build_edges(extended, max_dist_km=args.max_dist_km, max_dt_days=max_dt_days)

    base_components, base_dsu = closure_components(base, base_edges)
    ext_components, ext_dsu = closure_components(extended, ext_edges)
    base_ids = {q.row_id for q in base}
    base_components_inside_extended = count_base_components_within_extended(base_ids=base_ids, extended_dsu=ext_dsu)

    mediators = mediator_candidates(
        base=base,
        extended=extended,
        max_dist_km=args.max_dist_km,
        max_dt_days=max_dt_days,
    )

    out_summary = f"{args.out_prefix}_SUMMARY.json"
    out_report = f"{args.out_prefix}_REPORT.md"
    out_mediators = f"{args.out_prefix}_MEDIATOR_CANDIDATES.csv"

    with open(out_mediators, "w", newline="", encoding="utf-8") as f:
        if mediators:
            w = csv.DictWriter(f, fieldnames=list(mediators[0].keys()))
            w.writeheader()
            w.writerows(mediators[:500])
        else:
            f.write("")

    def _top_sizes(dsu: DSU) -> list[int]:
        sizes = sorted((len(v) for v in dsu.components().values()), reverse=True)
        return sizes[:12]

    summary = {
        "input_csv": args.csv,
        "params": {
            "base_minmag": base_minmag,
            "ext_minmag": ext_minmag,
            "base_max_gap": base_max_gap,
            "ext_max_gap": ext_max_gap,
            "max_dist_km": args.max_dist_km,
            "max_dt_days": max_dt_days,
        },
        "counts": {
            "rows_total": len(quakes),
            "base_events": len(base),
            "extended_events": len(extended),
            "added_events": len(extended) - len(base),
        },
        "closure": {
            "base_components": base_components,
            "extended_components": ext_components,
            "base_components_inside_extended": base_components_inside_extended,
            "base_edges_total": len(base_edges),
            "extended_edges_total": len(ext_edges),
            "mediator_candidates_found": len(mediators),
            "base_top_component_sizes": _top_sizes(base_dsu),
            "extended_top_component_sizes": _top_sizes(ext_dsu),
        },
    }
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    report = [
        "# Local Earthquake CSV — Closure Grammar Check",
        "",
        f"- Input: `{args.csv}`",
        f"- Base min magnitude: `{args.base_minmag}`",
        f"- Extended min magnitude: `{args.ext_minmag}`",
        f"- Edge rule: distance ≤ `{args.max_dist_km}` km"
        + (f", time gap ≤ `{max_dt_days}` days" if max_dt_days is not None else ", time gate: disabled"),
        "",
        "## Results",
        f"- Total rows: `{len(quakes)}`",
        f"- Base events: `{len(base)}` → components: `{base_components}`",
        f"- Extended events: `{len(extended)}` (+{len(extended) - len(base)}) → components: `{ext_components}`",
        "",
        "## Interpretation (tight, not philosophical)",
        "- If `extended_components < base_components` under the SAME edge rule, then lowering the magnitude threshold acts like an **extended-universe mediator expansion** that restores continuity lost by thresholding.",
        "- If there is NO reduction, then either (a) the edge rule is too strict, (b) the dataset is too sparse/global, or (c) magnitude-thresholding is not the right projection trap for this file.",
        "",
        "## Outputs",
        f"- `{out_summary}`",
        f"- `{out_report}`",
        f"- `{out_mediators}`",
        "",
    ]
    with open(out_report, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
