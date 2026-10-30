"""Figures quoted from papers and reports → data/processed/literature_figures.csv.

Every row in data/manual/literature_figures.csv names the macro it becomes,
the number, how to format it, and the bib key and page it comes from.
export_stats.py turns each row into a \\newcommand automatically, so a
number quoted from the literature is entered exactly once, with its source.
"""

from __future__ import annotations

import pandas as pd

from _common import MANUAL, write_csv

REQUIRED = ["macro", "value", "unit", "fmt", "year", "source_key", "page"]
FORMATS = {"int", "pct", "usd", "gbp", "millions"}


def main() -> None:
    frame = pd.read_csv(MANUAL / "literature_figures.csv")
    missing = frame[REQUIRED].isna().any(axis=1)
    if missing.any():
        raise SystemExit(f"rows missing required fields:\n{frame[missing]}")
    bad = ~frame["fmt"].isin(FORMATS)
    if bad.any():
        raise SystemExit(f"unknown fmt:\n{frame[bad]}")
    dupes = frame["macro"].duplicated()
    if dupes.any():
        raise SystemExit(f"duplicate macros: {list(frame.loc[dupes, 'macro'])}")
    write_csv(frame.sort_values("macro"), "literature_figures.csv")


if __name__ == "__main__":
    main()
