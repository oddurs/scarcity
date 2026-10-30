"""Fetch Global Findex account-ownership series via the World Bank API.

Findex lives in database 28 (2025 edition, survey year 2024). Its regional
aggregate for sub-Saharan Africa is SSA (excluding high income); WDI's SSF
code returns nothing here. Cached like fetch_wdi.py; --refresh to re-download.
Licence: CC BY 4.0. See data/SOURCES.md.
"""

from __future__ import annotations

import wbgapi as wb

from _common import RAW, REFRESH

INDICATORS = {
    "account.t.d": "Account (% age 15+)",
    "fiaccount.t.d": "Financial institution account (% age 15+)",
    "mobileaccount.t.d": "Mobile money account (% age 15+)",
}
ECONOMIES = ["WLD", "SSA", "KEN", "TZA", "UGA", "GHA", "NGA", "IND", "PHL"]
FINDEX_DB = 28


def main() -> None:
    out_dir = RAW / "findex"
    out_dir.mkdir(parents=True, exist_ok=True)
    for code, label in INDICATORS.items():
        path = out_dir / f"{code}.csv"
        if path.exists() and not REFRESH:
            print(f"  cached {code}")
            continue
        print(f"  fetching {code}: {label}")
        frame = wb.data.DataFrame(code, ECONOMIES, db=FINDEX_DB, columns="time", numericTimeKeys=True)
        long = (frame.reset_index()
                     .melt(id_vars="economy", var_name="year", value_name="value")
                     .dropna()
                     .assign(indicator=code)
                     .sort_values(["economy", "year"]))
        long[["indicator", "economy", "year", "value"]].to_csv(path, index=False, lineterminator="\n")


if __name__ == "__main__":
    main()
