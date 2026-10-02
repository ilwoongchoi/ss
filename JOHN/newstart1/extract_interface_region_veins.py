import argparse
import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mandelbrot_vein_mapper import (
    SPARK_ANGLE_RAD,
    _epsilon_extra_value,
    _leak_value,
    build_vein_graph,
    extract_veins,
    generate_field,
)
from run_biophysics_interface_grid_128x128 import _load_sim_d3_grid, _safe_float, _window_params


@dataclass(frozen=True)
class Region:
    name: str
    w0: int
    w1: int
    n0: int
    n1: int


def _parse_region(text: str) -> Region:
    parts = [p.strip() for p in str(text or "").split(",") if p.strip()]
    if len(parts) != 5:
        raise ValueError(
            "Region must be 'name,w_start,w_end,n_start,n_end' (example: escape,120,127,1,16)"
        )
    name = parts[0]
    w0 = int(parts[1])
    w1 = int(parts[2])
    n0 = int(parts[3])
    n1 = int(parts[4])
    if not (0 <= w0 <= 127 and 0 <= w1 <= 127 and w0 <= w1):
        raise ValueError(f"Invalid window range: {w0}..{w1}")
    if not (1 <= n0 <= 128 and 1 <= n1 <= 128 and n0 <= n1):
        raise ValueError(f"Invalid n range: {n0}..{n1}")
    return Region(name=name, w0=w0, w1=w1, n0=n0, n1=n1)


