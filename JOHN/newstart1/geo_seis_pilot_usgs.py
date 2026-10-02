from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
import math
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Any, Iterable


@dataclasses.dataclass(frozen=True)
class Event:
    event_id: str
    time_utc: dt.datetime
    lat: float
    lon: float
    depth_km: float | None
    mag: float | None


def _dt_utc_from_ms(ms: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(ms / 1000.0, tz=dt.UTC)


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def fetch_usgs_events_geojson(
    *,
    starttime: str,
    endtime: str,
    minmagnitude: float,
    minlatitude: float,
    maxlatitude: float,
    minlongitude: float,
    maxlongitude: float,
    limit: int,
) -> dict[str, Any]:
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": str(minmagnitude),
        "minlatitude": str(minlatitude),
        "maxlatitude": str(maxlatitude),
        "minlongitude": str(minlongitude),
        "maxlongitude": str(maxlongitude),
        "limit": str(limit),
        "orderby": "time-asc",
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        raw = resp.read()
    return json.loads(raw.decode("utf-8"))


def parse_events(geojson: dict[str, Any]) -> list[Event]:
    out: list[Event] = []
    for feature in geojson.get("features", []):
        props = feature.get("properties") or {}
        geom = feature.get("geometry") or {}
        coords = geom.get("coordinates") or []
        if not isinstance(coords, list) or len(coords) < 2:
            continue
        lon = _parse_float(coords[0])
        lat = _parse_float(coords[1])
        depth = _parse_float(coords[2]) if len(coords) >= 3 else None
        if lat is None or lon is None:
            continue

        eid = feature.get("id")
        if not isinstance(eid, str) or not eid:
            continue

        t_ms = props.get("time")
        if not isinstance(t_ms, int):
            continue
        t_utc = _dt_utc_from_ms(t_ms)
        mag = _parse_float(props.get("mag"))
        out.append(Event(event_id=eid, time_utc=t_utc, lat=lat, lon=lon, depth_km=depth, mag=mag))
    out.sort(key=lambda e: e.time_utc)
    return out


class DSU:
    def __init__(self, items: Iterable[str]) -> None:
        self.parent: dict[str, str] = {i: i for i in items}
        self.size: dict[str, int] = {i: 1 for i in items}

    def find(self, x: str) -> str:
        p = self.parent.get(x)
        if p is None:
            raise KeyError(x)
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        self.parent[x] = p
        return p

    def union(self, a: str, b: str) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def components(self) -> dict[str, list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for x in self.parent.keys():
            groups[self.find(x)].append(x)
        return dict(groups)


@dataclasses.dataclass(frozen=True)
class Edge:
    a: str
    b: str
    dist_km: float
    dt_days: float


def build_edges(
    events: list[Event],
    *,
    max_dist_km: float,
    max_dt_days: float | None,
) -> list[Edge]:
    edges: list[Edge] = []
    # O(n^2) but kept intentionally small via limit + region selection.
    for i in range(len(events)):
        ei = events[i]
        for j in range(i + 1, len(events)):
            ej = events[j]
            dt_days = abs((ej.time_utc - ei.time_utc).total_seconds()) / 86400.0
            if max_dt_days is not None and dt_days > max_dt_days:
                continue
            d_km = _haversine_km(ei.lat, ei.lon, ej.lat, ej.lon)
            if d_km <= max_dist_km:
                edges.append(Edge(a=ei.event_id, b=ej.event_id, dist_km=d_km, dt_days=dt_days))
    edges.sort(key=lambda e: (e.dist_km, e.dt_days))
    return edges


def closure_run(
    events: list[Event],
    edges: list[Edge],
) -> tuple[int, DSU, list[Edge]]:
    dsu = DSU([e.event_id for e in events])
    used: list[Edge] = []
    components_before = len(dsu.components())
    for edge in edges:
        if dsu.union(edge.a, edge.b):
            used.append(edge)
    components_after = len(dsu.components())
    if components_after > components_before:
        raise RuntimeError("components increased after closure run (should be monotone non-increasing)")
    return components_after, dsu, used


def bridging_low_mag_events(
    *,
    base_events: dict[str, Event],
    extended_events: dict[str, Event],
    max_dist_km: float,
    max_dt_days: float | None,
) -> list[dict[str, Any]]:
    """
    Find low-magnitude events (present only in extended set) that can act as minimal mediators
    between components of the base closure graph.
    """
    base_list = list(base_events.values())
    base_edges = build_edges(base_list, max_dist_km=max_dist_km, max_dt_days=max_dt_days)
    _, base_dsu, _ = closure_run(base_list, base_edges)
    base_comp = base_dsu.components()
    base_comp_id: dict[str, str] = {}
    for root, members in base_comp.items():
        for m in members:
            base_comp_id[m] = root

    added_ids = [eid for eid in extended_events.keys() if eid not in base_events]
    added: list[Event] = [extended_events[eid] for eid in added_ids]

    # For each added event, see which base components it touches within the edge threshold.
    hits: list[dict[str, Any]] = []
    for ev in added:
        touched: dict[str, float] = {}
        for b in base_list:
            dt_days = abs((ev.time_utc - b.time_utc).total_seconds()) / 86400.0
            if max_dt_days is not None and dt_days > max_dt_days:
                continue
            d_km = _haversine_km(ev.lat, ev.lon, b.lat, b.lon)
            if d_km <= max_dist_km:
                comp_root = base_comp_id[b.event_id]
                prev = touched.get(comp_root)
                if prev is None or d_km < prev:
                    touched[comp_root] = d_km

        if len(touched) >= 2:
            touched_sorted = sorted(touched.items(), key=lambda x: x[1])
            hits.append(
                {
                    "mediator_event_id": ev.event_id,
                    "mediator_time_utc": ev.time_utc.isoformat(),
                    "mediator_lat": ev.lat,
                    "mediator_lon": ev.lon,
                    "mediator_mag": ev.mag,
                    "touched_components": len(touched),
                    "closest_component_roots": ";".join([c for c, _ in touched_sorted[:5]]),
                    "closest_component_dists_km": ";".join([f"{d:.3f}" for _, d in touched_sorted[:5]]),
                }
            )
    hits.sort(key=lambda r: (-int(r["touched_components"]), float(r["mediator_mag"] or 0.0)))
    return hits


def _write_csv(path: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="USGS earthquake data pilot: test closure-grammar style internal vs extended closure via magnitude-threshold mediators."
    )
    p.add_argument("--start", required=False, help="YYYY-MM-DD (UTC). Default: now-30d")
    p.add_argument("--end", required=False, help="YYYY-MM-DD (UTC). Default: now")
    p.add_argument("--minlat", type=float, default=32.0)
    p.add_argument("--maxlat", type=float, default=42.5)
    p.add_argument("--minlon", type=float, default=-125.0)
    p.add_argument("--maxlon", type=float, default=-114.0)
    p.add_argument("--base-minmag", type=float, default=3.0)
    p.add_argument("--ext-minmag", type=float, default=1.0)
    p.add_argument("--limit", type=int, default=2000)
    p.add_argument("--max-dist-km", type=float, default=40.0)
    p.add_argument("--max-dt-days", type=float, default=7.0, help="Use 0 to disable time gating (distance-only).")
    p.add_argument("--out-prefix", default="GEO_SEIS_USGS_PILOT")
    args = p.parse_args(argv)

    now = dt.datetime.now(tz=dt.UTC).date()
    start = args.start or (now - dt.timedelta(days=30)).isoformat()
    end = args.end or now.isoformat()
    max_dt_days: float | None = None if args.max_dt_days == 0 else args.max_dt_days

    base_geo = fetch_usgs_events_geojson(
        starttime=start,
        endtime=end,
        minmagnitude=args.base_minmag,
        minlatitude=args.minlat,
        maxlatitude=args.maxlat,
        minlongitude=args.minlon,
        maxlongitude=args.maxlon,
        limit=args.limit,
    )
    ext_geo = fetch_usgs_events_geojson(
        starttime=start,
        endtime=end,
        minmagnitude=args.ext_minmag,
        minlatitude=args.minlat,
        maxlatitude=args.maxlat,
        minlongitude=args.minlon,
        maxlongitude=args.maxlon,
        limit=args.limit,
    )

    base_events_list = parse_events(base_geo)
    ext_events_list = parse_events(ext_geo)
    base_events = {e.event_id: e for e in base_events_list}
    ext_events = {e.event_id: e for e in ext_events_list}

    base_edges = build_edges(base_events_list, max_dist_km=args.max_dist_km, max_dt_days=max_dt_days)
    ext_edges = build_edges(ext_events_list, max_dist_km=args.max_dist_km, max_dt_days=max_dt_days)

    base_components, base_dsu, base_used = closure_run(base_events_list, base_edges)
    ext_components, ext_dsu, ext_used = closure_run(ext_events_list, ext_edges)
    base_ids = {e.event_id for e in base_events_list}
    base_components_inside_extended = len({ext_dsu.find(eid) for eid in base_ids if eid in ext_dsu.parent})

    mediator_hits = bridging_low_mag_events(
        base_events=base_events,
        extended_events=ext_events,
        max_dist_km=args.max_dist_km,
        max_dt_days=max_dt_days,
    )

    out_report = f"{args.out_prefix}_REPORT.md"
    out_mediators = f"{args.out_prefix}_MEDIATOR_CANDIDATES.csv"
    out_summary = f"{args.out_prefix}_SUMMARY.json"

    _write_csv(out_mediators, mediator_hits[:500])

    summary = {
        "query": {
            "start": start,
            "end": end,
            "bbox": [args.minlat, args.maxlat, args.minlon, args.maxlon],
            "base_minmag": args.base_minmag,
            "ext_minmag": args.ext_minmag,
            "limit": args.limit,
            "max_dist_km": args.max_dist_km,
            "max_dt_days": max_dt_days,
        },
        "counts": {
            "base_events": len(base_events_list),
            "ext_events": len(ext_events_list),
            "added_events": len(ext_events_list) - len(base_events_list),
        },
        "closure": {
            "base_components": base_components,
            "ext_components": ext_components,
            "base_components_inside_extended": base_components_inside_extended,
            "base_edges_total": len(base_edges),
            "ext_edges_total": len(ext_edges),
            "base_edges_used": len(base_used),
            "ext_edges_used": len(ext_used),
            "mediator_candidates_found": len(mediator_hits),
        },
    }
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    def _top_component_sizes(dsu: DSU, n: int = 10) -> list[int]:
        comps = dsu.components()
        sizes = sorted((len(v) for v in comps.values()), reverse=True)
        return sizes[:n]

    report_lines = [
        "# GEO/SEIS USGS Pilot — Closure Grammar Check",
        "",
        "This pilot tests a concrete 'internal vs extended closure' mechanism on real earthquake catalog data:",
        "",
        "- **Internal universe** = events above a stricter magnitude threshold (base).",
        "- **Extended universe** = include lower-magnitude events (extended).",
        "- **Mediator candidates** = added low-magnitude events that touch 2+ base components under the same edge rule.",
        "",
        "## Query",
        f"- Date range (UTC): `{start}` → `{end}`",
        f"- BBox: lat `{args.minlat}`..`{args.maxlat}`, lon `{args.minlon}`..`{args.maxlon}`",
        f"- Edge rule: distance ≤ `{args.max_dist_km}` km"
        + (f", time gap ≤ `{max_dt_days}` days" if max_dt_days is not None else ", time gate: disabled"),
        f"- Base min magnitude: `{args.base_minmag}`",
        f"- Extended min magnitude: `{args.ext_minmag}`",
        f"- API limit per query: `{args.limit}`",
        "",
        "## Results (Connected Components)",
        f"- Base events: `{len(base_events_list)}`; components: `{base_components}`",
        f"- Extended events: `{len(ext_events_list)}` (+{len(ext_events_list) - len(base_events_list)}); components: `{ext_components}`",
        f"- Base components *inside extended graph*: `{base_components_inside_extended}` (lower means 'mediator' actually merges base components)",
        "",
        "### Component size snapshot",
        f"- Base top sizes: `{_top_component_sizes(base_dsu)}`",
        f"- Extended top sizes: `{_top_component_sizes(ext_dsu)}`",
        "",
        "## Mediator candidates",
        f"- Candidates found (touching ≥2 base components): `{len(mediator_hits)}`",
        f"- Output: `{out_mediators}`",
        "",
        "## What this does / does not claim",
        "- If extended components < base components **under identical edge rules**, then lower-magnitude events behave like **mediators** that restore continuity lost by thresholding.",
        "- This is **not** a proof of 'universal geometry'; it is a concrete reproducible check that the *closure-grammar mechanism* (projection trap via thresholding + extended closure via minimal mediators) occurs in a real sparse-observation geophysical dataset.",
        "",
    ]
    with open(out_report, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
