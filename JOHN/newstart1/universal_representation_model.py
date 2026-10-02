"""Universal mathematical representation for the repo's bridge-state system.

This is a compact formalization of the recurring structure in the D3 / spiral /
bridge logs:
    atoms -> particles -> bridges -> archetypes -> closure

The goal is not to freeze one numeric legend, but to provide a reusable
representation that can absorb new bridge instances and still project them into
the same state-space.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from functools import lru_cache
from typing import Dict, Iterable, List, Mapping, Tuple
from collections import Counter

import numpy as np


ARCHETYPES: Tuple[str, ...] = ("BM", "BW", "SM", "SW")
PARTICLES: Tuple[str, ...] = ("gamma", "p", "nu", "e")

# Higher-order coordinates that let the same bridge algebra act on
# subject/state, condition, and spacetime context simultaneously.
CONDITION_AXES: Tuple[str, ...] = (
    "stress",
    "non_stress",
    "assault",
    "hospitality",
)
SPACETIME_AXES: Tuple[str, ...] = (
    "time",
    "space",
    "curvature",
    "causality",
)
UNIVERSE_AXES: Tuple[str, ...] = (
    "particle",
    "force",
    "gate",
    "bridge",
    "observer",
    "constant",
    "condition",
    "spacetime",
)


@dataclass(frozen=True)
class Bridge:
    name: str
    left: str
    right: str
    kind: str
    weight: float
    level: int

    def archetype_pair(self) -> Tuple[str, str]:
        return (self.left, self.right)


BRIDGES: Tuple[Bridge, ...] = (
    Bridge("GLUON_QUARK", "BM", "BM", "core_binding", 3.75, 1),
    Bridge("QUARK_PROTON", "BM", "BW", "structure", 3.25, 1),
    Bridge("NAM_NAM_BRIDGE", "BW", "SM", "strong_force", 2.75, 2),
    Bridge("NEUTRON_ELECTRON", "SM", "SW", "weak_transfer", 1.75, 2),
    Bridge("PHOTOELECTRIC", "BM", "SW", "em_surface", 2.5, 2),
    Bridge("BREMSSTRAHLUNG", "SW", "BM", "em_radiation", 1.5, 2),
    Bridge("BETA_DECAY", "SM", "BW", "decay", 2.0, 2),
    Bridge("HIGGS_TRAPEZIUS", "BW", "BW", "mass_anchor", 2.25, 3),
    Bridge("QUARK_GLUE_RECURSION", "BM", "BM", "recursive_binding", 3.5, 1),
    Bridge("ELECTRON_COMMAND", "SW", "SW", "control", 1.0, 3),
    Bridge("YEO_YEO_BRIDGE", "BW", "SW", "filter", 2.0, 2),
    Bridge("DOPAMINE_VETO", "BM", "BM", "veto", 1.25, 3),
    Bridge("OMEGA_CLOSURE", "BM", "SW", "closure", 4.0, 4),
)


PARTICLE_TO_ARCHETYPE: Dict[str, str] = {
    "gamma": "BM",
    "p": "BW",
    "nu": "SM",
    "e": "SW",
}

KNOWN_BRIDGE_TOKENS: Tuple[str, ...] = tuple(bridge.name for bridge in BRIDGES)
NUMERIC_ANCHOR_PATTERN = re.compile(r"(?<![\w.])(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?")
CORE_CORPUS_HINTS: Tuple[str, ...] = (
    "mathematical_representation.md",
    "D3_Higgs_Decoder_Paper.md",
    "D3_HIGGS_DECODER_FINAL.md",
    "D3_HIGGS_UNIFIED_THEORY.md",
    "D3_HIGGS_UNIFIED_THEORY_v2.md",
    "SPIRAL_PHYSICS_MAPPING.md",
    "gemini 연산자.txt",
    "gemini1.txt",
    "gemini2.txt",
    "gemini3.txt",
    "gemini4.txt",
    "gemini5.txt",
    "gemini9.txt",
)


def _iter_corpus_files(root: Path, hints: Tuple[str, ...] | None = None) -> Iterable[Path]:
    if hints:
        for hint in hints:
            path = root / hint
            if path.is_file():
                yield path
        return
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            yield path


@lru_cache(maxsize=8)
def extract_corpus_signals(root: str | Path = ".", use_core_hints: bool = True) -> Dict[str, object]:
    """Extract bridge names and numeric anchors from the repo corpus."""

    root_path = Path(root)
    bridge_hits: Dict[str, int] = {name: 0 for name in KNOWN_BRIDGE_TOKENS}
    numeric_hist: Dict[str, int] = {}
    files_scanned = 0

    hints = CORE_CORPUS_HINTS if use_core_hints else None
    for path in _iter_corpus_files(root_path, hints=hints):
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for token in KNOWN_BRIDGE_TOKENS:
            if token in text:
                bridge_hits[token] += text.count(token)

        for match in NUMERIC_ANCHOR_PATTERN.findall(text):
            numeric_hist[match] = numeric_hist.get(match, 0) + 1

    return {
        "files_scanned": files_scanned,
        "bridge_hits": {k: v for k, v in bridge_hits.items() if v > 0},
        "numeric_anchors": dict(sorted(numeric_hist.items(), key=lambda item: (-item[1], item[0]))),
    }


def infer_numeric_hierarchy(numeric_anchors: Mapping[str, int]) -> Dict[str, List[Tuple[str, int]]]:
    """Split corpus numbers into likely core anchors and downstream labels."""

    items = Counter(numeric_anchors)
    core: List[Tuple[str, int]] = []
    derived: List[Tuple[str, int]] = []
    labels: List[Tuple[str, int]] = []

    for token, count in items.most_common():
        if token in {"0", "1", "2", "3", "4", "8", "13", "128"} or "." in token:
            core.append((token, count))
        elif count >= 100:
            derived.append((token, count))
        else:
            labels.append((token, count))

    return {
        "core": core,
        "derived": derived,
        "labels": labels,
    }


def bridge_matrix() -> np.ndarray:
    """Adjacency matrix in archetype space, accumulated by bridge weight."""

    idx = {a: i for i, a in enumerate(ARCHETYPES)}
    mat = np.zeros((4, 4), dtype=float)
    for bridge in BRIDGES:
        i = idx[bridge.left]
        j = idx[bridge.right]
        mat[i, j] += bridge.weight
    return mat


def closure_vector() -> np.ndarray:
    """Return the normalized closure vector of the 4 archetypes."""

    mat = bridge_matrix()
    vec = mat.sum(axis=0) + mat.sum(axis=1)
    total = float(np.sum(vec))
    if total <= 0:
        return vec
    return vec / total


def bridge_levels() -> Dict[int, List[str]]:
    levels: Dict[int, List[str]] = {}
    for bridge in BRIDGES:
        levels.setdefault(bridge.level, []).append(bridge.name)
    return {k: sorted(v) for k, v in levels.items()}


def induced_state(state: Mapping[str, float]) -> Dict[str, float]:
    """Project an arbitrary state onto the archetype basis."""

    out = {a: float(state.get(a, 0.0)) for a in ARCHETYPES}
    total = sum(out.values()) or 1.0
    for key in out:
        out[key] /= total
    return out


def state_transition(state: Mapping[str, float]) -> Dict[str, float]:
    """One formal transition step under the bridge algebra.

    x' = normalize(x + A x)
    where A is the bridge adjacency matrix.
    """

    x = np.array([float(state.get(a, 0.0)) for a in ARCHETYPES], dtype=float)
    A = bridge_matrix()
    x2 = x + A @ x
    total = float(x2.sum())
    if total <= 0:
        return {a: 0.0 for a in ARCHETYPES}
    x2 /= total
    return {a: float(x2[i]) for i, a in enumerate(ARCHETYPES)}


def normalize_vector(state: Mapping[str, float], axes: Tuple[str, ...]) -> np.ndarray:
    """Normalize an arbitrary vector on the requested axes."""

    vec = np.array([float(state.get(axis, 0.0)) for axis in axes], dtype=float)
    total = float(vec.sum())
    if total <= 0:
        return vec
    return vec / total


def universal_state(
    state: Mapping[str, float],
    conditions: Mapping[str, float] | None = None,
    spacetime: Mapping[str, float] | None = None,
) -> Dict[str, np.ndarray]:
    """Pack the model into a single three-part representation.

    The repo's bridge algebra acts on a subject/state vector, while the
    condition and spacetime vectors modulate how that state should be read.
    """

    conditions = conditions or {}
    spacetime = spacetime or {}
    return {
        "state": normalize_vector(state, ARCHETYPES),
        "condition": normalize_vector(conditions, CONDITION_AXES),
        "spacetime": normalize_vector(spacetime, SPACETIME_AXES),
    }


def universe_state(
    state: Mapping[str, float],
    *,
    particle: Mapping[str, float] | None = None,
    force: Mapping[str, float] | None = None,
    gate: Mapping[str, float] | None = None,
    bridge: Mapping[str, float] | None = None,
    observer: Mapping[str, float] | None = None,
    constant: Mapping[str, float] | None = None,
    condition: Mapping[str, float] | None = None,
    spacetime: Mapping[str, float] | None = None,
) -> Dict[str, np.ndarray]:
    """Pack the whole model into a single eight-part universe vector set."""

    return {
        "state": normalize_vector(state, ARCHETYPES),
        "particle": normalize_vector(particle or {}, PARTICLES),
        "force": normalize_vector(force or {}, ("strong", "weak", "em", "closure")),
        "gate": normalize_vector(gate or {}, ("open", "closed", "threshold", "escape")),
        "bridge": normalize_vector(bridge or {}, tuple(bridge.name for bridge in BRIDGES)),
        "observer": normalize_vector(observer or {}, ("w_gate", "melatonin", "consciousness", "d3")),
        "constant": normalize_vector(constant or {}, ("0.2828", "1.4", "7.4", "138.88")),
        "condition": normalize_vector(condition or {}, CONDITION_AXES),
        "spacetime": normalize_vector(spacetime or {}, SPACETIME_AXES),
    }


def universal_transition(
    state: Mapping[str, float],
    conditions: Mapping[str, float] | None = None,
    spacetime: Mapping[str, float] | None = None,
) -> Dict[str, np.ndarray]:
    """Advance the full representation by one bridge step.

    We keep the archetype dynamics explicit and let condition/spacetime act as
    contextual weights rather than pretending they are frozen constants.
    """

    packed = universal_state(state, conditions=conditions, spacetime=spacetime)
    next_state = np.array(
        [state_transition({a: packed["state"][i] for i, a in enumerate(ARCHETYPES)})[a] for a in ARCHETYPES],
        dtype=float,
    )

    condition_gain = float(packed["condition"].dot(np.array([0.8, 0.6, 1.0, 0.7], dtype=float))) if packed["condition"].size else 0.0
    spacetime_gain = float(packed["spacetime"].dot(np.array([0.9, 0.8, 1.1, 1.0], dtype=float))) if packed["spacetime"].size else 0.0
    contextual_scale = 1.0 + 0.25 * condition_gain + 0.15 * spacetime_gain
    next_state = next_state * contextual_scale
    total = float(next_state.sum())
    if total > 0:
        next_state /= total
    return {
        "state": next_state,
        "condition": packed["condition"],
        "spacetime": packed["spacetime"],
    }


def universe_transition(
    state: Mapping[str, float],
    *,
    particle: Mapping[str, float] | None = None,
    force: Mapping[str, float] | None = None,
    gate: Mapping[str, float] | None = None,
    bridge: Mapping[str, float] | None = None,
    observer: Mapping[str, float] | None = None,
    constant: Mapping[str, float] | None = None,
    condition: Mapping[str, float] | None = None,
    spacetime: Mapping[str, float] | None = None,
) -> Dict[str, np.ndarray]:
    """Advance the full universe representation by one step."""

    packed = universe_state(
        state,
        particle=particle,
        force=force,
        gate=gate,
        bridge=bridge,
        observer=observer,
        constant=constant,
        condition=condition,
        spacetime=spacetime,
    )
    state_step = state_transition({a: packed["state"][i] for i, a in enumerate(ARCHETYPES)})
    base = np.array([state_step[a] for a in ARCHETYPES], dtype=float)
    observer_weight = float(packed["observer"].sum()) if packed["observer"].size else 0.0
    constant_weight = float(packed["constant"].sum()) if packed["constant"].size else 0.0
    scale = 1.0 + 0.1 * observer_weight + 0.05 * constant_weight
    base = base * scale
    total = float(base.sum())
    if total > 0:
        base /= total
    return {
        "state": base,
        "particle": packed["particle"],
        "force": packed["force"],
        "gate": packed["gate"],
        "bridge": packed["bridge"],
        "observer": packed["observer"],
        "constant": packed["constant"],
        "condition": packed["condition"],
        "spacetime": packed["spacetime"],
    }


def model_summary() -> Dict[str, object]:
    mat = bridge_matrix()
    corpus = extract_corpus_signals(".")
    hierarchy = infer_numeric_hierarchy(corpus["numeric_anchors"])
    return {
        "archetypes": list(ARCHETYPES),
        "particles": list(PARTICLES),
        "condition_axes": list(CONDITION_AXES),
        "spacetime_axes": list(SPACETIME_AXES),
        "universe_axes": list(UNIVERSE_AXES),
        "bridge_count": len(BRIDGES),
        "bridge_levels": bridge_levels(),
        "adjacency": mat.tolist(),
        "closure": closure_vector().tolist(),
        "corpus": corpus,
        "numeric_hierarchy": hierarchy,
    }


if __name__ == "__main__":
    summary = model_summary()
    print(summary)
