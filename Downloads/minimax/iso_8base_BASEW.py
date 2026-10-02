"""
iso_8base_BASEW.py — 8 buffer cascade with REAL BASE_W constants.

Uses constants from universe_math_structures.py:
  HG = C = sqrt(0.08) = 0.2828
  GM = 1.0
  MP = 2/16 = 0.125
  PT = 3/16 = 0.1875
  TW = C = 0.2828
  WZ = 4/16 = 0.25
  Znu = 1/28 = 0.0357 (LUNAR_CYCLE)
"""
import json, math
from pathlib import Path

C2 = 0.08
C = math.sqrt(C2)  # 0.2828
LUNAR = 1.0/28.0   # 0.0357

K = {
    "HG": C,           # 0.2828
    "GM": 1.0,
    "MP": 2.0/16.0,    # 0.125
    "PT": 3.0/16.0,    # 0.1875
    "TW": C,           # 0.2828
    "WZ": 4.0/16.0,    # 0.25
    "Znu": LUNAR,      # 0.0357
}

def cascade(t, x):
    H, G, M, P, T_, W, Z, N = x
    return [
        -K["HG"] * H,
        K["HG"] * H - K["GM"] * G,
        K["GM"] * G - K["MP"] * M,
        K["MP"] * M - K["PT"] * P,
        K["PT"] * P - K["TW"] * T_,
        K["TW"] * T_ - K["WZ"] * W,
        K["WZ"] * W - K["Znu"] * Z,
        K["Znu"] * Z,
    ]

def rk4(f, t, x, h):
    k1 = f(t, x)
    k2 = f(t+h/2, [x[i]+h*k1[i]/2 for i in range(8)])
    k3 = f(t+h/2, [x[i]+h*k2[i]/2 for i in range(8)])
    k4 = f(t+h, [x[i]+h*k3[i] for i in range(8)])
    return [x[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(8)], t+h

def integrate(f, x0, t_end, dt):
    ts, xs = [0.0], [x0[:]]
    t, x = 0.0, x0[:]
    for _ in range(int(t_end/dt)):
        x, t = rk4(f, t, x, dt)
        ts.append(t); xs.append(x[:])
    return ts, xs

def main():
    print("=" * 70)
    print("CASCADE with REAL BASE_W constants")
    print("=" * 70)
    print(f"  HG = C = sqrt(0.08) = {K['HG']:.4f}")
    print(f"  GM = 1.0")
    print(f"  MP = 2/16 = {K['MP']:.4f}")
    print(f"  PT = 3/16 = {K['PT']:.4f}")
    print(f"  TW = C = {K['TW']:.4f}")
    print(f"  WZ = 4/16 = {K['WZ']:.4f}")
    print(f"  Znu = 1/28 = LUNAR_CYCLE = {K['Znu']:.4f}")
    print()

    x0 = [1.0, 0, 0, 0, 0, 0, 0, 0]
    ts, xs = integrate(cascade, x0, t_end=100.0, dt=0.05)

    print(f"  {'t':6s}  {'H':7s}  {'G':7s}  {'M':7s}  {'P':7s}  {'T':7s}  {'W':7s}  {'Z':7s}  {'Nu':7s}  {'SUM':7s}")
    for i in [0, 5, 10, 20, 30, 50, 80, 100, 200, 500, 1000, 1999]:
        if i < len(ts):
            x = xs[i]
            s = sum(x)
            print(f"  {ts[i]:5.1f}  {x[0]:6.4f}  {x[1]:6.4f}  {x[2]:6.4f}  {x[3]:6.4f}  {x[4]:6.4f}  {x[5]:6.4f}  {x[6]:6.4f}  {x[7]:6.4f}  {s:6.4f}")

    final = xs[-1]
    print(f"\n  Mass conservation: final SUM = {sum(final):.4f} (initial 1.0)")
    print(f"  Final ghost sink (νμ) fraction: {final[-1]:.4f}")
    print(f"  Final Z retained: {final[6]:.4f}")

    out = {
        "_version": "8base_BASEW_v1",
        "_date": "2026-09-09",
        "_source": "universe_math_structures.py:7057-7076 BASE_W + LUNAR_CYCLE",
        "k_values": K,
        "mass_conservation": round(sum(final), 4),
        "ghost_sink_fraction": round(final[-1], 4),
    }
    out_path = Path(__file__).parent / "iso_8base_BASEW.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
