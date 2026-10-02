from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.split("}")[-1]


def try_dataselect(url: str, *, timeout_s: int = 30) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "codex-cli"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = resp.read()
            if resp.status == 200 and data:
                return data
            return None
    except urllib.error.HTTPError as e:
        if e.code == 204:
            return None
        raise


def main() -> int:
    meta = json.loads(Path("picked_event.json").read_text(encoding="utf-8"))
    start = meta["window_start"]
    end = meta["window_end"]

    tree = ET.parse("earthscope_station_response.xml")
    root = tree.getroot()

    candidates: list[dict[str, str]] = []
    for net in root.iter():
        if local(net.tag) != "Network":
            continue
        net_code = net.attrib.get("code", "")
        for sta in list(net):
            if local(sta.tag) != "Station":
                continue
            sta_code = sta.attrib.get("code", "")
            for ch in sta.iter():
                if local(ch.tag) != "Channel":
                    continue
                cha = ch.attrib.get("code", "")
                loc = ch.attrib.get("locationCode", "") or ""
                if not (net_code and sta_code and cha):
                    continue
                candidates.append({"net": net_code, "sta": sta_code, "loc": loc, "cha": cha})
                if len(candidates) >= 200:
                    break
            if len(candidates) >= 200:
                break
        if len(candidates) >= 200:
            break

    for c in candidates:
        url = "https://service.earthscope.org/fdsnws/dataselect/1/query?" + urllib.parse.urlencode(
            {"net": c["net"], "sta": c["sta"], "loc": c["loc"], "cha": c["cha"], "starttime": start, "endtime": end}
        )
        data = try_dataselect(url)
        if data is None:
            continue
        Path("picked_channel.json").write_text(json.dumps({**c, "dataselect_url": url}, indent=2), encoding="utf-8")
        Path("picked_waveform.mseed").write_bytes(data)
        print("FOUND", c["net"], c["sta"], c["loc"], c["cha"], len(data))
        return 0

    print("NO_WAVEFORM_FOUND")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

