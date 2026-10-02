from __future__ import annotations

from pathlib import Path


def main() -> None:
    path = Path("인간의 본성은 추악하다. txt.txt")
    s = path.read_text(encoding="utf-8", errors="ignore")
    terms = ["HOMO", "habilis", "erectus", "cannib", "식인", "호모", "하빌", "에렉", "네안데", "강간", "rape"]
    print("chars", len(s))
    for term in terms:
        idx = s.lower().find(term.lower())
        if idx == -1:
            continue
        a = max(0, idx - 200)
        b = min(len(s), idx + 400)
        snippet = s[a:b].replace("\r", " ").replace("\n", " ")
        print()
        print(term, idx)
        print(snippet)


if __name__ == "__main__":
    main()
