"""Accumulate a shared vector core from the repo's geometry and D3 docs.

The goal is not to replace the source files, but to read them together and
distill the repeated mathematical skeleton into a single pruned registry.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parent

SOURCE_PATTERNS = [
    "mathematical_representation.md",
    "SPIRAL_PHYSICS_MAPPING.md",
    "FACE_BODY_SPIRAL_MAPPING.py",
    "D3_Higgs_Decoder_Paper.md",
    "D3_HIGGS_DECODER_FINAL.md",
    "D3_HIGGS_UNIFIED_THEORY.md",
    "D3_HIGGS_UNIFIED_THEORY_v2.md",
    "geometry_package/**/*.md",
    "geometry_package/**/*.py",
]

CANONICAL_AXES = ("stress", "non_stress", "assault", "hospitality")
TOKEN_TO_AXIS = {
    "spark": "stress",
    "proton": "stress",
    "gluon": "stress",
    "melatonin": "non_stress",
    "progesterone": "non_stress",
    "p": "non_stress",
    "neutrino": "assault",
    "quark": "assault",
    "n": "assault",
    "higgs": "hospitality",
    "endorphin": "hospitality",
    "e": "hospitality",
}

KEY_PATTERNS = {
    "triad": re.compile(r"Primordial Triad|Stage 1|3 Inputs|three primordial", re.I),
    "gate8": re.compile(r"8 Particles|8 Gates|8 fundamental", re.I),
    "channel64": re.compile(r"64[- ]Channel|64 channels|64 fundamental", re.I),
    "type128": re.compile(r"128 types|16 MBTI|4 Blood|2 Gender", re.I),
    "type146": re.compile(r"146 types|pregnenolone|left love", re.I),
    "spiral": re.compile(r"log spiral|spiral arm|hysteresis|spark", re.I),
    "vector": re.compile(r"vector|basis|matrix|axis", re.I),
}


@dataclass(frozen=True)
class SourceSummary:
    path: str
    signals: Dict[str, int]
    vector_hits: Dict[str, int]


def _iter_sources() -> Iterable[Path]:
    seen = set()
    for pattern in SOURCE_PATTERNS:
        for path in ROOT.glob(pattern):
            if path.is_file() and path.suffix.lower() in {".md", ".py"} and path not in seen:
                seen.add(path)
                yield path


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _scan_source(path: Path) -> SourceSummary:
    text = _read_text(path)
    signals = {name: len(regex.findall(text)) for name, regex in KEY_PATTERNS.items()}
    tokens = Counter(re.findall(r"[A-Za-z_]+", text.lower()))
    vector_hits = {axis: 0 for axis in CANONICAL_AXES}
    for token, axis in TOKEN_TO_AXIS.items():
        vector_hits[axis] += tokens.get(token, 0)
    return SourceSummary(path=str(path), signals=signals, vector_hits=vector_hits)


def accumulate_vector_core() -> Dict[str, object]:
    sources = [_scan_source(path) for path in _iter_sources()]
    total_signals = Counter()
    total_vectors = Counter()
    per_source = []
    for src in sources:
        total_signals.update(src.signals)
        total_vectors.update(src.vector_hits)
        per_source.append(
            {
                "path": src.path,
                "signals": src.signals,
                "vector_hits": src.vector_hits,
            }
        )

    basis = {
        axis: float(total_vectors.get(axis, 0)) for axis in CANONICAL_AXES
    }
    total = sum(basis.values()) or 1.0
    normalized = {axis: value / total for axis, value in basis.items()}

    clusters = defaultdict(list)
    for src in sources:
        hot_axis = max(src.vector_hits.items(), key=lambda kv: kv[1])[0] if src.vector_hits else "stress"
        clusters[hot_axis].append(src.path)

    return {
        "root": str(ROOT),
        "source_count": len(sources),
        "signals": dict(total_signals),
        "raw_axis_counts": basis,
        "normalized_axis_weights": normalized,
        "clusters": {axis: sorted(paths) for axis, paths in clusters.items()},
        "sources": per_source,
    }


def write_registry(output: Path | None = None) -> Path:
    registry = accumulate_vector_core()
    if output is None:
        output = ROOT / "vector_core_registry.json"
    output.write_text(json.dumps(registry, indent=2, ensure_ascii=True), encoding="utf-8")
    return output


if __name__ == "__main__":
    registry = accumulate_vector_core()
    print(json.dumps(
        {
            "source_count": registry["source_count"],
            "normalized_axis_weights": registry["normalized_axis_weights"],
            "signals": registry["signals"],
        },
        indent=2,
    ))
