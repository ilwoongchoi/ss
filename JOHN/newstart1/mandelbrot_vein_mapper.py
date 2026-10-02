
import os
import json
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import csr_matrix

# 1. CANONICAL CONSTANTS & CONFIG
try:
    from absolute_constants import C, SPARK_ANGLE_RAD
except ImportError:
    C = float(np.sqrt(2.0) / 5.0)
    SPARK_ANGLE_RAD = np.deg2rad(138.88)


def _try_load_geometry_constants():
    try:
        import geometry_package.absolute_constants as gc  # type: ignore

        return gc
    except Exception:
        return None


_GC = _try_load_geometry_constants()

OMEGA = 7.4
DELTA_T_OBS = float(getattr(_GC, "DELTA_T_OBS_DERIVED", 99.0 / 350.0)) if _GC else (99.0 / 350.0)
EPSILON0 = (C**2) / 128.0

PHASES = {
    "phase1":     {"spark": 0.7625,  "Z": 0.8175},
    "phase2":     {"spark": 1.0125,  "Z": 0.6375},
    "hysteresis": {"spark": 0.5825,  "Z": 1.3475},
}
C1 = complex(PHASES["phase1"]["spark"]/OMEGA,     PHASES["phase1"]["Z"]/OMEGA)
C2 = complex(PHASES["phase2"]["spark"]/OMEGA,     PHASES["phase2"]["Z"]/OMEGA)
C3 = complex(PHASES["hysteresis"]["spark"]/OMEGA, PHASES["hysteresis"]["Z"]/OMEGA)
C_FUSION_AVG = (C1 + C2 + C3) / 3.0

C_MANDELBROT = complex(math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD))

MODES = ["mandelbrot", "fusion_1c", "fusion_3c"]


def _leak_value(leak_mode: str) -> float:
    leak_mode = str(leak_mode or "none").lower().strip()
    if leak_mode == "none":
        return 0.0
    if leak_mode == "locked":
        if _GC is not None and hasattr(_GC, "OMEGA_SLOTTING_DELTA"):
            return float(_GC.OMEGA_SLOTTING_DELTA)
        return 0.076
    if leak_mode == "derived":
        if _GC is not None and hasattr(_GC, "DRIFT_FROM_GAP_11_OVER_8"):
            return float(_GC.DRIFT_FROM_GAP_11_OVER_8)
        return (11.0 / 8.0) / 18.0
    raise ValueError(f"Unknown leak mode: {leak_mode!r}")


def _epsilon_extra_value(epsilon_mode: str) -> float:
    epsilon_mode = str(epsilon_mode or "none").lower().strip()
    if epsilon_mode == "none":
        return 0.0
    if epsilon_mode == "resid_5_32":
        if _GC is not None and hasattr(_GC, "RESID_DATA_5_32"):
            return float(_GC.RESID_DATA_5_32)
        # fallback: purely geometric mismatch (pi/20 - 5/32)
        return float((math.pi / 20.0) - (5.0 / 32.0))
    if epsilon_mode == "pi_over_20_minus_5_32":
        return float((math.pi / 20.0) - (5.0 / 32.0))
    raise ValueError(f"Unknown epsilon mode: {epsilon_mode!r}")


# 2. CORE KERNEL
def iterate_kernel(
    z,
    c_pixel,
    plane="julia",
    mode="mandelbrot",
    julia_c_override=None,
    max_iter=100,
    escape_r=10.0,
    leak=0.0,
    epsilon_extra=0.0,
):
    """
    z_{n+1} = (z_n^2 * exp(i*DELTA_T_OBS) + c_eff) * (1 - C) + (EPSILON0 + epsilon_extra) - i*leak
    """
    rot = complex(math.cos(DELTA_T_OBS), math.sin(DELTA_T_OBS))
    damping = (1.0 - C)
    epsilon = float(EPSILON0 + float(epsilon_extra))
    leak = float(leak)
    
    # Determine base c_eff for Julia plane or use c_pixel for Mandelbrot plane.
    # If julia_c_override is provided, it replaces the mode-specific Julia constant.
    if plane == "mandelbrot":
        base_c = c_pixel
    else:
        if julia_c_override is not None:
            base_c = complex(julia_c_override)
        else:
            if mode == "mandelbrot":
                base_c = C_MANDELBROT
            elif mode == "fusion_1c":
                base_c = C_FUSION_AVG
            else: # fusion_3c
                base_c = None # Will be set per iteration
            
    potential = 0.0
    for n in range(max_iter):
        if abs(z) > escape_r:
            potential = n + 1 - math.log2(max(1e-9, math.log2(abs(z))))
            return potential
        
        if mode == "fusion_3c" and julia_c_override is None:
            c_eff = [C1, C2, C3][n % 3] if plane == "julia" else c_pixel # Simplification for M-plane
        else:
            c_eff = base_c
            
        z = (z**2 * rot + c_eff) * damping + epsilon - 1j * leak
        
    return max_iter

