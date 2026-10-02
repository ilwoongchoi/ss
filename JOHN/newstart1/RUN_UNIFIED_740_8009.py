from __future__ import annotations

import argparse
import json

from fusion_clean import edge_stack_master_step


def main() -> int:
    p = argparse.ArgumentParser(description="Unified 7.4/0.8009 operator runner")
    p.add_argument("--bm", type=float, default=0.2)
    p.add_argument("--bw", type=float, default=0.3)
    p.add_argument("--sm", type=float, default=0.1)
    p.add_argument("--sw", type=float, default=0.15)
    p.add_argument("--phase-fill", type=float, default=0.42)
    p.add_argument("--clock", type=str, default="13:30")
    p.add_argument("--quark-order", type=float, default=3.5)
    p.add_argument("--neutrino-order", type=float, default=2.5)
    p.add_argument("--efficiency", type=float, default=0.8009)
    args = p.parse_args()

    state4 = [args.bm, args.bw, args.sm, args.sw]
    out = edge_stack_master_step(
        state4,
        phase_fill=args.phase_fill,
        clock_hhmm=args.clock,
        enable_unified_operator=True,
        quark_order=args.quark_order,
        neutrino_order=args.neutrino_order,
        efficiency_target=args.efficiency,
    )

    summary = {
        "state_in": state4,
        "state_out": [float(x) for x in out["state_out"]],
        "omega_out": float(out["omega_out"]),
        "psi_sovereign": float(out["psi_sovereign"]),
        "closure_error_to_7_4": float(out["closure_error"]),
        "quark_order": float(out["quark_order"]),
        "neutrino_order": float(out["neutrino_order"]),
        "efficiency_target": float(out["efficiency_target"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
