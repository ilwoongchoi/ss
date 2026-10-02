from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def http_get(url: str, *, timeout_s: int = 30) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout_s) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-wave", action="store_true", help="Only download catalog + station XML, skip waveform MiniSEED.")
    ap.add_argument("--timeout-s", type=int, default=30)
    args = ap.parse_args()

    # Exact example query the user referenced
    usgs_url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?"
        + urllib.parse.urlencode(
            {
                "format": "geojson",
                "starttime": "2026-02-01",
                "endtime": "2026-03-01",
                "minmagnitude": "4",
                "minlatitude": "32",
                "maxlatitude": "42",
                "minlongitude": "-125",
                "maxlongitude": "-114",
                "orderby": "time-asc",
                "limit": "20000",
            }
        )
    )

    geo_path = Path("usgs_events_2026-02-01_2026-03-01_ca_bbox.geojson")
    print("Downloading USGS GeoJSON...", flush=True)
    geo_path.write_bytes(http_get(usgs_url, timeout_s=args.timeout_s))
    geojson: dict[str, Any] = json.loads(geo_path.read_text(encoding="utf-8"))

    features = geojson.get("features") or []
    if not isinstance(features, list) or not features:
        raise SystemExit("No events returned from USGS for the example query.")

    def _mag(f: dict[str, Any]) -> float:
        props = f.get("properties") or {}
        m = props.get("mag")
        try:
            return float(m)
        except (TypeError, ValueError):
            return -1e9

    features.sort(key=_mag, reverse=True)
    top = features[0]
    props = top.get("properties") or {}
    geom = top.get("geometry") or {}
    coords = geom.get("coordinates") or []
    if not (isinstance(coords, list) and len(coords) >= 2):
        raise SystemExit("Picked event missing coordinates.")
    lon = float(coords[0])
    lat = float(coords[1])

    t_ms = props.get("time")
    if not isinstance(t_ms, int):
        raise SystemExit("Picked event missing time.")
    origin = dt.datetime.fromtimestamp(t_ms / 1000.0, tz=dt.UTC)
    window_start = (origin - dt.timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S")
    window_end = (origin + dt.timedelta(minutes=8)).strftime("%Y-%m-%dT%H:%M:%S")

    station_url = (
        "http://service.iris.edu/fdsnws/station/1/query?"
        + urllib.parse.urlencode(
            {
                "format": "xml",
                "starttime": window_start,
                "endtime": window_end,
                "minlat": str(lat - 2),
                "maxlat": str(lat + 2),
                "minlon": str(lon - 2),
                "maxlon": str(lon + 2),
                "level": "channel",
            }
        )
    )

    picked_event = {
        "id": top.get("id"),
        "mag": props.get("mag"),
        "time_utc": origin.isoformat(),
        "lat": lat,
        "lon": lon,
        "window_start": window_start,
        "window_end": window_end,
        "station_url": station_url,
    }
    Path("picked_event.json").write_text(json.dumps(picked_event, indent=2), encoding="utf-8")

    station_xml_path = Path("iris_station_response.xml")
    print("Downloading StationXML (IRIS/EarthScope station service)...", flush=True)
    station_xml_path.write_bytes(http_get(station_url, timeout_s=args.timeout_s))

    tree = ET.parse(station_xml_path)
    root = tree.getroot()

    def local(tag: str) -> str:
        return tag.split("}")[-1]

    net = sta = cha = None
    loc = ""
    for net_el in root.iter():
        if local(net_el.tag) != "Network":
            continue
        net = net_el.attrib.get("code")
        for sta_el in net_el:
            if local(sta_el.tag) != "Station":
                continue
            sta = sta_el.attrib.get("code")
            for ch_el in sta_el.iter():
                if local(ch_el.tag) != "Channel":
                    continue
                loc = ch_el.attrib.get("locationCode", "") or ""
                cha = ch_el.attrib.get("code")
                break
            if cha:
                break
        if cha:
            break

    if not (net and sta and cha):
        raise SystemExit("StationXML returned no channels in the selected window/bbox.")

    wave_url = (
        "https://service.earthscope.org/fdsnws/dataselect/1/query?"
        + urllib.parse.urlencode(
            {
                "net": net,
                "sta": sta,
                "loc": loc,
                "cha": cha,
                "starttime": window_start,
                "endtime": window_end,
            }
        )
    )

    picked_channel = {"net": net, "sta": sta, "loc": loc, "cha": cha, "dataselect_url": wave_url}
    Path("picked_channel.json").write_text(json.dumps(picked_channel, indent=2), encoding="utf-8")

    if args.no_wave:
        print("Skipping waveform download (--no-wave).", flush=True)
        print("OK")
        print(f"USGS_GEOJSON={geo_path}")
        print("PICKED_EVENT=picked_event.json")
        print("STATION_XML=iris_station_response.xml")
        print("PICKED_CHANNEL=picked_channel.json")
        return 0

    print("Downloading waveform MiniSEED (EarthScope dataselect)...", flush=True)
    mseed_path = Path("picked_waveform.mseed")
    mseed_path.write_bytes(http_get(wave_url, timeout_s=args.timeout_s))

    print("OK")
    print(f"USGS_GEOJSON={geo_path}")
    print("PICKED_EVENT=picked_event.json")
    print("STATION_XML=iris_station_response.xml")
    print("PICKED_CHANNEL=picked_channel.json")
    print(f"WAVEFORM_MSEED={mseed_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
