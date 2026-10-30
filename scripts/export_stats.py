"""Write generated/stats.tex: one \\newcommand per number quoted in the prose.

Each statistic is declared once in STATS below, with the processed CSV it
comes from and how to round it. The prose only ever uses the macro, so a
data refresh updates every sentence at once and rounding stays consistent.
Output is deterministic (sorted, no timestamps) so diffs show real changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "generated" / "stats.tex"


# ---- formatting -----------------------------------------------------------

def pct(value: float, digits: int = 0) -> str:
    return f"{value:.{digits}f}\\%"


def number(value: float, digits: int = 0) -> str:
    return f"\\num{{{value:.{digits}f}}}"


def millions(value: float, digits: int = 0) -> str:
    return f"{value / 1e6:.{digits}f}~million"


def year(value: float) -> str:
    return f"{int(value)}"


# ---- declarations ---------------------------------------------------------

@dataclass(frozen=True)
class Stat:
    macro: str                         # without backslash, letters only
    csv: str                           # file in data/processed/
    get: Callable[[pd.DataFrame], float]
    fmt: Callable[[float], str]
    note: str                          # what it is, written into stats.tex


STATS: list[Stat] = [
    # Filled in as each dataset is wired up, e.g.
    # Stat("sspElecAccess", "electricity_access.csv",
    #      lambda d: d.query("iso3 == 'SSF'").sort_values("year").value.iloc[-1],
    #      lambda v: pct(v, 1), "Access to electricity, sub-Saharan Africa, latest year"),
]


def main() -> None:
    lines = [
        "% generated/stats.tex — written by scripts/export_stats.py. Do not edit.",
        "",
    ]
    for stat in sorted(STATS, key=lambda s: s.macro):
        if not stat.macro.isalpha():
            raise ValueError(f"macro names must be letters only: {stat.macro}")
        frame = pd.read_csv(PROCESSED / stat.csv)
        value = stat.get(frame)
        lines.append(f"% {stat.note} [{stat.csv}]")
        lines.append(f"\\newcommand{{\\{stat.macro}}}{{{stat.fmt(value)}}}")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"stats: {len(STATS)} macros -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
