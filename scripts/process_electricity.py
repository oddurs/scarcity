"""Electricity access, rate and headcount → data/processed/electricity_access.csv.

Columns (one row per year):
  wld, ssf, ssf_rural      access to electricity, % of (rural) population
  ssf_without_m            people in sub-Saharan Africa without electricity, millions
  ken                      access to electricity in Kenya, %
"""

from __future__ import annotations

import pandas as pd

from _common import RAW, write_csv


def load(code: str) -> pd.DataFrame:
    return pd.read_csv(RAW / "wdi" / f"{code}.csv")


def series(frame: pd.DataFrame, economy: str, name: str) -> pd.Series:
    return frame.query("economy == @economy").set_index("year")["value"].rename(name)


def main() -> None:
    access = load("EG.ELC.ACCS.ZS")
    rural = load("EG.ELC.ACCS.RU.ZS")
    pop = load("SP.POP.TOTL")

    out = pd.concat([
        series(access, "WLD", "wld"),
        series(access, "SSF", "ssf"),
        series(rural, "SSF", "ssf_rural"),
        series(access, "KEN", "ken"),
        series(pop, "SSF", "ssf_pop"),
    ], axis=1).sort_index()
    out["ssf_without_m"] = out["ssf_pop"] * (1 - out["ssf"] / 100) / 1e6
    # Before 2000 the regional aggregate rests on too few surveys to compare.
    out = out[(out.index >= 2000) & out["ssf"].notna()].drop(columns="ssf_pop")
    out.index.name = "year"
    write_csv(out.reset_index()[["year", "wld", "ssf", "ssf_rural", "ken", "ssf_without_m"]],
              "electricity_access.csv")


if __name__ == "__main__":
    main()
