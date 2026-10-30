"""Fetch World Development Indicators via the World Bank API (wbgapi).

Writes one untouched long-format CSV per indicator to data/raw/wdi/.
Cached: an existing file is reused unless --refresh is given, so builds are
repeatable offline and only change when we choose to refresh the data.
Licence: CC BY 4.0. See data/SOURCES.md.
"""

from __future__ import annotations

import wbgapi as wb

from _common import RAW, REFRESH

INDICATORS = {
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "EG.ELC.ACCS.RU.ZS": "Access to electricity, rural (% of rural population)",
    "SP.POP.TOTL": "Population, total",
    "SP.RUR.TOTL": "Rural population",
    "NY.GDP.PCAP.PP.KD": "GDP per capita, PPP (constant 2021 international $)",
    "IT.CEL.SETS.P2": "Mobile cellular subscriptions (per 100 people)",
}

# WLD world, SSF sub-Saharan Africa (all income levels), plus case countries.
ECONOMIES = ["WLD", "SSF", "KEN", "NGA", "ETH", "TZA", "UGA", "RWA", "IND", "PHL", "BRA", "USA"]
YEARS = range(1990, 2026)


def main() -> None:
    out_dir = RAW / "wdi"
    out_dir.mkdir(parents=True, exist_ok=True)
    for code, label in INDICATORS.items():
        path = out_dir / f"{code}.csv"
        if path.exists() and not REFRESH:
            print(f"  cached {code}")
            continue
        print(f"  fetching {code}: {label}")
        frame = wb.data.DataFrame(code, ECONOMIES, time=YEARS, db=2, columns="time", numericTimeKeys=True)
        long = (frame.reset_index()
                     .melt(id_vars="economy", var_name="year", value_name="value")
                     .dropna()
                     .assign(indicator=code)
                     .sort_values(["economy", "year"]))
        long[["indicator", "economy", "year", "value"]].to_csv(path, index=False, lineterminator="\n")


if __name__ == "__main__":
    main()
