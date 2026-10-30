"""Shared paths and helpers for the data pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
MANUAL = ROOT / "data" / "manual"
PROCESSED = ROOT / "data" / "processed"

REFRESH = "--refresh" in sys.argv


def write_csv(frame: pd.DataFrame, name: str) -> None:
    """Write a processed CSV deterministically. Missing values become `nan`,
    which pgfplots skips with `unbounded coords=jump`."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    path = PROCESSED / name
    frame.to_csv(path, index=False, na_rep="nan", float_format="%.4f", lineterminator="\n")
    print(f"  wrote {path.relative_to(ROOT)} ({len(frame)} rows)")
