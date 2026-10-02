import argparse
import json
import os
from pathlib import Path

import pandas as pd


def _load_particle_sweep(csv_path: Path, prefix: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.copy()
    df["n"] = df["n"].astype(int)
    df = df.add_prefix(prefix)
    df = df.rename(columns={f"{prefix}n": "n"})
    return df


def _load_bio_schedule(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.copy()
    if "window" not in df.columns:
        raise ValueError("Bio schedule CSV must have a 'window' column (0..127).")
    df["window"] = df["window"].astype(int)
    df["n"] = df["window"] + 1
    return df


def _ensure_128(df: pd.DataFrame, name: str, key_col: str = "n") -> None:
    if key_col not in df.columns:
        raise ValueError(f"{name} must have column {key_col!r}.")
    uniq = sorted(set(int(x) for x in df[key_col].tolist()))
    if uniq != list(range(1, 129)):
        raise ValueError(f"{name} must cover n=1..128 exactly (got {uniq[:5]}...{uniq[-5:]}).")


def _top_corr(
    merged: pd.DataFrame, particle_col: str, bio_cols: list[str], k: int = 24
) -> pd.DataFrame:
    x = merged[particle_col].astype(float)
    rows = []
    for col in bio_cols:
        y = merged[col].astype(float)
        c = float(x.corr(y))
        rows.append({"particle_col": particle_col, "bio_col": col, "corr": c, "abs_corr": abs(c)})
    out = pd.DataFrame(rows).sort_values(["abs_corr", "bio_col"], ascending=[False, True]).head(k)
    return out.reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join particle-128 Mandelbrot/Julia sweep with biology-128 schedule to form an interface dataset."
    )
    parser.add_argument(
        "--particle-real",
        default="analysis_results/veins_pocket_tunnel/sweep_128/sweep_128_real.csv",
        help="Particle sweep CSV for c=n/128 (real axis)",
    )
    parser.add_argument(
        "--particle-spark-ray",
        default="analysis_results/veins_pocket_tunnel/sweep_128/sweep_128_spark_ray.csv",
        help="Particle sweep CSV for c=(n/128)*exp(i*138.88°)",
    )
    parser.add_argument(
        "--bio-schedule",
        default="HOMEOSTASIS_24_SCHEDULE_128.csv",
        help="Biology schedule CSV (128 rows, window 0..127)",
    )
    parser.add_argument(
        "--out",
        default="analysis_results/veins_pocket_tunnel/interface_128",
        help="Output directory",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df_real = _load_particle_sweep(Path(args.particle_real), "p_real_")
    df_ray = _load_particle_sweep(Path(args.particle_spark_ray), "p_ray_")
    df_bio = _load_bio_schedule(Path(args.bio_schedule))

    _ensure_128(df_real, "particle-real")
    _ensure_128(df_ray, "particle-spark-ray")
    _ensure_128(df_bio, "bio-schedule")

    merged = df_bio.merge(df_real, on="n", how="inner").merge(df_ray, on="n", how="inner")

    # Add canonical graph paths for easy loading into MANDELBROT_POCKET_FOLD.html
    merged["p_real_graph_path"] = merged["n"].apply(
        lambda n: f"analysis_results/veins_pocket_tunnel/sweep_128/veins_sweep_real_n{int(n):03d}_graph.json"
    )
    merged["p_ray_graph_path"] = merged["n"].apply(
        lambda n: f"analysis_results/veins_pocket_tunnel/sweep_128/veins_sweep_spark_ray_n{int(n):03d}_graph.json"
    )

    out_csv = out_dir / "biophysics_interface_128.csv"
    merged.to_csv(out_csv, index=False)

    # Quick correlation scan: particle morphology ↔ bio u_* channels (float)
    bio_u_cols = [c for c in merged.columns if c.startswith("u_")]
    particle_cols = [
        "p_real_poly_total_length",
        "p_real_tunnel_total_length",
        "p_real_polylines",
        "p_real_nodes",
        "p_ray_poly_total_length",
        "p_ray_tunnel_total_length",
        "p_ray_polylines",
        "p_ray_nodes",
    ]
    corr_rows = []
    for pcol in particle_cols:
        if pcol not in merged.columns:
            continue
        corr_rows.append(_top_corr(merged, pcol, bio_u_cols, k=24))
    corr = pd.concat(corr_rows, ignore_index=True) if corr_rows else pd.DataFrame()
    out_corr = out_dir / "biophysics_interface_top_corr.csv"
    corr.to_csv(out_corr, index=False)

    meta = {
        "particle_real_csv": str(Path(args.particle_real)),
        "particle_spark_ray_csv": str(Path(args.particle_spark_ray)),
        "bio_schedule_csv": str(Path(args.bio_schedule)),
        "rows": int(len(merged)),
        "bio_u_cols": int(len(bio_u_cols)),
        "particle_cols_scanned": particle_cols,
        "outputs": {
            "merged_csv": str(out_csv),
            "top_corr_csv": str(out_corr),
        },
        "note": "This builds a joined dataset; the actual bio→physics parameter mapping (leak/epsilon/c_eff) can be added next.",
    }
    (out_dir / "biophysics_interface_128_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_corr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

