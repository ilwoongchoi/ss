import argparse
import csv
import math
import os
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

from mandelbrot_vein_mapper import (
    SPARK_ANGLE_RAD,
    _epsilon_extra_value,
    _leak_value,
    build_vein_graph,
    extract_veins,
    generate_field,
)


@dataclass(frozen=True)
class SweepRow:
    n: int
    c_re: float
    c_im: float
    c_abs: float
    c_arg: float
    polylines: int
    nodes: int
    poly_total_length: float
    tunnel_total_length: float
    tunnel_edges: int
    seconds: float


def _polyline_total_length(polylines: list[list[list[float]]]) -> tuple[float, int]:
    total = 0.0
    node_count = 0
    for poly in polylines:
        node_count += len(poly)
        for i in range(len(poly) - 1):
            (x0, y0) = poly[i]
            (x1, y1) = poly[i + 1]
            total += math.hypot(x1 - x0, y1 - y0)
    return float(total), int(node_count)


def _mst_tunnel_length(polylines: list[list[list[float]]], max_components: int) -> tuple[float, int]:
    if len(polylines) <= 1:
        return 0.0, 0
    if len(polylines) > max_components:
        return 0.0, 0

    comp_points = np.asarray([poly[0] for poly in polylines], dtype=float)
    diff = comp_points[:, None, :] - comp_points[None, :, :]
    dist = np.sqrt(np.sum(diff * diff, axis=-1))

    mst = minimum_spanning_tree(dist).tocoo()
    return float(mst.data.sum()), int(mst.nnz)


def _c_for_n(n: int, map_mode: str) -> complex:
    x = float(n) / 128.0
    map_mode = str(map_mode or "real").lower().strip()
    if map_mode == "real":
        return complex(x, 0.0)
    if map_mode == "spark_ray":
        return x * complex(math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD))
    raise ValueError(f"Unknown map mode: {map_mode!r}")


