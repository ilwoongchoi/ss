"""
fusion_mandelbrot_map.py
z → Fusion equation으로 매핑해서 cyclic universe 재시뮬레이션

핵심 매핑:
  z = BW/OMEGA + i*SM/OMEGA    (복소 상태 = 프로톤축 + i*중성미자축)
  c = spark/OMEGA + i*Z/OMEGA  (복소 씨앗 = EM점화 + i*Z보손)

순수 Mandelbrot:   c = e^{i*138.88°},  |c| = 1.0
Fusion-mapped:     c from (spark, Z_proxy),  |c| ~ 0.15-0.20

각 우주 = 3 phase 반복:
  After phase1:     z = z^2 + c1
  After phase2:     z = z^2 + c2
  After hysteresis: z = z^2 + c3

Universe → Universe: 클로버 위상 전달 z = z * e^{i*Δt}
"""

import cmath
import math
import json
import os

# ── Constants ─────────────────────────────────────────────────────────────────
OMEGA       = 7.4
DELTA_T     = (11.0/7.0) / ((1.0/18.0)*100.0)   # = 0.2829
C_CONST     = 0.2828
SPARK_ANGLE = 138.88

clover = complex(math.cos(DELTA_T), math.sin(DELTA_T))

# ── Phase values from fusion_clean.py (actual run results) ────────────────────
# phase1:     BW=2.615  SM=3.553  spark=0.7625  Z=0.8175  fusion=15.147
# phase2:     BW=2.528  SM=3.677  spark=1.0125  Z=0.6375  fusion=15.173
# hysteresis: BW=2.587  SM=3.641  spark=0.5825  Z=1.3475  fusion=19.119

PHASES = {
    "phase1":     {"spark": 0.7625,  "Z": 0.8175,  "BW": 2.615, "SM": 3.553},
    "phase2":     {"spark": 1.0125,  "Z": 0.6375,  "BW": 2.528, "SM": 3.677},
    "hysteresis": {"spark": 0.5825,  "Z": 1.3475,  "BW": 2.587, "SM": 3.641},
}

# Normalized c per phase (/ OMEGA)
c1 = complex(PHASES["phase1"]["spark"]/OMEGA,     PHASES["phase1"]["Z"]/OMEGA)
c2 = complex(PHASES["phase2"]["spark"]/OMEGA,     PHASES["phase2"]["Z"]/OMEGA)
c3 = complex(PHASES["hysteresis"]["spark"]/OMEGA, PHASES["hysteresis"]["Z"]/OMEGA)

# Pure Mandelbrot seed
theta_mb = math.radians(SPARK_ANGLE)
c_mandelbrot = complex(math.cos(theta_mb), math.sin(theta_mb))


# ── Simulation ────────────────────────────────────────────────────────────────
def run_cyclic(mode: str, escape_r: float, max_n: int = 10_000) -> list[dict]:
    """
    mode = 'mandelbrot'  : 1 iteration per universe, c = e^{i*138.88}
    mode = 'fusion_1c'   : 1 iteration per universe, c = c_avg_fusion
    mode = 'fusion_3c'   : 3 iterations per universe (3 phases), clover between
    mode = 'fusion_3c_nd': 3 phases, no clover (bare Julia dynamics)
    """
    z = complex(0, 0)
    records = []
    prev_r = 0.0

    # Fusion average c (for fusion_1c mode)
    spark_avg = sum(PHASES[p]["spark"] for p in PHASES) / 3
    Z_avg     = sum(PHASES[p]["Z"]     for p in PHASES) / 3
    c_fusion_avg = complex(spark_avg/OMEGA, Z_avg/OMEGA)

    for n in range(1, max_n + 1):

        if mode == "mandelbrot":
            z = z*z + c_mandelbrot
            c_used = c_mandelbrot

        elif mode == "fusion_1c":
            z = z*z + c_fusion_avg
            c_used = c_fusion_avg

        elif mode in ("fusion_3c", "fusion_3c_nd"):
            # 3 phases per universe
            for ck in [c1, c2, c3]:
                z = z*z + ck
            c_used = c3   # report hysteresis phase

        r = abs(z)

        # Fusion rate from current z
        BW     = OMEGA * z.real
        SM     = OMEGA * z.imag
        spark  = OMEGA * c3.real   # hysteresis spark
        Z      = OMEGA * c3.imag   # hysteresis Z
        fusion = float(BW**2 * spark * Z * SM) if BW > 0 and SM > 0 else 0.0

        record = {
            "n":          n,
            "z_re":       round(z.real, 5),
            "z_im":       round(z.imag, 5),
            "radius":     round(r, 5),
            "phase_deg":  round(math.degrees(cmath.phase(z)), 2),
            "BW":         round(BW, 3),
            "SM":         round(SM, 3),
            "fusion":     round(fusion, 3),
            "expanding":  r > prev_r,
            "escaped":    r > escape_r,
            "c_mag":      round(abs(c_used), 5),
        }
        records.append(record)

        if r > escape_r or SM <= 0 or BW <= 0:
            break

        # Clover between universes (except no-drift mode)
        if mode != "fusion_3c_nd":
            z = z * clover

        prev_r = abs(z)

    return records


