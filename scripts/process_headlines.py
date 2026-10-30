"""Report headline figures → data/processed/report_headlines.csv.

Passes the hand-entered rows through unchanged apart from sorting, so that
export_stats.py reads every number from data/processed/ like everything else.
"""

from __future__ import annotations

import pandas as pd

from _common import MANUAL, write_csv


def main() -> None:
    frame = pd.read_csv(MANUAL / "report_headlines.csv")
    write_csv(frame.sort_values(["series", "entity", "year"]), "report_headlines.csv")


if __name__ == "__main__":
    main()
