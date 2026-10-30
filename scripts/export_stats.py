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


def m_whole(value: float) -> str:
    return f"{value:.0f}~million"


def m_one(value: float) -> str:
    return f"{value:.1f}~million"


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


def headline(series: str, entity: str, year_: int) -> Callable[[pd.DataFrame], float]:
    """One hand-entered report figure (data/manual/report_headlines.csv)."""
    return lambda d: d.loc[(d["series"] == series) & (d["entity"] == entity)
                           & (d["year"] == year_), "value"].item()


def cell(economy: str, column: str) -> Callable[[pd.DataFrame], float]:
    """One value from a per-economy summary table."""
    return lambda d: d.set_index("economy").loc[economy, column]


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
LEAP = "leapfrog_summary.csv"
OFFGRID = "offgrid_solar.csv"
HEAD = "report_headlines.csv"

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

    # Leapfrogging: subscriptions per 100 people (WDI IT.MLT.MAIN.P2, IT.CEL.SETS.P2)
    Stat("sspFixedPeak", LEAP, cell("SSF", "fixed_peak"), lambda v: number(v, 1), "SSA fixed lines per 100, peak"),
    Stat("sspFixedPeakYear", LEAP, cell("SSF", "fixed_peak_year"), year, "Year of that peak"),
    Stat("sspMobileSubs", LEAP, cell("SSF", "mobile_latest"), number, "SSA mobile subscriptions per 100, latest"),
    Stat("sspMobileSubsYear", LEAP, cell("SSF", "latest_year"), year, "Latest year of SSA subscriptions"),
    Stat("kenFixedPeak", LEAP, cell("KEN", "fixed_peak"), lambda v: number(v, 1), "Kenya fixed lines per 100, peak"),
    Stat("kenMobileSubs", LEAP, cell("KEN", "mobile_latest"), number, "Kenya mobile subscriptions per 100, latest"),
    Stat("usaFixedPeak", LEAP, cell("USA", "fixed_peak"), number, "US fixed lines per 100, peak"),

    # Off-grid solar users in SSA (IRENA 2025 edition; Africa minus North Africa)
    Stat("sspSolarUsers", OFFGRID, latest("total"), m_whole, "SSA people using off-grid solar, latest"),
    Stat("sspSolarUsersStart", OFFGRID, first("total"), m_whole, "SSA people using off-grid solar, first year"),
    Stat("sspSolarYear", OFFGRID, latest_year("total"), year, "Latest IRENA year"),
    Stat("sspSolarStartYear", OFFGRID, first_year("total"), year, "First IRENA year"),
    Stat("sspShsUsers", OFFGRID, latest("shs"), m_whole, "SSA solar home system users (11 W+), latest"),
    Stat("sspShsUsersStart", OFFGRID, first("shs"), m_one, "SSA solar home system users (11 W+), first year"),
    Stat("sspLightUsers", OFFGRID, latest("lights"), m_whole, "SSA solar light users (<11 W), latest"),

    # Report headlines (hand-entered with page numbers)
    Stat("sdgWithoutElecWorld", HEAD, headline("people_without_electricity", "World", 2024), m_whole, "Tracking SDG7 2026: people without electricity, world, 2024"),
    Stat("sdgWithoutElecSSA", HEAD, headline("people_without_electricity", "Sub-Saharan Africa", 2024), m_whole, "Tracking SDG7 2026: people without electricity, SSA, 2024"),
    Stat("sdgOffgridServed", HEAD, headline("people_served_offgrid_solar_tier1_2", "World", 2024), m_whole, "Tracking SDG7 2026: Tier 1-2 off-grid solar, world, 2024"),
    Stat("sdgOffgridServedPrev", HEAD, headline("people_served_offgrid_solar_tier1_2", "World", 2023), m_whole, "Tracking SDG7 2026: Tier 1-2 off-grid solar, world, 2023"),
    Stat("sdgOffgridBackupShare", HEAD, headline("offgrid_solar_users_using_as_backup", "World", 2024), pct, "Tracking SDG7 2026: share of off-grid solar users using it as grid backup"),
    Stat("goglaYear", HEAD, lambda d: d.loc[d["series"] == "solar_energy_kits_sold", "year"].item(), year, "GOGLA report year"),
    Stat("goglaKitsSold", HEAD, headline("solar_energy_kits_sold", "World", 2025), m_one, "GOGLA: solar kits sold by affiliates, 2025"),
    Stat("goglaPeopleServed", HEAD, headline("people_served_gogla_affiliates", "World", 2025), m_whole, "GOGLA: people served by affiliates, 2025"),
    Stat("gsmaRegisteredAccounts", HEAD, headline("mobile_money_registered_accounts", "World", 2025), lambda v: f"{v:.1f}~billion", "GSMA: registered mobile money accounts, 2025"),
    Stat("gsmaRegisteredSSA", HEAD, headline("mobile_money_registered_accounts", "Sub-Saharan Africa", 2025), lambda v: f"{v:.1f}~billion", "GSMA: registered accounts, SSA, 2025"),
    Stat("gsmaValueSSA", HEAD, headline("mobile_money_transaction_value", "Sub-Saharan Africa", 2025), lambda v: f"\\${v:.1f}~trillion", "GSMA: transaction value, SSA, 2025"),
    Stat("gsmaActiveAccounts", HEAD, headline("mobile_money_active_30day_accounts", "World", 2025), m_whole, "GSMA: 30-day active accounts, 2025"),
    Stat("gsmaTransactionValue", HEAD, headline("mobile_money_transaction_value", "World", 2025), lambda v: f"\\${v:.1f}~trillion", "GSMA: transaction value, 2025"),
]


LITERATURE_FORMATS: dict[str, Callable[[float], str]] = {
    "int": number,
    "pct": pct,
    "usd": lambda v: f"\\$\\num{{{v:.0f}}}",
    "gbp": lambda v: f"£\\num{{{v:.0f}}}",
    "millions": lambda v: f"{v:.0f}~million",
}


def literature_stats() -> list[Stat]:
    """One macro per row of the hand-entered literature figures."""
    path = PROCESSED / "literature_figures.csv"
    if not path.exists():
        return []
    rows = pd.read_csv(path)
    return [
        Stat(r.macro, "literature_figures.csv",
             lambda d, m=r.macro: d.loc[d["macro"] == m, "value"].item(),
             LITERATURE_FORMATS[r.fmt],
             f"{r.unit}, {r.year} ({r.source_key}, p. {r.page})")
        for r in rows.itertuples()
    ]


def main() -> None:
    lines = [
        "% generated/stats.tex — written by scripts/export_stats.py. Do not edit.",
        "",
    ]
    stats = STATS + literature_stats()
    for stat in sorted(stats, key=lambda s: s.macro):
        if not stat.macro.isalpha():
            raise ValueError(f"macro names must be letters only: {stat.macro}")
        frame = pd.read_csv(PROCESSED / stat.csv)
        value = stat.get(frame)
        lines.append(f"% {stat.note} [{stat.csv}]")
        lines.append(f"\\newcommand{{\\{stat.macro}}}{{{stat.fmt(value)}}}")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"stats: {len(stats)} macros -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
