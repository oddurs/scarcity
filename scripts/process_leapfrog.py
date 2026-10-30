"""Mobile vs fixed telephone subscriptions → two processed CSVs.

leapfrog_series.csv   one row per year: mobile (mob) and fixed (fix)
                      subscriptions per 100 people, for SSF, KEN and USA
leapfrog_summary.csv  one row per economy: peak fixed-line rate (and its
                      year), latest mobile rate, first year mobile exceeded fixed
"""

from __future__ import annotations

import pandas as pd

from _common import RAW, write_csv

SERIES_ECONOMIES = {"SSF": "ssf", "KEN": "ken", "USA": "usa"}


def main() -> None:
    mob = pd.read_csv(RAW / "wdi" / "IT.CEL.SETS.P2.csv")
    fix = pd.read_csv(RAW / "wdi" / "IT.MLT.MAIN.P2.csv")
    both = mob.merge(fix, on=["economy", "year"], suffixes=("_mob", "_fix"))

    rows = []
    for economy, g in both.groupby("economy"):
        g = g.sort_values("year")
        over = g[g["value_mob"] > g["value_fix"]]
        peak = g.loc[g["value_fix"].idxmax()]
        last = g.iloc[-1]
        rows.append({
            "economy": economy,
            "fixed_peak": peak["value_fix"], "fixed_peak_year": int(peak["year"]),
            "mobile_latest": last["value_mob"], "latest_year": int(last["year"]),
            "mobile_overtook_year": int(over["year"].iloc[0]) if len(over) else None,
        })
    write_csv(pd.DataFrame(rows), "leapfrog_summary.csv")

    wide = {}
    for economy, short in SERIES_ECONOMIES.items():
        g = both[both["economy"] == economy].set_index("year")
        wide[f"{short}_mob"] = g["value_mob"]
        wide[f"{short}_fix"] = g["value_fix"]
    series = pd.DataFrame(wide).sort_index()
    series.index.name = "year"
    write_csv(series.reset_index(), "leapfrog_series.csv")


if __name__ == "__main__":
    main()
