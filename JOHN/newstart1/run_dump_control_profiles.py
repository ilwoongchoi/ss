from __future__ import annotations

import json
from pathlib import Path

from fusion_clean import _channel_control_profile


ROOT = Path(__file__).resolve().parent
OUT_MD = ROOT / "analysis_results" / "control_profiles.md"
OUT_JSON = ROOT / "analysis_results" / "control_profiles.json"


def _sort_keys(d: dict[str, object]) -> list[str]:
    keys = [str(k) for k in d.keys()]
    # Put the metadata key first if present.
    keys.sort(key=lambda k: (k != "hysteresis_window", k))
    return keys


def main() -> int:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    minutes = {
        "outside": 0,
        "hysteresis": 120,  # within 01:30-03:00 window
    }
    personas = ["user", "people"]

    profiles: dict[str, dict[str, dict[str, object]]] = {}
    for persona in personas:
        profiles[persona] = {}
        for regime, minute in minutes.items():
            profiles[persona][regime] = _channel_control_profile(int(minute), persona=persona)

    # JSON
    OUT_JSON.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown
    # Build a stable superset of keys.
    all_keys: set[str] = set()
    for persona in personas:
        for regime in minutes:
            all_keys.update(_sort_keys(profiles[persona][regime]))

    cols = [
        ("user", "outside"),
        ("user", "hysteresis"),
        ("people", "outside"),
        ("people", "hysteresis"),
    ]

    lines = []
    lines.append("# Control Profiles")
    lines.append("")
    lines.append("This is a direct dump of `_channel_control_profile(...)` with `config.toml` applied.")
    lines.append("")
    lines.append("| key | user/outside | user/hysteresis | people/outside | people/hysteresis |")
    lines.append("|---|---:|---:|---:|---:|")

    for k in sorted(all_keys):
        row = [k]
        for persona, regime in cols:
            row.append(str(profiles[persona][regime].get(k, "")))
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Differences (user vs people)")
    lines.append("")
    lines.append("| key | user/outside | people/outside | user/hysteresis | people/hysteresis |")
    lines.append("|---|---:|---:|---:|---:|")
    for k in sorted(all_keys):
        u_out = str(profiles["user"]["outside"].get(k, ""))
        p_out = str(profiles["people"]["outside"].get(k, ""))
        u_h = str(profiles["user"]["hysteresis"].get(k, ""))
        p_h = str(profiles["people"]["hysteresis"].get(k, ""))
        if (u_out != p_out) or (u_h != p_h):
            lines.append(f"| {k} | {u_out} | {p_out} | {u_h} | {p_h} |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
