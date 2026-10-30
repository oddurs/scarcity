"""Gate for `make final`: fail if the paper is not ready to release.

Checks, in order:
  1. no \\placeholder{...} or \\todo{...} left in the paper source
     (the preamble, which defines them, is exempt);
  2. no undefined citations or references in the LaTeX log;
  3. no citation key that biber could not find in references.bib.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
BUILD = PAPER / "build"

MARKER = re.compile(r"\\(placeholder|todo)\b")
LOG_PROBLEMS = [
    re.compile(r"Citation [`'].+?' .*undefined"),
    re.compile(r"Reference [`'].+?' .*undefined"),
    re.compile(r"There were undefined (references|citations)"),
    re.compile(r"Empty bibliography"),
]
BLG_PROBLEM = re.compile(r"WARN - I didn't find a database entry for '([^']+)'")


def strip_comment(line: str) -> str:
    return re.split(r"(?<!\\)%", line, maxsplit=1)[0]


def main() -> int:
    problems: list[str] = []

    sources = [p for p in PAPER.rglob("*.tex")
               if "preamble" not in p.parts and "build" not in p.parts]
    sources.append(PAPER / "main.tex")
    for path in sorted(set(sources)):
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if MARKER.search(strip_comment(line)):
                problems.append(f"{path.relative_to(ROOT)}:{n}: {line.strip()}")

    log = BUILD / "main.log"
    if not log.exists():
        problems.append("paper/build/main.log missing: build the PDF first")
    else:
        for line in log.read_text(errors="replace").splitlines():
            if any(p.search(line) for p in LOG_PROBLEMS):
                problems.append(f"main.log: {line.strip()}")

    blg = BUILD / "main.blg"
    if blg.exists():
        for key in BLG_PROBLEM.findall(blg.read_text(errors="replace")):
            problems.append(f"main.blg: no entry for citation key '{key}'")

    if problems:
        print(f"make final: {len(problems)} problem(s)\n")
        print("\n".join(f"  {p}" for p in problems))
        return 1
    print("make final: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
