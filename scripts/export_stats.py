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


def millions_from_m(value: float) -> str:
    """Value already in millions; rounded to the nearest 5 million, since the
    headcount is a product of two estimates and false precision would mislead."""
    return f"{5 * round(value / 5):.0f}~million"


def year(value: float) -> str:
    return f"{int(value)}"


# ---- selectors (all take the processed frame) -------------------------------

def latest(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d.dropna(subset=[column]).sort_values("year")[column].iloc[-1]


def latest_year(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d.dropna(subset=[column])["year"].max()


def first(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d.dropna(subset=[column]).sort_values("year")[column].iloc[0]


def first_year(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d.dropna(subset=[column])["year"].min()


def peak(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d[column].max()


def peak_year(column: str) -> Callable[[pd.DataFrame], float]:
    return lambda d: d.loc[d[column].idxmax(), "year"]


# ---- declarations ---------------------------------------------------------

@dataclass(frozen=True)
class Stat:
    macro: str                         # without backslash, letters only
    csv: str                           # file in data/processed/
    get: Callable[[pd.DataFrame], float]
    fmt: Callable[[float], str]
    note: str                          # what it is, written into stats.tex


ELEC = "electricity_access.csv"
FINDEX = "findex_accounts.csv"

STATS: list[Stat] = [
    # Electricity access (World Bank WDI, EG.ELC.ACCS.ZS; SSF = sub-Saharan Africa)
    Stat("sspElecAccess", ELEC, latest("ssf"), lambda v: pct(v), "SSA access to electricity, latest year"),
    Stat("sspElecYear", ELEC, latest_year("ssf"), year, "Latest year of SSA electricity data"),
    Stat("sspElecAccessStart", ELEC, first("ssf"), lambda v: pct(v), "SSA access to electricity, first year shown"),
    Stat("sspElecStartYear", ELEC, first_year("ssf"), year, "First year shown"),
    Stat("sspRuralElecAccess", ELEC, latest("ssf_rural"), lambda v: pct(v), "SSA rural access, latest year"),
    Stat("wldElecAccess", ELEC, latest("wld"), lambda v: pct(v), "World access to electricity, latest year"),
    Stat("kenElecAccess", ELEC, latest("ken"), lambda v: pct(v), "Kenya access to electricity, latest year"),
    Stat("sspWithoutElec", ELEC, latest("ssf_without_m"), millions_from_m, "People in SSA without electricity, latest year"),
    Stat("sspWithoutElecStart", ELEC, first("ssf_without_m"), millions_from_m, "People in SSA without electricity, first year shown"),
    Stat("sspWithoutElecPeak", ELEC, peak("ssf_without_m"), millions_from_m, "People in SSA without electricity, peak"),
    Stat("sspWithoutElecPeakYear", ELEC, peak_year("ssf_without_m"), year, "Year of that peak"),

    # Account ownership (Global Findex, db 28; SSA = sub-Saharan Africa excl. high income)
    Stat("findexYear", FINDEX, latest_year("ken_any"), year, "Latest Findex survey year"),
    Stat("kenAnyAccountStart", FINDEX, first("ken_any"), pct, "Kenya, any account, 2011"),
    Stat("kenAnyAccount", FINDEX, latest("ken_any"), pct, "Kenya, any account, latest"),
    Stat("kenMobileMoney", FINDEX, latest("ken_mm"), pct, "Kenya, mobile money account, latest"),
    Stat("kenBankAccount", FINDEX, latest("ken_fi"), pct, "Kenya, financial institution account, latest"),
    Stat("kenBankAccountPeak", FINDEX, peak("ken_fi"), pct, "Kenya, financial institution account, peak"),
    Stat("kenBankAccountPeakYear", FINDEX, peak_year("ken_fi"), year, "Year of that peak"),
    Stat("ssaMobileMoneyStart", FINDEX, first("ssa_mm"), pct, "SSA, mobile money account, first survey (2014)"),
    Stat("ssaMobileMoneyStartYear", FINDEX, first_year("ssa_mm"), year, "First survey asking about mobile money"),
    Stat("ssaMobileMoney", FINDEX, latest("ssa_mm"), pct, "SSA, mobile money account, latest"),
    Stat("ssaBankAccount", FINDEX, latest("ssa_fi"), pct, "SSA, financial institution account, latest"),
    Stat("ssaAnyAccount", FINDEX, latest("ssa_any"), pct, "SSA, any account, latest"),
    Stat("wldMobileMoney", FINDEX, latest("wld_mm"), pct, "World, mobile money account, latest"),
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
