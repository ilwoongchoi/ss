#!/usr/bin/env python
"""runsh_detune_feature_sweep_jax.py

High-throughput 2D sweep for detuned Swift-Hohenberg (JAX).

Equation:
  u_t = [ r - (q0^2 - |k|^2)^2 ] u - u^3
"""

from __future__ import annotations

import argparse, csv, json, os, time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"] = "platform"

import numpy as np

def _require_jax() -> None:
    try:
        import jax  # noqa: F401
        import jax.numpy as jnp  # noqa: F401
        import matplotlib.pyplot as plt  # noqa: F401
    except Exception as e:
        raise SystemExit(f"JAX or Matplotlib import failed: {e}")

def _default_outdir() -> str:
    if os.path.isdir("/kaggle/working"):
        return "/kaggle/working/geometry_sweep_2d"
    return "out/geometry_sweep_2d"

def _parse_list_floats(s: str) -> list[float]:
    if s is None:
        return []
    s = s.strip()
    if not s:
        return []
    return [float(x.strip()) for x in s.split(",") if x.strip()]

@dataclass(frozen=True)
class Cfg:
    grid: int
    domain: float
    dt: float
    steps: int
    dtype: str
    dealias: bool
    ring_rel_width: float
    batch: int

def _jax_dtype(dtype: str):
    import jax.numpy as jnp
    d = (dtype or "").lower().strip()
    if d in {"f32", "float32", "fp32"}:
        return jnp.float32
    if d in {"f64", "float64", "fp64"}:
        return jnp.float64
    raise ValueError("dtype must be f32 or f64")

def setup_kernels(cfg: Cfg):
    import jax
    import jax.numpy as jnp

    dtype = _jax_dtype(cfg.dtype)
    N = int(cfg.grid)
    L = float(cfg.domain)
    dx = L / N

    kx = jnp.fft.fftfreq(N, d=dx) * (2.0 * jnp.pi)
    ky = jnp.fft.fftfreq(N, d=dx) * (2.0 * jnp.pi)
    KX, KY = jnp.meshgrid(kx, ky, indexing="ij")
    k2 = (KX * KX + KY * KY).astype(dtype)
    kmag = jnp.sqrt(k2).astype(dtype)
    theta = jnp.arctan2(KY, KX).astype(dtype)

    dealias_mask = None
    if cfg.dealias:
        cutoff = 1.0 / 3.0
        k_norm = jnp.fft.fftfreq(N)
        KX_n, KY_n = jnp.meshgrid(k_norm, k_norm, indexing="ij")
        mask = (jnp.abs(KX_n) <= cutoff) & (jnp.abs(KY_n) <= cutoff)
        dealias_mask = mask.astype(dtype)

    dt = jnp.asarray(cfg.dt, dtype=dtype)
    ring_rel_width = float(cfg.ring_rel_width)

    def _step(u_hat, r, q0):
        term = (q0**2 - k2)
        Lk = r - term**2
        denom = 1.0 - dt * Lk

        u = jnp.fft.ifft2(u_hat).real
        nl_hat = jnp.fft.fft2(u**3)
        if dealias_mask is not None:
            nl_hat = nl_hat * dealias_mask
        return (u_hat - dt * nl_hat) / denom

    def _init(seed: int):
        key = jax.random.PRNGKey(seed)
        return jax.random.normal(key, (N, N), dtype=dtype) * 1e-2

    def _extract(u, u_hat, q0):
        ps = jnp.abs(u_hat) ** 2
        total_e = jnp.sum(ps)

        rw = ring_rel_width
        ring_lo = (1.0 - rw) * q0
        ring_hi = (1.0 + rw) * q0
        harm_lo = (1.0 - rw) * (2.0 * q0)
        harm_hi = (1.0 + rw) * (2.0 * q0)

        ring_mask = (kmag >= ring_lo) & (kmag <= ring_hi)
        harm_mask = (kmag >= harm_lo) & (kmag <= harm_hi)

        ring_e = jnp.sum(ps * ring_mask)
        harm_e = jnp.sum(ps * harm_mask)

        ring1_frac = ring_e / (total_e + 1e-12)
        broadband_frac = (total_e - ring_e) / (total_e + 1e-12)
        harm_ratio = harm_e / (ring_e + 1e-12)

        w = jnp.where(ring_mask, ps, 0.0)
        wsum = jnp.sum(w) + 1e-12
        e2 = jnp.exp(2.0j * theta)
        e6 = jnp.exp(6.0j * theta)
        psi2 = jnp.abs(jnp.sum(w * e2) / wsum)
        psi6 = jnp.abs(jnp.sum(w * e6) / wsum)

        amp = jnp.sqrt(jnp.mean(u ** 2))

        ps_no_dc = ps.at[0, 0].set(0.0)
        flat_idx = jnp.argmax(ps_no_dc.reshape(-1))
        k_peak = kmag.reshape(-1)[flat_idx]

        return amp, ring1_frac, harm_ratio, broadband_frac, psi2, psi6, k_peak

    @jax.jit
    def integrate(u0, r, q0):
        u_hat = jnp.fft.fft2(u0)
        def body(uh, _):
            return _step(uh, r, q0), None
        u_hat, _ = jax.lax.scan(body, u_hat, None, length=int(cfg.steps))
        u = jnp.fft.ifft2(u_hat).real
        return u, u_hat

    return {
        "init": _init,
        "extract": _extract,
        "integrate": integrate,
    }

