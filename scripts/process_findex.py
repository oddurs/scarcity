"""Account ownership by type → data/processed/findex_accounts.csv.

One row per Findex survey year (2011, 2014, 2017, 2021, 2024). For each of
Kenya (ken), sub-Saharan Africa excluding high income (ssa) and the world
(wld): any account, financial-institution account (fi) and mobile money
account (mm), all % of adults 15+. Mobile money was not asked in 2011.
"""

from __future__ import annotations

import pandas as pd

from _common import RAW, write_csv

CODES = {"account.t.d": "any", "fiaccount.t.d": "fi", "mobileaccount.t.d": "mm"}
ECONOMIES = {"KEN": "ken", "SSA": "ssa", "WLD": "wld"}


def main() -> None:
    frames = [pd.read_csv(RAW / "findex" / f"{code}.csv") for code in CODES]
    long = pd.concat(frames)
    long = long[long["economy"].isin(ECONOMIES)]
    long["column"] = long["economy"].map(ECONOMIES) + "_" + long["indicator"].map(CODES)
    wide = long.pivot(index="year", columns="column", values="value").sort_index()
    columns = [f"{e}_{c}" for e in ECONOMIES.values() for c in CODES.values()]
    write_csv(wide.reindex(columns=columns).reset_index(), "findex_accounts.csv")


if __name__ == "__main__":
    main()
