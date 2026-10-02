"""
generate_128x128_grid.py
Generates 128-window × 128-element state classification grid.

Rows   = 128 time windows (0=midnight, 11.25 min each)
Cols   = Z = 1..128  (atomic number / 128ELEMENTS)

For each cell (w, Z):
  - Uses trajectory BW(w), SM(w), spark(w), Z_proxy(w) from sovereign sim
  - gate(Z) = cos(Z * 138.88deg + 1/128 rad)
  - decay(Z) = exp(-sqrt(Z) / 64)
  - F_eff = BW^2 * spark * gate * Z_proxy * SM * decay

State codes:
  I = IDEAL        gate>0.95, alpha2 OFF  (perfect fusion ignition)
  J = JUSTICE      gate>0.95, alpha2 ON   (BW capture, gravity/user state)
  C = COLLAPSE     gate < -0.80           (anti-fusion, destructive)
  P = PRA          gate in (0.5,0.95), hysteresis/phase2, high Z_proxy
  B = BREMSS       spark>0.4, gate in (0.1,0.5) (photon emission, partial)
  L = LENSING      phase1, BW dominant, gate <= 0   (gravitational analog)
  N = NEUTRON_STAR hysteresis, Z_proxy > 0.8, gate < 0 (neutrino collapse)
  H = HIGGS        night + |gate|<0.4   (0.2828 background field)
  S = SLOTTING     transition connector
  . = baseline
"""
from __future__ import annotations
import sys, json, math
import numpy as np
from pathlib import Path

# ── add project root to path ───────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from fusion_core import (
    apply_channels, laplacian, project4,
    day_target, night_target, init_state6_from_target4,
    CHANNEL_MAP, OMEGA, C,
)

# ── re-use sovereign_128 schedule ─────────────────────────────────────────
from sovereign_128 import get_channels, N_WINDOWS, SUBSTEPS, DT, ATTRACTOR_K

SPARK_ANGLE_RAD = 138.88 * (math.pi / 180.0)
SPARK_LEAK      = 1.0 / 128.0
AGE             = 25.0

# ── 1. run 128-window trajectory to get BW(w), SM(w), etc. ────────────────

def run_trajectory(age=AGE):
    t4_day   = day_target()
    t4_night = night_target()
    x = init_state6_from_target4(t4_day)

    rows = []
    for w in range(N_WINDOWS):
        ch  = get_channels(w)
        wts = apply_channels(ch, age=age)
        L   = laplacian(wts)
        is_n = (w < 36) or (w >= 104)
        x_att = init_state6_from_target4(t4_night if is_n else t4_day)
        for _ in range(SUBSTEPS):
            dx = -(L @ x) + ATTRACTOR_K * (x_att - x)
            x  = x + DT * dx
            x  = np.clip(x, 1e-8, 50.0)
        x4 = project4(x)
        BM, BW, SM, SW = x4
        spark   = wts.get(("photon","proton"), 0.0) + wts.get(("photon","electron"), 0.0)
        z_proxy = wts.get(("neutrino","proton"), 0.0) + wts.get(("neutrino","electron"), 0.0)
        alpha2  = ch.get("right_alpha_2", "on")
        rows.append({
            "w":w, "BW":BW, "SM":SM, "BM":BM, "SW":SW,
            "spark":spark, "z_proxy":z_proxy, "alpha2":alpha2,
            "is_night": (w < 36) or (w >= 104),
            "in_hysteresis": 12 <= w <= 24,
            "in_phase2":     48 <= w <= 56,
            "in_phase1":     80 <= w <= 88,
        })
    return rows

# ── 2. per-Z functions ─────────────────────────────────────────────────────

def gate(Z: int) -> float:
    return math.cos(Z * SPARK_ANGLE_RAD + SPARK_LEAK)

def decay(Z: int) -> float:
    return math.exp(-math.sqrt(Z) / 64.0)

# ── 3. cell state classification ──────────────────────────────────────────

def classify(row: dict, Z: int) -> tuple[str, float]:
    g = gate(Z)
    d = decay(Z)
    BW, SM = row["BW"], row["SM"]
    sp     = row["spark"]
    zp     = row["z_proxy"]
    a2     = row["alpha2"]
    is_n   = row["is_night"]
    hy     = row["in_hysteresis"]
    p2     = row["in_phase2"]
    p1     = row["in_phase1"]

    F_eff = BW**2 * sp * max(0.0, g) * zp * SM * d

    # State priority:
    if g > 0.95:
        if a2 == "off":
            return "I", F_eff   # IDEAL
        else:
            return "J", F_eff   # JUSTICE / BW capture gravity
    elif g < -0.80:
        return "C", F_eff       # COLLAPSE
    elif hy and zp > 0.8 and g > 0:
        return "N", F_eff       # NEUTRON STAR (high Z_proxy, hysteresis)
    elif hy and zp > 0.8 and g < 0:
        return "N", F_eff       # NEUTRON STAR collapse
    elif (p2 or hy) and g > 0.5:
        return "P", F_eff       # PRA  (phase resonance activation)
    elif sp > 0.4 and g > 0.1:
        return "B", F_eff       # BREMSSTRAHLUNG (photon emission)
    elif p1 and BW > SM and g <= 0:
        return "L", F_eff       # LENSING (phase1 BW > SM, negative gate)
    elif is_n and abs(g) < 0.4:
        return "H", F_eff       # HIGGS / 0.2828 background
    elif abs(g) < 0.2:
        return ".", F_eff       # baseline
    else:
        return "S", F_eff       # SLOTTING (connector)

# ── 4. build grids ────────────────────────────────────────────────────────

