from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional, Union


JsonLike = Union[dict[str, Any], list[Any], str, int, float, bool, None]


def load_registry(registry_path: Union[str, Path]) -> dict[str, Any]:
    path = Path(registry_path)
    return json.loads(path.read_text(encoding="utf-8"))


def get_by_dotted_path(obj: JsonLike, dotted_path: str) -> Any:
    cur: Any = obj
    for part in dotted_path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
            continue
        raise KeyError(dotted_path)
    return cur


def get_value(obj: JsonLike, dotted_path: str, default: Any = None) -> Any:
    try:
        node = get_by_dotted_path(obj, dotted_path)
    except KeyError:
        return default

    if isinstance(node, dict) and "value" in node:
        return node["value"]

    return node
