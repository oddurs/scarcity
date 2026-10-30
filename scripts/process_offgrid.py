"""People using off-grid solar in sub-Saharan Africa → data/processed/offgrid_solar.csv.

Source: IRENA Off-grid Renewable Energy Statistics 2025 (data/manual/
irena_offgrid_people.csv), one edition only: editions revise each other
heavily and must never be mixed.

IRENA reports an "Africa" row. Sub-Saharan Africa (World Bank definition) is
that row minus the North African entries, which appear only in the >50 W
solar-home-system table (Egypt, Morocco, Tunisia).

Columns (millions of people): lights (<11 W, generally below Tier 1 access),
shs (solar home systems, 11 W and up) and total.
"""

from __future__ import annotations

import pandas as pd

from _common import MANUAL, write_csv

NORTH_AFRICA = ["Egypt", "Morocco", "Tunisia", "Algeria", "Libya"]


def main() -> None:
    raw = pd.read_csv(MANUAL / "irena_offgrid_people.csv")
    africa = raw[raw["entity"] == "Africa"].pivot(index="year", columns="series", values="value")
    north = (raw[raw["entity"].isin(NORTH_AFRICA)]
             .pivot_table(index="year", columns="series", values="value", aggfunc="sum")
             .reindex(index=africa.index, columns=africa.columns).fillna(0))
    ssa = (africa - north) / 1000  # thousands → millions

    out = pd.DataFrame({
        "lights": ssa["solar_lights_lt11w"],
        "shs": ssa["shs_11_50w"] + ssa["shs_gt50w"],
    })
    out["total"] = out["lights"] + out["shs"]
    out.index.name = "year"
    write_csv(out.reset_index(), "offgrid_solar.csv")


if __name__ == "__main__":
    main()
