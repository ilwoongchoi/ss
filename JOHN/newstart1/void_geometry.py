"""
void_geometry.py
================
Multi-universe chain simulation.

Each universe is parametrized by h_k = k * C (k = 1, 2, 3, ...).
For each universe:
  - Start: primordial_z(h_k)
  - Evolve: 5-phase K8 Laplacian cycle
  - End:    z*(h_k) = homeostasis fixed point (or collapse point)

VOID = the complex-space gap from one universe's endpoint to
       the NEXT universe's primordial starting point.

VOID_k = z*(h_k) - primordial_z(h_{k-1})

The geometry of these voids (angles, distances) encodes
how 138.88 deg emerges from C = 0.2828.
"""
from __future__ import annotations
import numpy as np
from universe_sim import primordial_z, run_universe, laplacian_h, PHASES, DT
from fusion_core import IDX, SUBJECTS, C as C_TRUE, OMEGA as OMEGA_TRUE


def evolve_full(h: float, n_cycles: int = 600) -> dict:
    """Full trajectory from primordial to homeostasis. Returns endpoint z*."""
    Ls = [laplacian_h(h, p) for p in PHASES]
    Props = [np.eye(8) - DT * L for L in Ls]
    z = primordial_z(h)
    traj = [z.copy()]
    prev_bw = None

    for cycle in range(n_cycles):
        for P in Props:
            z = P @ z
        if not np.all(np.isfinite(z)):
            return {"h": h, "converged": False, "collapsed": True,
                    "z_end": z, "cycles": cycle+1, "traj": traj}
        raw_bw = abs(z[IDX["w_boson"]])
        raw_sm = abs(z[IDX["z_boson"]])
        bw = raw_bw / (raw_bw + raw_sm + 1e-15) * OMEGA_TRUE
        traj.append(z.copy())
        if prev_bw is not None and abs(bw - prev_bw) < 1e-8:
            return {"h": h, "converged": True, "collapsed": False,
                    "z_end": z.copy(), "cycles": cycle+1, "traj": traj}
        prev_bw = bw

    return {"h": h, "converged": False, "collapsed": False,
            "z_end": z.copy(), "cycles": n_cycles, "traj": traj}


def void_vector(z_end: np.ndarray, h_next: float) -> np.ndarray:
    """VOID = z*(h_k) - primordial_z(h_{k-1})"""
    return z_end - primordial_z(h_next)


def void_angle(v: np.ndarray, particle_a: str = "photon",
               particle_b: str = "w_boson") -> float:
    """Angle of the void vector in the (particle_a / particle_b) plane."""
    a = v[IDX[particle_a]]
    b = v[IDX[particle_b]]
    return float(np.angle(a / (b + 1e-15)) * 180 / np.pi) % 360


def void_arc_angle(z_start: np.ndarray, z_end: np.ndarray,
                   particle: str = "w_boson") -> float:
    """Total arc traversed by one particle component from start to end."""
    a = z_start[IDX[particle]]
    b = z_end[IDX[particle]]
    return float(np.angle(b / (a + 1e-15)) * 180 / np.pi) % 360


