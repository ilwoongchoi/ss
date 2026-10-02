from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from fusion_clean import MOTIF_TARGET_4, nuclear_fusion_coarse_grain


ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "analysis_results" / "nuclear_fusion_0930.json"
OUT_MD = ROOT / "analysis_results" / "nuclear_fusion_0930.md"


def _fmt(x: float) -> str:
    return f"{x:.6g}"


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Use the motif-locked closure target as the baseline state.
    state4 = np.asarray(MOTIF_TARGET_4, dtype=float)
    out = nuclear_fusion_coarse_grain(
        state4,
        phase_fill=0.5,
        clock_hhmm="09:30",
        control_override={"__persona__": "user"},
    )

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    c = dict(out.get("components") or {})
    lines = [
        "# Nuclear Fusion Proxy @ 09:30",
        "",
        "Baseline input state: `MOTIF_TARGET_4`",
        "",
        f"- fusion_rate: `{_fmt(float(out.get('fusion_rate', 0.0)))}`",
        "",
        "## Components",
        f"- neutron_star: `{_fmt(float(c.get('neutron_star', 0.0)))}`",
        f"- higgs_02828: `{_fmt(float(c.get('higgs_02828', 0.0)))}`",
        f"- effective_string_tension: `{_fmt(float(c.get('effective_string_tension', 0.0)))}`",
        f"- spark_string_break: `{_fmt(float(c.get('spark_string_break', 0.0)))}`",
        f"- string_break_fraction: `{_fmt(float(c.get('string_break_fraction', 0.0)))}`",
        f"- proton: `{_fmt(float(c.get('proton', 0.0)))}`",
        f"- electron: `{_fmt(float(c.get('electron', 0.0)))}`",
        f"- coulomb_barrier_proxy: `{_fmt(float(c.get('coulomb_barrier_proxy', 0.0)))}`",
        f"- z_boson_proxy: `{_fmt(float(c.get('z_boson_proxy', 0.0)))}`",
        f"- gain_beta_decay: `{_fmt(float(c.get('gain_beta_decay', 0.0)))}`",
        "",
        "## Equation",
        f"- `{out.get('equation','')}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