class CsvWriter:
    def __init__(self, outdir: str):
        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.csv_path = self.outdir / "feature_cloud.csv"
        self.cols = ["r","q0","seed","amp_l2","ring1_frac","harm_ratio","broadband_frac","psi2","psi6","k_peak","status","walltime_sec"]
        if not self.csv_path.exists():
            with self.csv_path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(self.cols)

    def write_row(self, *row):
        with self.csv_path.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)

def _load_seen(csv_path: Path):
    seen = set()
    if not csv_path.exists():
        return seen
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                seen.add((float(r["r"]), float(r["q0"]), int(r["seed"])))
            except:
                pass
    return seen

def main():
    _require_jax()
    import jax
    import jax.numpy as jnp

    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=str, default=_default_outdir())
    ap.add_argument("--grid", "--N", dest="grid", type=int, default=256)
    ap.add_argument("--domain", "--L", dest="domain", type=float, default=200.0)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--dealias", action="store_true")
    ap.add_argument("--ring-rel-width", type=float, default=0.08)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--r-values", type=str, default=None)
    ap.add_argument("--q0-values", type=str, default=None)
    ap.add_argument("--seed-start", type=int, default=0)
    ap.add_argument("--n-seeds", type=int, default=10)
    ap.add_argument("--resume", action="store_true")

    args, _ = ap.parse_known_args()

    cfg = Cfg(
        grid=args.grid,
        domain=args.domain,
        dt=args.dt,
        steps=args.steps,
        dtype="f32",
        dealias=args.dealias,
        ring_rel_width=args.ring_rel_width,
        batch=args.batch,
    )

    kernels = setup_kernels(cfg)
    writer = CsvWriter(args.outdir)

    env = {"jax_version": getattr(jax, "__version__", "unknown"),
           "devices": [str(d) for d in jax.devices()],
           "platform": jax.default_backend(),
           "cfg": cfg.__dict__}
    with (Path(args.outdir) / "env.json").open("w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)

    r_list = _parse_list_floats(args.r_values)
    q0_list = _parse_list_floats(args.q0_values)
    if not r_list or not q0_list:
        raise SystemExit("Provide non-empty --r-values and --q0-values")

    seeds = np.arange(int(args.seed_start), int(args.seed_start) + int(args.n_seeds), dtype=np.int32)
    seen = _load_seen(writer.csv_path) if args.resume else set()

    total_jobs = len(r_list) * len(q0_list) * len(seeds)
    done = 0
    t0 = time.time()

    for r in r_list:
        for q0 in q0_list:
            for seed in seeds:
                if (r, q0, int(seed)) in seen:
                    done += 1
                    continue
                u0 = kernels["init"](int(seed))
                rr = jnp.asarray(r, dtype=jnp.float32)
                qq = jnp.asarray(q0, dtype=jnp.float32)
                tt = time.time()
                u, u_hat = kernels["integrate"](u0, rr, qq)
                u = jax.block_until_ready(u)
                u_hat = jax.block_until_ready(u_hat)
                amp, ring1, harm, broad, p2, p6, kp = kernels["extract"](u, u_hat, qq)
                wall = (time.time() - tt)
                status = "finite"
                if not np.all(np.isfinite(np.array(u))):
                    status = "nonfinite"
                writer.write_row(r,q0,int(seed),
                                 float(amp),float(ring1),float(harm),float(broad),
                                 float(p2),float(p6),float(kp),status,float(wall))
                done += 1
            elapsed = time.time() - t0
            rate = done / max(1e-9, elapsed)
            eta = (total_jobs - done) / max(1e-9, rate)
            print(f"progress {done}/{total_jobs} | eta {eta/3600:.2f}h | (r={r}, q0={q0})")

if __name__ == "__main__":
    main()