# ── Main analysis ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("MULTI-UNIVERSE CHAIN  h_k = k * C")
    print("=" * 65)

    # Build universe chain: h_k = k * C, k = 1, 2, 3, ...
    universes = []
    k = 1
    while True:
        h = k * C_TRUE
        res = evolve_full(h, n_cycles=800)
        sym = None
        if np.all(np.isfinite(res["z_end"])):
            raw_bw = abs(res["z_end"][IDX["w_boson"]])
            raw_sm = abs(res["z_end"][IDX["z_boson"]])
            r = raw_bw / (raw_bw + raw_sm + 1e-15)
            sym = abs(r - 0.5) * OMEGA_TRUE
        universes.append({
            "k": k, "h": h,
            "converged": res["converged"],
            "collapsed": res["collapsed"],
            "z_end": res["z_end"],
            "z_start": primordial_z(h),
            "cycles": res["cycles"],
            "symmetry_broken": (sym > 0.1) if sym is not None else True,
        })
        print(f"  k={k}  h={h:.6f}  "
              f"{'converged' if res['converged'] else 'NOT converged'}"
              f"{'  [COLLAPSED]' if res['collapsed'] else ''}"
              f"  sym_broken={universes[-1]['symmetry_broken']}"
              f"  cycles={res['cycles']}")
        # Stop when permanently broken or h > 1.2
        if h > 1.2 or (k > 2 and universes[-1]["symmetry_broken"]):
            break
        k += 1

    print()
    print("=" * 65)
    print("VOID GEOMETRY (z*(h_k) -> primordial(h_{k-1}))")
    print("=" * 65)
    print(f"  {'k->k-1':8s}  {'void |w|':10s}  {'void |z|':10s}  "
          f"{'angle ph/w':12s}  {'angle ph/z':12s}")

    for i in range(1, len(universes)):
        u_k   = universes[i]      # higher h (earlier universe)
        u_k1  = universes[i - 1]  # lower h  (later universe, this or closer)
        v = void_vector(u_k["z_end"], u_k1["h"])
        a_pw = void_angle(v, "photon",  "w_boson")
        a_pz = void_angle(v, "photon",  "z_boson")
        a_wz = void_angle(v, "w_boson", "z_boson")
        vw = abs(v[IDX["w_boson"]])
        vz = abs(v[IDX["z_boson"]])
        print(f"  k={u_k['k']}->{u_k1['k']}        "
              f"{vw:10.6f}  {vz:10.6f}  "
              f"{a_pw:12.4f}  {a_pz:12.4f}  "
              f"  wz={a_wz:.4f}")

    print()
    print("=" * 65)
    print("HOMEOSTASIS ENDPOINT ANGLES (z*[particle])")
    print("=" * 65)
    for u in universes:
        z = u["z_end"]
        if not np.all(np.isfinite(z)):
            print(f"  k={u['k']}  h={u['h']:.4f}  COLLAPSED")
            continue
        w_ang = float(np.angle(z[IDX["w_boson"]]) * 180 / np.pi) % 360
        z_ang = float(np.angle(z[IDX["z_boson"]]) * 180 / np.pi) % 360
        p_ang = float(np.angle(z[IDX["photon"]])  * 180 / np.pi) % 360
        w_abs = abs(z[IDX["w_boson"]])
        z_abs = abs(z[IDX["z_boson"]])
        print(f"  k={u['k']}  h={u['h']:.4f}  "
              f"|w|={w_abs:.6f}  arg(w)={w_ang:.4f} deg  "
              f"|z|={z_abs:.6f}  arg(z)={z_ang:.4f} deg  "
              f"arg(ph)={p_ang:.4f} deg")

    print()
    print("=" * 65)
    print("VOID ARC: cumulative angle from h=kC end to h=C primordial")
    print("=" * 65)
    # Key question: what is the total complex rotation
    # from z*(2C) [previous universe endpoint]
    # to primordial_z(C) [this universe start]?
    # Does this give 138.88?

    if len(universes) >= 2:
        u2 = universes[1]  # h = 2C
        u1 = universes[0]  # h = C

        z_end_prev = u2["z_end"]      # homeostasis of previous universe
        z_start_this = u1["z_start"]  # primordial of this universe

        print(f"\n  Previous universe endpoint z*(h=2C):")
        for name in SUBJECTS:
            amp = z_end_prev[IDX[name]]
            print(f"    {name:12s}  |z|={abs(amp):.6f}  "
                  f"arg={np.angle(amp)*180/np.pi % 360:.4f} deg")

        print(f"\n  This universe primordial z(h=C):")
        for name in SUBJECTS:
            amp = z_start_this[IDX[name]]
            print(f"    {name:12s}  |z|={abs(amp):.6f}  "
                  f"arg={np.angle(amp)*180/np.pi % 360:.4f} deg")

        void = z_end_prev - z_start_this
        print(f"\n  VOID vector (z*(2C) - primordial(C)):")
        for name in SUBJECTS:
            v = void[IDX[name]]
            print(f"    {name:12s}  |void|={abs(v):.6f}  "
                  f"arg={np.angle(v)*180/np.pi % 360:.4f} deg")

        # The critical angle: VOID in the w_boson/z_boson plane
        v_w = void[IDX["w_boson"]]
        v_z = void[IDX["z_boson"]]
        v_p = void[IDX["photon"]]
        v_q = void[IDX["quark"]]
        v_g = void[IDX["gluon"]]

        ang_wz = float(np.angle(v_w / (v_z + 1e-15)) * 180 / np.pi) % 360
        ang_pw = float(np.angle(v_p / (v_w + 1e-15)) * 180 / np.pi) % 360
        ang_qg = float(np.angle(v_q / (v_g + 1e-15)) * 180 / np.pi) % 360

        print(f"\n  KEY VOID ANGLES:")
        print(f"    arg(void_w / void_z) = {ang_wz:.6f} deg  (target: 138.88?)")
        print(f"    arg(void_ph / void_w) = {ang_pw:.6f} deg  (target: 138.88?)")
        print(f"    arg(void_q / void_g) = {ang_qg:.6f} deg  (target: 138.88?)")
        print()

        # Also: ratio of amplitudes in the void
        ratio_wz = abs(v_w) / (abs(v_z) + 1e-15)
        ratio_pw = abs(v_p) / (abs(v_w) + 1e-15)
        print(f"  VOID AMPLITUDE RATIOS:")
        print(f"    |void_w| / |void_z| = {ratio_wz:.6f}")
        print(f"    |void_ph| / |void_w| = {ratio_pw:.6f}")
        print(f"    arctan(ratio_wz) * (180/pi) = "
              f"{np.arctan(ratio_wz)*180/np.pi:.6f} deg")
        print(f"    360 * C^2 = {360 * C_TRUE**2:.6f} deg")
        print(f"    360 * C   = {360 * C_TRUE:.6f} deg")

    print()
    print("=" * 65)
    print("GEOMETRIC DERIVATION: 138.88 from C = 0.2828")
    print("=" * 65)
    # Analytical: what angle relationships does C = sqrt(2)/5 imply?
    C = C_TRUE
    print(f"  C = sqrt(2)/5 = {C:.8f}")
    print(f"  C^2 = {C**2:.8f}")
    print(f"  1/C = {1/C:.8f}")
    print(f"  arctan(C) = {np.arctan(C)*180/np.pi:.6f} deg")
    print(f"  arctan(1/C) = {np.arctan(1/C)*180/np.pi:.6f} deg")
    print(f"  arccos(C) = {np.arccos(C)*180/np.pi:.6f} deg")
    print(f"  arccos(-C) = {np.arccos(-C)*180/np.pi:.6f} deg")
    print(f"  arccos(C^2) = {np.arccos(C**2)*180/np.pi:.6f} deg")
    print(f"  arccos(-C^2) = {np.arccos(-C**2)*180/np.pi:.6f} deg")
    print(f"  180 * C = {180 * C:.6f} deg")
    print(f"  360 * C = {360 * C:.6f} deg")
    print(f"  360 * (1 - C) = {360 * (1 - C):.6f} deg")
    print(f"  2 * arccos(C) = {2*np.arccos(C)*180/np.pi:.6f} deg")
    print(f"  pi/2 + 2*arctan(C) = {90 + 2*np.arctan(C)*180/np.pi:.6f} deg")
    print(f"  arcsin(5*C^2) = {np.arcsin(5*C**2)*180/np.pi:.6f} deg  (5C^2=0.4)")
    print(f"  arccos(5*C^2 - 1) = N/A (5C^2-1={5*C**2-1:.4f})")

    # Try: 360 * C / (2 * pi * C) = 360/(2*pi)? No.
    # Try: angle = sum of K8 node phases at homeostasis?
    # Try: 138.88 = 180 - arctan(1/C) ?
    val1 = 180 - np.arctan(1/C)*180/np.pi
    print(f"  180 - arctan(1/C) = {val1:.6f} deg")

    # Try: 138.88 = arccos(-C * sqrt(1+C^2) / (1 + C^2)) ?
    val2 = np.arctan(C / (1 + C**2)) * 180/np.pi
    print(f"  arctan(C/(1+C^2)) = {val2:.6f} deg")

    # Try: C = 0.2828, and 0.2828 * 360 = 101.8, but NEUTRON_TIME_SYNC * 360 = 138.85
    # NEUTRON_TIME_SYNC = 0.3857
    NEUTRON = 0.3857
    print(f"\n  NEUTRON_TIME_SYNC = {NEUTRON}")
    print(f"  NEUTRON * 360 = {NEUTRON*360:.4f} deg  (= 138.85 ~ 138.88)")
    print(f"  NEUTRON / C = {NEUTRON/C:.6f}")
    print(f"  C * NEUTRON = {C*NEUTRON:.6f}")
    print(f"  NEUTRON = C * ? => factor = {NEUTRON/C:.6f}")
    print(f"  ~ 3*sqrt(2)/4 = {3*np.sqrt(2)/4:.6f}")
    print(f"  ~ sqrt(3)/2*C * ? ")
    print(f"  ~ (1 + C^2) * C = {(1+C**2)*C:.6f}")
    print(f"  ~ C * (1 + C + C^2) = {C*(1+C+C**2):.6f}")
    print(f"  ~ C * 4/3 = {C*4/3:.6f}")
    print(f"  ~ C * pi/2 = {C*np.pi/2:.6f}")
    print(f"  ~ C * (pi/2 + C) = {C*(np.pi/2 + C):.6f}")
    print(f"  arctan(1 + C) * (180/pi) = {np.arctan(1+C)*180/np.pi:.6f} deg")
    print(f"  arctan(1 + C) * (360/pi) = {np.arctan(1+C)*360/np.pi:.6f} deg")
    print()
    # NEUTRON_TIME_SYNC = 0.3857 ≈ 3*sqrt(2)/11
    val3 = 3*np.sqrt(2)/11
    print(f"  3*sqrt(2)/11 = {val3:.8f}  (NEUTRON_TIME_SYNC = {NEUTRON})")
    print(f"  3*sqrt(2)/11 * 360 = {val3*360:.6f} deg")
    print(f"  3*C*5/11 = {3*C*5/11:.8f}  (= 15C/11)")
    print(f"  15C/11 * 360 = {15*C/11*360:.6f} deg  (target: 138.88)")
    print(f"  => 138.88 = 15C/11 * 360 = (15 * sqrt(2)/5 / 11) * 360")
    print(f"             = (3*sqrt(2)/11) * 360")
    print(f"             = 3 * C * (5/11) * 360")