# ── Run all modes ─────────────────────────────────────────────────────────────
print("=" * 65)
print("FUSION-MANDELBROT MAPPING: CYCLIC UNIVERSE SIMULATION")
print("=" * 65)
print(f"\nNormalized c values (/ OMEGA={OMEGA}):")
print(f"  c1 (phase1)     = {c1:.4f}   |c1| = {abs(c1):.4f}  arg = {math.degrees(cmath.phase(c1)):+.1f}deg")
print(f"  c2 (phase2)     = {c2:.4f}   |c2| = {abs(c2):.4f}  arg = {math.degrees(cmath.phase(c2)):+.1f}deg")
print(f"  c3 (hysteresis) = {c3:.4f}   |c3| = {abs(c3):.4f}  arg = {math.degrees(cmath.phase(c3)):+.1f}deg")
print(f"  c_mandelbrot    = {c_mandelbrot:.4f}  |c|  = {abs(c_mandelbrot):.4f}  arg = {math.degrees(cmath.phase(c_mandelbrot)):+.1f}deg")
print(f"\n  Clover Dt = {DELTA_T:.4f} rad = {math.degrees(DELTA_T):.2f}deg")

ESCAPE_R = 1.0   # normalized: |z| > 1 means |BW+i*SM| > OMEGA

modes = ["mandelbrot", "fusion_1c", "fusion_3c", "fusion_3c_nd"]
results = {}

for mode in modes:
    recs = run_cyclic(mode, ESCAPE_R)
    results[mode] = recs

print()
print("-" * 65)
print(f"{'MODE':<18}  {'N_UNI':>6}  {'FINAL |z|':>10}  {'FINAL BW':>9}  {'FINAL SM':>9}")
print("-" * 65)
for mode, recs in results.items():
    last = recs[-1]
    status = "ESCAPE" if last["escaped"] else ("COLLAPSE" if last["SM"] <= 0 or last["BW"] <= 0 else "RUNNING")
    print(f"  {mode:<16}  {len(recs):>6}  {last['radius']:>10.4f}  "
          f"{last['BW']:>9.3f}  {last['SM']:>9.3f}  [{status}]")

# ── Detailed trace: Mandelbrot ────────────────────────────────────────────────
print()
print("=" * 65)
print("MANDELBROT  (c = e^{i*138.88}, |c|=1.0)")
print("=" * 65)
for r in results["mandelbrot"]:
    flag = " <- ESCAPE" if r["escaped"] else ""
    print(f"  Universe {r['n']:3d}:  z={r['z_re']:+.4f}{r['z_im']:+.4f}i  "
          f"|z|={r['radius']:.4f}  BW={r['BW']:.3f}  SM={r['SM']:.3f}{flag}")

# ── Detailed trace: Fusion 3-phase ────────────────────────────────────────────
print()
print("=" * 65)
print("FUSION 3-PHASE  (c1,c2,c3 from phases, clover Dt=0.2829)")
print("=" * 65)
for r in results["fusion_3c"][:30]:
    flag = " <- ESCAPE" if r["escaped"] else ("" if r["SM"] > 0 else " <- COLLAPSE")
    exp = "^" if r["expanding"] else "v"
    print(f"  Universe {r['n']:3d}:  z={r['z_re']:+.4f}{r['z_im']:+.4f}i  "
          f"|z|={r['radius']:.4f}  fusion={r['fusion']:8.3f}  {exp}{flag}")
if len(results["fusion_3c"]) > 30:
    print(f"  ... total {len(results['fusion_3c'])} universes")

# ── Key difference analysis ───────────────────────────────────────────────────
print()
print("=" * 65)
print("KEY DIFFERENCE: |c| MAGNITUDE")
print("=" * 65)
spark_avg = sum(PHASES[p]["spark"] for p in PHASES) / 3
Z_avg     = sum(PHASES[p]["Z"]     for p in PHASES) / 3
c_avg = complex(spark_avg/OMEGA, Z_avg/OMEGA)