def _parse_int_set(text: str) -> set[int]:
    out: set[int] = set()
    for chunk in str(text or "").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        out.add(int(chunk))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep n=1..128 and measure vein metrics for Julia constants c(n).")
    parser.add_argument("--out", default="analysis_results/veins_pocket_tunnel/sweep_128", help="Output directory")
    parser.add_argument("--map", choices=["real", "spark_ray"], default="real", help="c(n) mapping")
    parser.add_argument("--res", type=int, default=64, help="Grid resolution per axis")
    parser.add_argument("--levels", type=int, default=20, help="Contour levels")
    parser.add_argument("--max-iter", type=int, default=80, help="Max iterations per pixel")
    parser.add_argument("--escape-r", type=float, default=10.0, help="Escape radius")
    parser.add_argument("--leak", choices=["none", "locked", "derived"], default="locked", help="Imaginary leak mode")
    parser.add_argument(
        "--epsilon",
        choices=["none", "resid_5_32", "pi_over_20_minus_5_32"],
        default="resid_5_32",
        help="Extra real epsilon injection mode",
    )
    parser.add_argument(
        "--save-graphs",
        default="1,7,8,16,32,64,128",
        help="Comma-separated n values for which to save full graph+png outputs",
    )
    parser.add_argument("--save-all", action="store_true", help="Save graph+png for every n (large output)")
    parser.add_argument(
        "--mst-max-components",
        type=int,
        default=800,
        help="Skip MST tunnel length if polylines exceed this count",
    )
    args = parser.parse_args()

    out_dir = str(args.out)
    os.makedirs(out_dir, exist_ok=True)

    leak = _leak_value(args.leak)
    epsilon_extra = _epsilon_extra_value(args.epsilon)

    wanted_graphs = _parse_int_set(args.save_graphs)
    rows: list[SweepRow] = []

    # Julia plane view range
    j_x = (-2.0, 2.0)
    j_y = (-2.0, 2.0)

    csv_path = os.path.join(out_dir, f"sweep_128_{args.map}.csv")
    meta_path = os.path.join(out_dir, f"sweep_128_{args.map}_meta.json")

    meta = {
        "map": args.map,
        "res": int(args.res),
        "levels": int(args.levels),
        "max_iter": int(args.max_iter),
        "escape_r": float(args.escape_r),
        "leak_mode": args.leak,
        "leak_value": float(leak),
        "epsilon_mode": args.epsilon,
        "epsilon_extra": float(epsilon_extra),
        "spark_angle_rad": float(SPARK_ANGLE_RAD),
        "save_graphs": sorted(list(wanted_graphs)),
        "save_all": bool(args.save_all),
        "mst_max_components": int(args.mst_max_components),
    }
    try:
        import json

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "n",
                "c_re",
                "c_im",
                "c_abs",
                "c_arg",
                "polylines",
                "nodes",
                "poly_total_length",
                "tunnel_total_length",
                "tunnel_edges",
                "seconds",
            ]
        )

        for n in range(1, 129):
            t0 = time.perf_counter()
            c = _c_for_n(n, args.map)

            X, Y, G = generate_field(
                mode="mandelbrot",
                plane="julia",
                julia_c_override=c,
                res=int(args.res),
                x_range=j_x,
                y_range=j_y,
                max_iter=int(args.max_iter),
                escape_r=float(args.escape_r),
                leak=float(leak),
                epsilon_extra=float(epsilon_extra),
            )
            polylines = extract_veins(X, Y, G, num_levels=int(args.levels))
            poly_total_length, node_count = _polyline_total_length(polylines)
            tunnel_total_length, tunnel_edges = _mst_tunnel_length(polylines, int(args.mst_max_components))

            seconds = float(time.perf_counter() - t0)
            row = SweepRow(
                n=n,
                c_re=float(c.real),
                c_im=float(c.imag),
                c_abs=float(abs(c)),
                c_arg=float(math.atan2(c.imag, c.real)),
                polylines=int(len(polylines)),
                nodes=int(node_count),
                poly_total_length=float(poly_total_length),
                tunnel_total_length=float(tunnel_total_length),
                tunnel_edges=int(tunnel_edges),
                seconds=seconds,
            )
            rows.append(row)

            w.writerow(
                [
                    row.n,
                    f"{row.c_re:.12g}",
                    f"{row.c_im:.12g}",
                    f"{row.c_abs:.12g}",
                    f"{row.c_arg:.12g}",
                    row.polylines,
                    row.nodes,
                    f"{row.poly_total_length:.12g}",
                    f"{row.tunnel_total_length:.12g}",
                    row.tunnel_edges,
                    f"{row.seconds:.6f}",
                ]
            )
            f.flush()

            should_save = bool(args.save_all) or (n in wanted_graphs)
            if should_save:
                graph = build_vein_graph(polylines)
                base = f"veins_sweep_{args.map}_n{n:03d}"

                # Save polyline + graph JSON
                try:
                    import json

                    with open(os.path.join(out_dir, f"{base}_polylines.json"), "w", encoding="utf-8") as jf:
                        json.dump(polylines, jf, ensure_ascii=False)
                    with open(os.path.join(out_dir, f"{base}_graph.json"), "w", encoding="utf-8") as jf:
                        json.dump(graph, jf, ensure_ascii=False)
                except Exception:
                    pass

                # Save PNG
                out_png = os.path.join(out_dir, f"{base}.png")
                plt.figure(figsize=(7, 7))
                if polylines:
                    for poly in polylines:
                        p = np.asarray(poly, dtype=float)
                        plt.plot(p[:, 0], p[:, 1], "b-", alpha=0.55, linewidth=0.5)
                else:
                    plt.text(0.5, 0.5, "No Veins Found", ha="center", va="center")
                plt.title(f"Julia veins: n={n}  c={c.real:.5f}{c.imag:+.5f}i")
                plt.xlim(j_x[0], j_x[1])
                plt.ylim(j_y[0], j_y[1])
                plt.gca().set_aspect("equal", adjustable="box")
                plt.grid(True, alpha=0.2)
                plt.tight_layout()
                plt.savefig(out_png, dpi=140)
                plt.close()

            print(
                f"n={n:3d} polylines={row.polylines:4d} length={row.poly_total_length:10.2f} "
                f"mst={row.tunnel_total_length:8.2f} sec={row.seconds:6.2f}"
            )

    # Summary plot
    try:
        n_vals = [r.n for r in rows]
        poly_len = [r.poly_total_length for r in rows]
        poly_cnt = [r.polylines for r in rows]
        tunnel_len = [r.tunnel_total_length for r in rows]

        fig, ax1 = plt.subplots(figsize=(11, 5))
        ax1.plot(n_vals, poly_len, color="#00d0ff", lw=1.6, label="poly_total_length")
        ax1.plot(n_vals, tunnel_len, color="#ffb000", lw=1.2, alpha=0.9, label="mst_tunnel_length")
        ax1.set_xlabel("n (1..128)")
        ax1.set_ylabel("length")
        ax1.grid(True, alpha=0.2)

        ax2 = ax1.twinx()
        ax2.plot(n_vals, poly_cnt, color="#00ff6a", lw=1.2, alpha=0.9, label="polylines")
        ax2.set_ylabel("polyline count")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
        plt.title(f"Vein sweep (Julia) map={args.map}  res={args.res} levels={args.levels}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"sweep_128_{args.map}_summary.png"), dpi=160)
        plt.close(fig)
    except Exception:
        pass

    print(f"\nWrote: {csv_path}")
    print(f"Wrote: {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