# 3. FIELD GENERATION
def generate_field(
    mode="mandelbrot",
    plane="mandelbrot",
    julia_c_override=None,
    res=150,
    x_range=(-2, 2),
    y_range=(-2, 2),
    max_iter=100,
    escape_r=10.0,
    leak=0.0,
    epsilon_extra=0.0,
):
    x = np.linspace(x_range[0], x_range[1], res)
    y = np.linspace(y_range[0], y_range[1], res)
    X, Y = np.meshgrid(x, y)
    Z_field = np.zeros_like(X)
    
    for i in range(res):
        for j in range(res):
            pixel = complex(X[i, j], Y[i, j])
            if plane == "julia":
                Z_field[i, j] = iterate_kernel(
                    pixel,
                    None,
                    plane="julia",
                    mode=mode,
                    julia_c_override=julia_c_override,
                    max_iter=max_iter,
                    escape_r=escape_r,
                    leak=leak,
                    epsilon_extra=epsilon_extra,
                )
            else: # mandelbrot plane
                Z_field[i, j] = iterate_kernel(
                    0j,
                    pixel,
                    plane="mandelbrot",
                    mode=mode,
                    max_iter=max_iter,
                    escape_r=escape_r,
                    leak=leak,
                    epsilon_extra=epsilon_extra,
                )
                
    return X, Y, Z_field

# 4. VEIN EXTRACTION & GRAPH
def extract_veins(X, Y, G, num_levels=30):
    # Check if field is constant
    if np.allclose(G, G[0,0]):
        return []
        
    fig, ax = plt.subplots()
    try:
        contours = ax.contour(X, Y, G, levels=num_levels)
        polylines = []
        for path in contours.get_paths():
            v = path.vertices
            if len(v) > 1:
                polylines.append(v.tolist())
    except Exception as e:
        print(f"Contour extraction failed: {e}")
        polylines = []
    finally:
        plt.close(fig)
    return polylines

def build_vein_graph(polylines):
    nodes = []
    poly_edges = []
    tunnel_edges = []
    
    for poly in polylines:
        p_indices = []
        for pt in poly:
            idx = len(nodes)
            nodes.append(pt)
            p_indices.append(idx)
        for i in range(len(p_indices) - 1):
            poly_edges.append((p_indices[i], p_indices[i+1]))
            
    stats = {
        "components_before": 0,
        "components_after": 0,
        "total_length": 0.0,
        "poly_total_length": 0.0,
        "tunnel_total_length": 0.0,
        "poly_edges_count": 0,
        "tunnel_edges_count": 0,
        "holes": 0
    }
    
    if not nodes:
        return {"nodes": [], "edges": [], "poly_edges": [], "tunnel_edges": [], "stats": stats}

    components = []
    curr_idx = 0
    for poly in polylines:
        components.append(list(range(curr_idx, curr_idx + len(poly))))
        curr_idx += len(poly)
        
    stats["components_before"] = len(components)
    
    if len(components) > 1:
        comp_points = np.array([nodes[c[0]] for c in components])
        dist_matrix = np.sqrt(np.sum((comp_points[:, None] - comp_points[None, :])**2, axis=-1))
        mst = minimum_spanning_tree(dist_matrix).toarray()
        
        sources, targets = np.where(mst > 0)
        for s, t in zip(sources, targets):
            tunnel_edges.append((components[s][0], components[t][0]))
             
    stats["components_after"] = 1 if len(components) > 0 else 0

    def _edge_len(e):
        (a, b) = e
        return math.hypot(nodes[a][0] - nodes[b][0], nodes[a][1] - nodes[b][1])

    poly_total_length = sum(_edge_len(e) for e in poly_edges)
    tunnel_total_length = sum(_edge_len(e) for e in tunnel_edges)
    stats["poly_total_length"] = float(poly_total_length)
    stats["tunnel_total_length"] = float(tunnel_total_length)
    stats["poly_edges_count"] = int(len(poly_edges))
    stats["tunnel_edges_count"] = int(len(tunnel_edges))
    stats["total_length"] = float(poly_total_length + tunnel_total_length)

    edges = poly_edges + tunnel_edges
             
    return {
        "nodes": nodes,
        "edges": edges,
        "poly_edges": poly_edges,
        "tunnel_edges": tunnel_edges,
        "stats": stats
    }