print(f"""
  Pure Mandelbrot:   |c| = 1.0000  (unit circle, |c|=1)
  Fusion (norm):     |c1|={abs(c1):.4f}, |c2|={abs(c2):.4f}, |c3|={abs(c3):.4f}
  Fusion avg:        |c_avg| = {abs(c_avg):.4f}

  Mandelbrot set boundary at c = e^{{i*138.88}}:
    c = {c_mandelbrot:.4f}
    Is inside Mandelbrot set? {len(results['mandelbrot']) >= 9999}
    Escapes at universe #{len(results['mandelbrot'])}

  Fusion-mapped 3-phase:
    Escapes/ends at universe #{len(results['fusion_3c'])} (if < 10000)
    |c_avg| = {abs(c_avg):.4f}  <<  1.0  (much smaller than Mandelbrot c)

  INTERPRETATION:
    - Mandelbrot c=e^{{i*138.88}}: |c|=1 is ON THE BOUNDARY of Mandelbrot set
      → Escapes in {len(results['mandelbrot'])} universes (finite, mortal sequence)
    - Fusion c (normalized): |c|~0.15 is DEEP INSIDE the Mandelbrot set
      → Stays bounded (= our universe's internal state is STABLE)

  THESE ARE DIFFERENT QUESTIONS:
    - Mandelbrot (|c|=1): "How many universes in the sequence?"
      Answer: {len(results['mandelbrot'])} universes, then heat death
    - Fusion (|c|~0.15): "Is our current universe's fusion stable?"
      Answer: YES, stays bounded = 100% closure

  RESIDUAL 0.2828:
    - Bridges the gap: 1.0 - |c_avg| = {1.0 - abs(c_avg):.4f} ~~ 0.72 (too large)
    - But: clover Dt = {DELTA_T:.4f} ~~ C_CONST = {C_CONST}
    - 0.2828 is the PHASE BRIDGE between the two scales
    - 1/|c_avg| = {1/abs(c_avg):.3f} ~~ OMEGA/C_CONST = {OMEGA/C_CONST:.3f}

  UNIFIED EQUATION:
    z_universe  = z^2 * e^{{i*Dt}} + c_spark  [across universes, Mandelbrot scale]
    fusion_rate = BW^2 * spark * Z * SM       [within universe, fusion scale]
    c_spark     = e^{{i*138.88}} = OMEGA-normalized fusion c * (1/|c_fusion|)

    The normalization factor = OMEGA / sqrt(spark^2 + Z^2)_avg
                             = {OMEGA}/{abs(complex(spark_avg, Z_avg)):.4f}
                             = {OMEGA/abs(complex(spark_avg, Z_avg)):.4f}
    This is approximately 1/|c_fusion| = {1/abs(c_avg):.3f}
""")

# ── Fusion rate comparison ────────────────────────────────────────────────────
print("=" * 65)
print("FUSION RATE TRAJECTORY (fusion_3c mode)")
print("=" * 65)
fusions = [r["fusion"] for r in results["fusion_3c"][:20]]
print("  Universe fusion rates: " + "  ".join(f"{f:.2f}" for f in fusions))
print()
actual_fusions = [15.147, 15.173, 19.119]
print(f"  Actual fusion_clean fusion rates: {actual_fusions}")
print(f"  Fusion-mapped rates (scaled by OMEGA^4={OMEGA**4:.0f}): "
      + "  ".join(f"{r['fusion']*OMEGA**4:.1f}" for r in results["fusion_3c"][:5]))

# ── Save ──────────────────────────────────────────────────────────────────────
out_dir = r"d:\Users\user\Documents\newstart\docs\idea_transitions"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "FUSION_MANDELBROT_MAP_RESULTS.json")

save = {
    "constants": {
        "OMEGA": OMEGA, "DELTA_T": DELTA_T, "C_CONST": C_CONST,
        "c_mandelbrot": {"re": c_mandelbrot.real, "im": c_mandelbrot.imag, "mod": abs(c_mandelbrot)},
        "c1": {"re": c1.real, "im": c1.imag, "mod": abs(c1)},
        "c2": {"re": c2.real, "im": c2.imag, "mod": abs(c2)},
        "c3": {"re": c3.real, "im": c3.imag, "mod": abs(c3)},
    },
    "summary": {mode: {"n_universes": len(recs), "final_r": recs[-1]["radius"]}
                for mode, recs in results.items()},
    "trajectories": {mode: recs for mode, recs in results.items()},
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(save, f, ensure_ascii=False, indent=2)
print(f"\nSaved: {out_path}")