def _plot_polylines(polylines: list[list[list[float]]], title: str, out_png: Path) -> None:
    plt.figure(figsize=(8, 8))
    if polylines:
        for poly in polylines:
            p = np.asarray(poly, dtype=float)
            if p.ndim == 2 and p.shape[0] >= 2:
                plt.plot(p[:, 0], p[:, 1], "b-", alpha=0.55, linewidth=0.6)
    else:
        plt.text(0.5, 0.5, "No Veins Found", ha="center", va="center")
    plt.title(title)
    plt.axis("equal")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract full Julia-plane veins for selected (window,n) regions using the bio/physics interface mapping."
    )
    parser.add_argument("--bio-schedule", default="HOMEOSTASIS_24_SCHEDULE_128.csv")
    parser.add_argument("--sim-results", default="analysis_results/CONSCIOUSNESS_FIELD_128x128.csv")
    parser.add_argument("--sim-window-col", default="step")
    parser.add_argument("--sim-n-col", default="archetype_n")
    parser.add_argument("--sim-d3-col", default="d3_actual")
    parser.add_argument(
        "--out",
        default="analysis_results/veins_pocket_tunnel/interface_128/region_veins",
        help="Output directory",
    )
    parser.add_argument("--maps", default="real,spark_ray", help="Comma-separated subset: real,spark_ray")
    parser.add_argument("--base-leak", choices=["none", "locked", "derived"], default="locked")
    parser.add_argument("--base-epsilon", choices=["none", "resid_5_32", "pi_over_20_minus_5_32"], default="resid_5_32")
    parser.add_argument("--leak-return-scale", type=float, default=1.0)
    parser.add_argument("--epsilon-mask-scale", type=float, default=1.0)
    parser.add_argument("--c-gain-scale", type=float, default=1.0)
    parser.add_argument("--collapse-scale", type=float, default=0.02)
    parser.add_argument(
        "--collapse-col",
        default="",
        help="Optional: use this bio schedule column as collapse proxy (used only when sim d3 is missing).",
    )
    parser.add_argument(
        "--regions",
        action="append",
        default=[
            "escape_heart,120,127,1,16",
            "collapse_heart,60,70,120,128",
        ],
        help="Repeatable region spec: name,w0,w1,n0,n1",
    )
    parser.add_argument("--res", type=int, default=96, help="Grid resolution per axis")
    parser.add_argument("--levels", type=int, default=28, help="Contour levels")
    parser.add_argument("--max-iter", type=int, default=100, help="Max iterations per pixel")
    parser.add_argument("--escape-r", type=float, default=10.0, help="Escape radius")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    selected_maps = [m.strip() for m in str(args.maps).split(",") if m.strip()]
    for m in selected_maps:
        if m not in ("real", "spark_ray"):
            raise ValueError(f"Unknown map mode: {m!r} (allowed: real,spark_ray)")

    regions = [_parse_region(r) for r in (args.regions or [])]

    df_bio = pd.read_csv(args.bio_schedule)
    if "window" not in df_bio.columns:
        raise ValueError("bio schedule must include 'window' column (0..127).")
    df_bio = df_bio.copy()
    df_bio["window"] = df_bio["window"].astype(int)
    df_bio = df_bio.sort_values("window").reset_index(drop=True)
    if df_bio["window"].tolist() != list(range(128)):
        raise ValueError("bio schedule must cover window=0..127 exactly.")

    base_leak = float(_leak_value(args.base_leak))
    base_epsilon_extra = float(_epsilon_extra_value(args.base_epsilon))
    collapse_col = str(args.collapse_col).strip() or None

    sim_d3_grid = _load_sim_d3_grid(
        str(args.sim_results).strip(),
        window_col=str(args.sim_window_col),
        n_col=str(args.sim_n_col),
        d3_col=str(args.sim_d3_col),
    )
    sim_available = sim_d3_grid is not None and int(np.isfinite(sim_d3_grid).sum()) > 0

    # Precompute per-window params (bio modulation components)
    windows = [
        _window_params(
            row=row,
            base_leak=base_leak,
            base_epsilon_extra=base_epsilon_extra,
            leak_return_scale=float(args.leak_return_scale),
            epsilon_mask_scale=float(args.epsilon_mask_scale),
            c_gain_scale=float(args.c_gain_scale),
            collapse_col=collapse_col,
        )
        for _, row in df_bio.iterrows()
    ]
    win_by_idx = {int(w.window): w for w in windows}

    spark_ray_unit = complex(math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD))
    map_unit = {"real": 1.0 + 0.0j, "spark_ray": spark_ray_unit}

    manifest_rows: list[dict[str, object]] = []
    t0 = time.perf_counter()

    for region in regions:
        region_dir = out_dir / region.name
        region_dir.mkdir(parents=True, exist_ok=True)

        for window in range(region.w0, region.w1 + 1):
            w = win_by_idx[int(window)]

            for n in range(region.n0, region.n1 + 1):
                # Collapse driver: prefer simulation d3_actual per cell; fallback to schedule proxy
                collapse_source = str(w.collapse_proxy_source)
                collapse_value = float(w.collapse_proxy_value)
                if sim_available:
                    d3 = float(sim_d3_grid[int(window), int(n) - 1])
                    if math.isfinite(d3):
                        collapse_source = f"sim:{str(args.sim_d3_col)}"
                        collapse_value = d3

                leak_total = base_leak + float(w.leak_return) + float(args.collapse_scale) * float(collapse_value)
                epsilon_extra = float(w.epsilon_extra_total)
                c_base = float(n) / 128.0
                c_gain = float(w.c_gain)

                for map_mode in selected_maps:
                    c_eff = (c_gain * c_base) * map_unit[map_mode]

                    stem = f"{region.name}_w{int(window):03d}_n{int(n):03d}_{map_mode}"
                    out_png = region_dir / f"{stem}.png"
                    out_poly = region_dir / f"{stem}_polylines.json"
                    out_graph = region_dir / f"{stem}_graph.json"
                    out_meta = region_dir / f"{stem}_meta.json"

                    if out_graph.exists() and out_poly.exists() and out_png.exists() and out_meta.exists():
                        continue

                    X, Y, G = generate_field(
                        mode="mandelbrot",
                        plane="julia",
                        julia_c_override=c_eff,
                        res=int(args.res),
                        x_range=(-2, 2),
                        y_range=(-2, 2),
                        max_iter=int(args.max_iter),
                        escape_r=float(args.escape_r),
                        leak=float(leak_total),
                        epsilon_extra=float(epsilon_extra),
                    )
                    polylines = extract_veins(X, Y, G, num_levels=int(args.levels))
                    graph = build_vein_graph(polylines)

                    _plot_polylines(
                        polylines,
                        title=f"{region.name} w={window} n={n} {map_mode}",
                        out_png=out_png,
                    )
                    out_poly.write_text(json.dumps(polylines, ensure_ascii=False), encoding="utf-8")
                    out_graph.write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")

                    meta = {
                        "region": region.name,
                        "window": int(window),
                        "n": int(n),
                        "map_mode": str(map_mode),
                        "kernel": {
                            "res": int(args.res),
                            "levels": int(args.levels),
                            "max_iter": int(args.max_iter),
                            "escape_r": float(args.escape_r),
                            "base_leak_mode": str(args.base_leak),
                            "base_leak_value": float(base_leak),
                            "base_epsilon_mode": str(args.base_epsilon),
                            "base_epsilon_extra": float(base_epsilon_extra),
                            "collapse_scale": float(args.collapse_scale),
                        },
                        "bio_window_params": {
                            "u_male_gaba_b": float(w.u_male_gaba_b),
                            "u_right_occipitalis_gaba_a": float(w.u_right_occipitalis_gaba_a),
                            "u_female_left_noradrenaline": float(w.u_female_left_noradrenaline),
                            "c_gain": float(c_gain),
                            "epsilon_extra_total": float(epsilon_extra),
                            "leak_return": float(w.leak_return),
                            "collapse_proxy_source": str(w.collapse_proxy_source),
                            "collapse_proxy_value": float(w.collapse_proxy_value),
                        },
                        "cell_params": {
                            "c_base": float(c_base),
                            "c_eff_re": float(np.real(c_eff)),
                            "c_eff_im": float(np.imag(c_eff)),
                            "leak_total": float(leak_total),
                            "collapse_source": str(collapse_source),
                            "collapse_value": float(collapse_value),
                        },
                        "outputs": {
                            "png": str(out_png),
                            "polylines_json": str(out_poly),
                            "graph_json": str(out_graph),
                        },
                        "graph_stats": graph.get("stats", {}),
                    }
                    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

                    manifest_rows.append(
                        {
                            "region": region.name,
                            "window": int(window),
                            "n": int(n),
                            "map_mode": str(map_mode),
                            "c_gain": float(c_gain),
                            "c_eff_re": float(np.real(c_eff)),
                            "c_eff_im": float(np.imag(c_eff)),
                            "leak_total": float(leak_total),
                            "epsilon_extra_total": float(epsilon_extra),
                            "collapse_source": str(collapse_source),
                            "collapse_value": float(collapse_value),
                            "collapse_proxy_value": float(w.collapse_proxy_value),
                            "polylines": int(len(polylines)),
                            "poly_edges": int(graph.get("stats", {}).get("poly_edges_count", 0)),
                            "tunnel_edges": int(graph.get("stats", {}).get("tunnel_edges_count", 0)),
                            "poly_total_length": float(graph.get("stats", {}).get("poly_total_length", 0.0)),
                            "tunnel_total_length": float(graph.get("stats", {}).get("tunnel_total_length", 0.0)),
                            "total_length": float(graph.get("stats", {}).get("total_length", 0.0)),
                            "graph_json": str(out_graph),
                            "png": str(out_png),
                        }
                    )

            print(f"region={region.name} window={window} done")

    seconds = float(time.perf_counter() - t0)

    manifest_path = out_dir / "region_veins_manifest.csv"
    if manifest_rows:
        pd.DataFrame(manifest_rows).to_csv(manifest_path, index=False)

    run_meta = {
        "bio_schedule": str(args.bio_schedule),
        "sim_results": str(args.sim_results),
        "sim_columns": {"window": str(args.sim_window_col), "n": str(args.sim_n_col), "d3": str(args.sim_d3_col)},
        "sim_available": bool(sim_available),
        "maps": selected_maps,
        "regions": [region.__dict__ for region in regions],
        "runtime_seconds": seconds,
        "manifest_csv": str(manifest_path) if manifest_rows else None,
    }
    (out_dir / "region_veins_run_meta.json").write_text(
        json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nWrote: {out_dir / 'region_veins_run_meta.json'}")
    if manifest_rows:
        print(f"Wrote: {manifest_path}")
    print(f"Runtime: {seconds:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