# 5. MAIN EXECUTION
def main():
    parser = argparse.ArgumentParser(description="Generate Mandelbrot/Julia vein mappings from the canonical origin kernel.")
    parser.add_argument("--out", default="analysis_results/veins_pocket_tunnel", help="Output directory")
    parser.add_argument("--res", type=int, default=150, help="Grid resolution per axis")
    parser.add_argument("--levels", type=int, default=30, help="Contour levels")
    parser.add_argument("--max-iter", type=int, default=100, help="Max iterations per pixel")
    parser.add_argument("--escape-r", type=float, default=10.0, help="Escape radius")
    parser.add_argument("--leak", choices=["none", "locked", "derived"], default="locked", help="Imaginary leak term mode")
    parser.add_argument(
        "--epsilon",
        choices=["none", "resid_5_32", "pi_over_20_minus_5_32"],
        default="resid_5_32",
        help="Extra real epsilon injection mode",
    )
    parser.add_argument("--modes", default=",".join(MODES), help="Comma-separated subset of modes")
    parser.add_argument("--planes", default="julia,mandelbrot", help="Comma-separated subset of planes")
    args = parser.parse_args()

    out_dir = str(args.out)
    os.makedirs(out_dir, exist_ok=True)

    leak = _leak_value(args.leak)
    epsilon_extra = _epsilon_extra_value(args.epsilon)
    
    # Range for Mandelbrot set
    m_range = (-2.5, 1.5, -2, 2)
    # Range for Julia set
    j_range = (-2, 2, -2, 2)
    
    selected_modes = [m.strip() for m in str(args.modes).split(",") if m.strip()]
    selected_planes = [p.strip() for p in str(args.planes).split(",") if p.strip()]

    meta = {
        "C": float(C),
        "EPSILON0": float(EPSILON0),
        "DELTA_T_OBS": float(DELTA_T_OBS),
        "leak_mode": args.leak,
        "leak_value": float(leak),
        "epsilon_mode": args.epsilon,
        "epsilon_extra": float(epsilon_extra),
        "res": int(args.res),
        "levels": int(args.levels),
        "max_iter": int(args.max_iter),
        "escape_r": float(args.escape_r),
        "modes": selected_modes,
        "planes": selected_planes,
    }
    with open(os.path.join(out_dir, "run_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    for mode in selected_modes:
        if mode not in MODES:
            raise ValueError(f"Unknown mode: {mode!r} (allowed: {MODES})")
        for plane in selected_planes:
            if plane not in ("julia", "mandelbrot"):
                raise ValueError(f"Unknown plane: {plane!r} (allowed: julia, mandelbrot)")
            print(f"Processing mode: {mode}, plane: {plane}")
            r = m_range if plane == "mandelbrot" else j_range
            X, Y, G = generate_field(
                mode=mode,
                plane=plane,
                res=int(args.res),
                x_range=(r[0], r[1]),
                y_range=(r[2], r[3]),
                max_iter=int(args.max_iter),
                escape_r=float(args.escape_r),
                leak=leak,
                epsilon_extra=epsilon_extra,
            )
            
            polylines = extract_veins(X, Y, G, num_levels=int(args.levels))
            graph = build_vein_graph(polylines)
            
            suffix = f"{mode}_{plane}"
            out_png = os.path.join(out_dir, f"veins_{suffix}.png")
            plt.figure(figsize=(10, 10))
            if polylines:
                for poly in polylines:
                    p = np.array(poly)
                    plt.plot(p[:, 0], p[:, 1], 'b-', alpha=0.5, linewidth=0.5)
            else:
                plt.text(0.5, 0.5, "No Veins Found", ha='center', va='center')
            plt.title(f"Vein Mapping - {suffix}")
            plt.savefig(out_png)
            plt.close()
             
            with open(os.path.join(out_dir, f"veins_{suffix}_polylines.json"), "w", encoding="utf-8") as f:
                json.dump(polylines, f, ensure_ascii=False)
                 
            with open(os.path.join(out_dir, f"veins_{suffix}_graph.json"), "w", encoding="utf-8") as f:
                json.dump(graph, f, ensure_ascii=False)
                 
            print(f"Finished {suffix}. Components: {graph['stats']['components_after']}, Total Length: {graph['stats']['total_length']:.2f}")

if __name__ == "__main__":
    main()
