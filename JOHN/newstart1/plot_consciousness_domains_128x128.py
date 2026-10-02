import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _save_heatmap(arr: np.ndarray, title: str, out_png: Path, *, cmap: str = "magma") -> None:
    plt.figure(figsize=(12, 7))
    plt.imshow(arr, aspect="auto", origin="lower", cmap=cmap)
    plt.colorbar()
    plt.title(title)
    plt.xlabel("archetype_n (1..128)")
    plt.ylabel("window/step (0..127)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot per-domain 128x128 heatmaps from CONSCIOUSNESS_FIELD CSV.")
    parser.add_argument(
        "--in",
        dest="in_csv",
        default="analysis_results/CONSCIOUSNESS_FIELD_128x128_fullX.csv",
        help="Input CSV with columns step, archetype_n, and x_00..x_23 domain columns.",
    )
    parser.add_argument("--out", default="analysis_results/consciousness_domains_128x128")
    parser.add_argument("--cmap", default="magma")
    args = parser.parse_args()

    in_csv = Path(args.in_csv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_csv)
    required = {"step", "archetype_n"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing} (in={str(in_csv)!r})")

    domain_cols = [c for c in df.columns if c.startswith("x_")]
    if not domain_cols:
        raise ValueError(f"No domain columns found (expected x_00_...); in={str(in_csv)!r}")

    df = df.copy()
    df["step"] = df["step"].astype(int)
    df["archetype_n"] = df["archetype_n"].astype(int)

    stats_rows: list[dict[str, object]] = []
    for col in domain_cols:
        pivot = df.pivot(index="step", columns="archetype_n", values=col).sort_index()
        arr = pivot.to_numpy(dtype=float)
        out_png = out_dir / f"heatmap_{col}.png"
        _save_heatmap(arr, title=col, out_png=out_png, cmap=str(args.cmap))

        finite = arr[np.isfinite(arr)]
        stats_rows.append(
            {
                "domain_col": col,
                "min": float(np.min(finite)) if finite.size else float("nan"),
                "max": float(np.max(finite)) if finite.size else float("nan"),
                "mean": float(np.mean(finite)) if finite.size else float("nan"),
                "std": float(np.std(finite)) if finite.size else float("nan"),
                "png": str(out_png),
            }
        )

    stats_csv = out_dir / "domain_stats.csv"
    pd.DataFrame(stats_rows).to_csv(stats_csv, index=False)

    meta = {
        "in_csv": str(in_csv),
        "out_dir": str(out_dir),
        "domain_cols": domain_cols,
        "domain_count": int(len(domain_cols)),
        "stats_csv": str(stats_csv),
    }
    (out_dir / "domain_plots_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote: {stats_csv}")
    print(f"Wrote: {out_dir / 'domain_plots_meta.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

