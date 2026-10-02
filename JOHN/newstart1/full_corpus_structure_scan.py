from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed


TEXT_EXTS = {
    ".md", ".txt", ".py", ".json", ".jsonl", ".csv", ".html", ".htm", ".php",
    ".js", ".ts", ".tsx", ".jsx", ".css", ".scss", ".less", ".tex", ".svg",
    ".ps1", ".qmd", ".log", ".ddl", ".h", ".hpp", ".c", ".cc", ".cpp", ".rs",
    ".go", ".java", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env", ".xml",
    ".mdx", ".r", ".m", ".swift", ".kt", ".sh", ".bat", ".cmd", ".sql"
}

NUM_PATTERN = re.compile(r"(?<![\w.])(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?")


def iter_files(root: Path) -> Iterable[Path]:
    proc = subprocess.run(["rg", "--files"], cwd=root, capture_output=True)
    proc.check_returncode()
    for line in proc.stdout.decode("utf-8", errors="ignore").splitlines():
        yield root / line


def main() -> None:
    root = Path(".").resolve()
    total = 0
    ext_counts = Counter()
    numeric_counts = Counter()
    token_counts = Counter()
    token_list = ("GLUON_QUARK", "QUARK_PROTON", "NAM_NAM_BRIDGE", "NEUTRON_ELECTRON",
                   "PHOTOELECTRIC", "BREMSSTRAHLUNG", "BETA_DECAY", "HIGGS_TRAPEZIUS",
                   "QUARK_GLUE_RECURSION", "ELECTRON_COMMAND", "YEO_YEO_BRIDGE",
                   "DOPAMINE_VETO", "OMEGA_CLOSURE", "BM", "BW", "SM", "SW")
    files = list(iter_files(root))
    total = len(files)

    def process(path: Path):
        if path.suffix.lower() not in TEXT_EXTS and path.suffix:
            return None
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None
        nums = Counter(NUM_PATTERN.findall(text))
        toks = Counter({tok: text.count(tok) for tok in token_list if tok in text})
        return path, nums, toks

    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = [ex.submit(process, path) for path in files]
        for fut in as_completed(futures):
            result = fut.result()
            if result is None:
                continue
            path, nums, toks = result
            ext_counts[path.suffix.lower()] += 1
            numeric_counts.update(nums)
            token_counts.update(toks)

    out = {
        "files_total": total,
        "files_scanned": sum(ext_counts.values()),
        "extensions": ext_counts.most_common(50),
        "top_numbers": numeric_counts.most_common(200),
        "top_tokens": token_counts.most_common(100),
    }
    Path("full_corpus_structure.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps({
        "files_total": total,
        "files_scanned": sum(ext_counts.values()),
        "top_numbers": numeric_counts.most_common(20),
        "top_tokens": token_counts.most_common(20),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