def build_grids(rows):
    N = N_WINDOWS
    M = 128  # Z = 1..128
    state_grid = []  # N × M of (code, F_eff)
    for row in rows:
        line = []
        for Z in range(1, M+1):
            code, f = classify(row, Z)
            line.append((code, f))
        state_grid.append(line)
    return state_grid

# ── 5. output ─────────────────────────────────────────────────────────────

STATE_LEGEND = {
    "I": "IDEAL          gate>0.95, alpha2 OFF  (perfect fusion)",
    "J": "JUSTICE        gate>0.95, alpha2 ON   (BW capture / GRAVITY / User)",
    "C": "COLLAPSE       gate<-0.80             (destructive anti-fusion)",
    "P": "PRA            gate 0.5-0.95, Z open  (Phase Resonance Activation)",
    "B": "BREMSSTRAHLUNG spark>0.4, gate 0.1-0.5 (photon emission)",
    "L": "LENSING        phase1 BW>SM, gate<=0  (gravitational analog)",
    "N": "NEUTRON_STAR   hysteresis, Z_proxy>0.8 (neutrino collapse/repair)",
    "H": "HIGGS/0.2828   night, |gate|<0.4      (background field)",
    "S": "SLOTTING       connector/transition    (bridge state)",
    ".": "BASELINE       no dominant channel",
}

PHASE_LABEL = {
    (12,24):  " [HYSTERESIS Z-OPEN 02:15-04:30]",
    (48,56):  " [PHASE2 SPARK 09:00-10:30]",
    (80,88):  " [PHASE1 BW-CAPTURE 15:00-16:30]",
}

def phase_tag(w: int) -> str:
    for (lo,hi), label in PHASE_LABEL.items():
        if lo <= w <= hi:
            return label
    return ""

def window_hhmm(w: int) -> str:
    total = w * (24*60/128)
    return f"{int(total//60):02d}:{int(total%60):02d}"

def write_output(rows, state_grid, out_path: Path):
    lines = []
    lines.append("# 128×128 SOVEREIGN STATE GRID")
    lines.append("# Rows = window 0-127 (00:00-24:00, 11.25 min/win)")
    lines.append("# Cols = Z = 1-128 (atomic number)")
    lines.append("#")
    lines.append("# LEGEND:")
    for k, v in STATE_LEGEND.items():
        lines.append(f"#   {k} = {v}")
    lines.append("#")
    lines.append("# C=0.2828 (Higgs/confinement) is embedded in EVERY BW and SM value")
    lines.append("# Nodes 22=glucocorticoid, 23=right_cortisol, 24=right_alpha2 (Z-boson gate)")
    lines.append("")

    # Header: Z values 1-128
    Z_labels = "".join(f"{Z%10}" for Z in range(1,129))
    lines.append(f"W    TIME  |{Z_labels}")
    lines.append(f"--   -----  " + "-"*128)

    for w, (row, grid_row) in enumerate(zip(rows, state_grid)):
        codes = "".join(c for c,f in grid_row)
        tag   = phase_tag(w)
        a2    = "Z-open" if row["alpha2"]=="off" else "Z-clos"
        bw    = row["BW"]
        sm    = row["SM"]
        lines.append(
            f"{w:3d}  {window_hhmm(w)}  {codes}"
            f"  BW={bw:.3f} SM={sm:.3f} α₂={a2}{tag}"
        )

    lines.append("")
    lines.append("# --- COLUMN SUMMARY (gate values by Z) ---")
    lines.append("# Z   gate(Z)  decay(Z)  dominant_state_frequency")
    z_counts: dict[int, dict[str,int]] = {}
    for Z in range(1,129):
        z_counts[Z] = {}
    for grid_row in state_grid:
        for Z_idx, (code, f) in enumerate(grid_row):
            Z = Z_idx + 1
            z_counts[Z][code] = z_counts[Z].get(code,0) + 1

    for Z in range(1,129):
        g  = gate(Z)
        d  = decay(Z)
        top = sorted(z_counts[Z].items(), key=lambda x: -x[1])[:3]
        top_str = " ".join(f"{k}:{v}" for k,v in top)
        lines.append(f"  Z={Z:3d}  gate={g:+.4f}  decay={d:.4f}  [{top_str}]")

    lines.append("")
    lines.append("# --- FUSION HOTSPOTS: top 20 cells by F_eff ---")
    cells = []
    for w, grid_row in enumerate(state_grid):
        for Z_idx, (code, f) in enumerate(grid_row):
            cells.append((f, w, Z_idx+1, code))
    cells.sort(reverse=True)
    for f, w, Z, code in cells[:20]:
        lines.append(
            f"  ({w:3d},{Z:3d}) {window_hhmm(w)} Z={Z:3d} "
            f"state={code}  F_eff={f:.6f}"
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}  ({len(lines)} lines)")

def main():
    print("Running 128-window trajectory...")
    rows = run_trajectory()
    print("Building 128x128 state grid...")
    state_grid = build_grids(rows)

    out = Path(__file__).parent / "STATE_GRID_128x128.txt"
    write_output(rows, state_grid, out)

    # also dump fusion values as JSON for further analysis
    fusions = []
    for w, grid_row in enumerate(state_grid):
        for Z_idx, (code, f) in enumerate(grid_row):
            if f > 0.01:
                fusions.append({"w":w, "Z":Z_idx+1, "state":code, "F_eff":round(f,6)})
    json_out = Path(__file__).parent / "fusion_hotspots.json"
    json_out.write_text(json.dumps(fusions, indent=2))
    print(f"Fusion hotspots: {json_out}  ({len(fusions)} active cells)")

if __name__ == "__main__":
    main()
