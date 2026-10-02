import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

import fusion_core as k8


def _parse_weights(s: str) -> tuple[float, float]:
    parts = [p.strip() for p in str(s).split(",") if p.strip()]
    if len(parts) != 2:
        raise ValueError(f"--weights must be 'a,b' (got {s!r})")
    return float(parts[0]), float(parts[1])


def _load_positions(path: Path | None) -> dict[str, tuple[float, float]]:
    if path is None:
        # Deterministic fallback layout (6x5). Replace with an anatomical map when ready.
        positions: dict[str, tuple[float, float]] = {}
        cols, rows = 6, 5
        for i, name in enumerate(k8.CHANNEL_ORDER):
            col = i % cols
            row = i // cols
            x = (col + 0.5) * (128.0 / cols)
            y = (row + 0.5) * (128.0 / rows)
            positions[name] = (x, y)
        return positions

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError(f"positions json must be a dict channel->(x,y), got {type(raw)}")
    positions = {}
    for name in k8.CHANNEL_ORDER:
        xy = raw.get(name)
        if xy is None:
            raise KeyError(f"Missing channel position for {name!r} in {str(path)!r}")
        if (
            not isinstance(xy, (list, tuple))
            or len(xy) != 2
            or not isinstance(xy[0], (int, float))
            or not isinstance(xy[1], (int, float))
        ):
            raise TypeError(f"Position for {name!r} must be [x,y] numbers, got {xy!r}")
        positions[name] = (float(xy[0]), float(xy[1]))
    return positions


def _load_vector(path: Path) -> np.ndarray:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        v = np.asarray(raw, dtype=float).ravel()
        if v.size != len(k8.CHANNEL_ORDER):
            raise ValueError(f"Vector list must have length {len(k8.CHANNEL_ORDER)}")
        return v
    if isinstance(raw, dict):
        v = np.zeros(len(k8.CHANNEL_ORDER), dtype=float)
        for i, name in enumerate(k8.CHANNEL_ORDER):
            v[i] = float(raw.get(name, 0.0))
        return v
    raise TypeError("Vector json must be a list[30] or dict[channel->value].")


def _vector_from_phase(phase_key: str, no_control_value: float) -> np.ndarray:
    states = k8.resolve_phase_states(phase_key)
    return k8.states_to_channel_vector(states, no_control_value=no_control_value)


def _node_mask(node_set: str) -> np.ndarray:
    mask = np.ones(len(k8.CHANNEL_ORDER), dtype=float)
    if node_set == "28":
        for name in ("muscle_a", "muscle_b"):
            mask[k8.CHANNEL_ORDER.index(name)] = 0.0
    elif node_set != "30":
        raise ValueError("--node-set must be '30' or '28'")
    return mask


def _gaussian_weights(
    positions: dict[str, tuple[float, float]],
    sigma: float,
    mask: np.ndarray,
) -> np.ndarray:
    yy, xx = np.mgrid[0:128, 0:128]
    weights = np.zeros((len(k8.CHANNEL_ORDER), 128, 128), dtype=float)
    denom = 2.0 * float(sigma) * float(sigma)
    for i, name in enumerate(k8.CHANNEL_ORDER):
        if mask[i] <= 0.0:
            continue
        cx, cy = positions[name]
        dist2 = (xx - cx) ** 2 + (yy - cy) ** 2
        weights[i] = np.exp(-dist2 / denom)
    return weights


def _field_from_u(u: np.ndarray, weights: np.ndarray) -> np.ndarray:
    # Barycentric normalization so the field stays in the scale of u (u in [0..1]).
    wsum = weights.sum(axis=0)
    wsum = np.where(wsum <= 1e-12, 1.0, wsum)
    return (u[:, None, None] * weights).sum(axis=0) / wsum


def _render_heatmap(field: np.ndarray, out_path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="white")
    ax.set_facecolor("white")
    im = ax.imshow(field, cmap="coolwarm", origin="lower")
    ax.set_title(title, fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Potential (arb.)")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Render a 128x128 potential field from 30-channel control vectors."
    )
    ap.add_argument("--positions", type=Path, default=None, help="JSON mapping channel-> [x,y] in 0..127.")
    ap.add_argument("--phase-a", type=str, default="phase1", help=f"Phase key for vector A (have: {sorted(k8.PHASE_TABLE)}).")
    ap.add_argument("--phase-b", type=str, default="phase2", help="Phase key for vector B.")
    ap.add_argument("--vector-a", type=Path, default=None, help="Override vector A with JSON list[30] or dict.")
    ap.add_argument("--vector-b", type=Path, default=None, help="Override vector B with JSON list[30] or dict.")
    ap.add_argument("--no-control", type=float, default=0.5, help="Numeric value for 'no_control' state.")
    ap.add_argument("--node-set-a", type=str, default="30", help="Use '30' or '28' (exclude muscle_a/b).")
    ap.add_argument("--node-set-b", type=str, default="30", help="Use '30' or '28' (exclude muscle_a/b).")
    ap.add_argument("--sigma", type=float, default=12.0, help="Gaussian kernel sigma (pixels).")
    ap.add_argument("--weights", type=str, default="1,1", help="Potential difference weights 'a,b' (e.g. '7,1').")
    ap.add_argument("--out", type=Path, default=Path("artifacts/field_128_potential_diff.png"))
    args = ap.parse_args(argv)

    w_a, w_b = _parse_weights(args.weights)
    positions = _load_positions(args.positions)

    if args.vector_a is not None:
        u_a = _load_vector(args.vector_a)
    else:
        u_a = _vector_from_phase(args.phase_a, no_control_value=args.no_control)
    if args.vector_b is not None:
        u_b = _load_vector(args.vector_b)
    else:
        u_b = _vector_from_phase(args.phase_b, no_control_value=args.no_control)

    mask_a = _node_mask(args.node_set_a)
    mask_b = _node_mask(args.node_set_b)
    weights_a = _gaussian_weights(positions, sigma=args.sigma, mask=mask_a)
    weights_b = _gaussian_weights(positions, sigma=args.sigma, mask=mask_b)

    field_a = _field_from_u(u_a, weights_a)
    field_b = _field_from_u(u_b, weights_b)
    field_diff = (w_a * field_a) - (w_b * field_b)

    title = f"Potential diff: ({w_a:g}*{args.phase_a}/{args.node_set_a}) - ({w_b:g}*{args.phase_b}/{args.node_set_b})"
    _render_heatmap(field_diff, args.out, title=title)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
