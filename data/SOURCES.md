# Sources

Every dataset and every factual claim the paper relies on, with where it comes
from and how far it has been checked. Bibliography keys match
`paper/references.bib`. Last full check: **2026-10-30**.

**Status key**

| Status | Meaning |
|---|---|
| VERIFIED | Checked against the publisher, an index (Crossref, PubMed) or the primary document itself |
| PARTIAL | Core facts confirmed; a detail is secondary-only or missing (noted) |
| UNVERIFIED | Not confirmed. Must not appear in the paper except as `\placeholder{}` |

---

## 1. Datasets (fetched by script)

| Dataset | What we use | Access | Licence | Status |
|---|---|---|---|---|
| **World Bank WDI** | `EG.ELC.ACCS.ZS` access to electricity (% pop.); `EG.ELC.ACCS.RU.ZS` rural; `SP.POP.TOTL`, `SP.RUR.TOTL` population; `NY.GDP.PCAP.PP.KD` GDP pc PPP (**constant 2021** intl $); `IT.CEL.SETS.P2` mobile and `IT.MLT.MAIN.P2` fixed telephone subscriptions per 100 | `wbgapi` (db 2) → api.worldbank.org/v2. WDI last updated 2026-10-08 | CC BY 4.0 | VERIFIED: live API tested 2026-10-30 |
| **Global Findex** (2025 edition, survey year 2024) | `account.t.d` any account; `fiaccount.t.d` financial-institution account; `mobileaccount.t.d` mobile money account (all % age 15+) | `wbgapi` **db 28** | CC BY 4.0 | VERIFIED: live API tested |
| **CHAT** (Comin & Hobijn) | Technology adoption dates and lags, for the leapfrogging test | data.nber.org/data-appendix/w15319/ (`FinalCHAT_72909.csv`, `chat.dta`, `README.TXT`); dataset DOI 10.60592/csem-gt84 | NBER public data; cite `comin2009chat` | VERIFIED: still hosted |

**Gotchas found while checking**

- Region codes differ by database. In WDI, `SSF` = Sub-Saharan Africa (all
  incomes). In Findex (db 28) the aggregate is `SSA` (excluding high income),
  and `SSF` returns nothing.
- WDI `FX.OWN.TOTL.ZS` for SSF (55.1 in 2021) does **not** match Findex
  `account.t.d` for SSA (49.3 in 2021). The paper uses **Findex only** for
  account ownership, so the definitions stay consistent.
- WDI has no mobile-money indicator. Mobile money comes from Findex.
- Kenya 2011 "account" covers financial-institution accounts only, because
  mobile money was not asked in 2011.
- **Headcount without electricity.** Our SSA figure (WDI population × share
  without access) is about 580 million for 2024. Tracking SDG7 2026 reports
  563 million. The gap is aggregation: the custodian agencies use their own
  population weights and regional definition. The paper uses the WDI-derived
  series for the time trend (it is internally consistent across years) and
  quotes the SDG7 figure, attributed, when stating the official number.
- WDI electricity aggregates for SSA before 2000 rest on few surveys and jump
  around (28.5% in 1996 vs 25.7% in 2000), so the series starts in 2000.
- Kenya's electricity series is noisy year to year (e.g. 30% in 2008, then 23%
  and 19% in 2009–10) because it is pieced together from different surveys.
  Use it for levels, not year-on-year changes.
- Subscriptions are not people: many adults hold several SIMs, so mobile
  subscriptions per 100 overstate how many people have a phone.

**Off-grid solar series: why IRENA, and the caveats**

- Only IRENA 2025 gives an annual, single-method, regional series. Tracking
  SDG7 changed its headline off-grid metric in almost every edition from 2018
  to 2026 and mislabels years across editions; GOGLA changed units ("products"
  to "kits", 2022), cadence (half-yearly to annual, 2025) and has documented
  breaks in "people served".
- **Never mix IRENA editions.** The 2024 highlights put solar-light users in
  2023 at ~100m worldwide; the 2025 edition says 40.3m.
- IRENA rests mostly on GOGLA-affiliate sales (~29% of the market), so it
  undercounts. The whole-market estimate in Tracking SDG7 2026 is 449m people
  worldwide on Tier 1–2 off-grid solar in 2024, against IRENA's ~84m.
- Lights under 11 W generally fall short of Tier 1 access; the figure shows
  them separately from solar home systems.
- ~35% of off-grid solar users are grid-connected and use it as backup
  (60 Decibels 2025, cited in Tracking SDG7 2026), so uptake ≠ first access.
- Research notes with ~150 candidate data points, including the rejected
  series, are kept outside the repo; only the chosen series is entered.

## 1b. Processed outputs

| File | Built by | Feeds |
|---|---|---|
| `electricity_access.csv` | `process_electricity.py` | Figure 2 (§3.1); `\ssp*Elec*`, `\wldElecAccess`, `\kenElecAccess` |
| `findex_accounts.csv` | `process_findex.py` | Figure 3 (§3.2); `\ken*Account*`, `\ssa*`, `\wldMobileMoney` |
| `leapfrog_summary.csv`, `leapfrog_series.csv` | `process_leapfrog.py` | Leapfrogging (§2, §4 causation); `\*FixedPeak`, `\*MobileSubs` |
| `offgrid_solar.csv` | `process_offgrid.py` (from `data/manual/irena_offgrid_people.csv`) | Figure 2 bands; `\ssp*Solar*`, `\sspShs*`, `\sspLightUsers` |
| `report_headlines.csv` | `process_headlines.py` (from `data/manual/report_headlines.csv`) | `\sdg*`, `\gogla*`, `\gsma*` |

## 2. Reports (figures entered by hand into `data/manual/`)

Each value goes in `data/manual/*.csv` with `value, unit, year, source_key, page`.

| Report | Headline figures | URL | Licence | Status |
|---|---|---|---|---|
| **Tracking SDG7 2026** (data year 2024), via UNSD SDG Extended Report 2026, Goal 7 (`unsd2026sdg7`) | 92% global access; 655m without electricity; 563m (86%) in SSA; ~449m served by tier 1–2 off-grid solar; ~48m by mini-grids | unstats.un.org/sdgs/report/2026/extended-report/Extended-Report-2026_Goal-7.pdf | UN terms; quote with citation | VERIFIED. The ESMAP portal blocks automated fetch, so the UNSD copy is used |
| **GOGLA** Global Off-Grid Solar Market Report, June 2026, covering 2025 (`gogla2026`) | 10.2m kits sold in 2025 (+10%); affiliates serve "over 148 million people", 11m added in 2025 | gogla.org/wp-content/uploads/2026/06/GOGLA_Global-Off-Grid-Solar-Market-Report_2026_DEF3.pdf | "Public Report"; **no open licence found**. Quote aggregates, don't redistribute | VERIFIED. Covers affiliates only, so it **undercounts** the market |
| **GSMA** State of the Industry Report on Mobile Money 2026, data year 2025 (`gsma2026sotir`) | Global: 2.3bn registered, 593m 30-day active, $2.1tn value (PDF pp. 3, 6). SSA: 1.2bn registered (~52%), 341m active, $1.4tn (~67% of value): **SSA figures not found in the text layer; page still TODO** | gsma.com/sotir/…/The-State-of-the-Industry-Report-2026_English.pdf | GSMA terms; quote with citation | VERIFIED |
| **Orkustofnun**, District heating (`orkustofnun_heating`) | ~90% of domestic heating energy geothermal (2020); district heating reaches 95% of the population; oil crises of 1973 and 1979 changed energy policy | orkustofnun.is/en/natural_resources/district_heating | Government web page | VERIFIED |
| **IRENA** Off-grid Renewable Energy Statistics 2025 (`irena2025offgrid`) | People using solar lights (<11 W), SHS 11–50 W and SHS >50 W, by country and region, 2015–2024 (PDF pp. 57, 59, 61) | irena.org/-/media/Files/IRENA/Agency/Publication/2025/Dec/IRENA_DAT_Off-grid_Renewable_Energy_Statistics_2025.pdf | Free reuse with acknowledgement of IRENA | VERIFIED: every value re-read from the PDF. **Chosen series for Fig. 2** (one edition, one method, regional). SSA = Africa row minus Egypt, Morocco, Tunisia (≤0.45m, >50 W table only) |

## 3. Claims in the outline, checked

These are the claims the outline leans on. Several were wrong in the form we
first had them.

| Claim | Finding | Status | Use in paper |
|---|---|---|---|
| Moser invented the bottle light in Brazil around 2002 | BBC: "In 2002 … during one of the country's frequent electricity blackouts", in Uberaba | VERIFIED (`zobel2013bbc`) | The BBC says "southern Brazil", but Uberaba is in Minas Gerais (south-east). Say "Uberaba, Brazil" |
| Bleach in the bottle | "two capfuls of bleach to protect the water so it doesn't turn green" | VERIFIED | As quoted |
| "Equivalent to a 40–60 W bulb" | Moser's own words: "more or less 40 to 60 watts" | PARTIAL | Attribute it to Moser. It is not an independent measurement |
| Liter of Light scale | BBC (Aug 2013): MyShelter began June 2011; 140,000 Philippine homes; ~15 countries. "One million" is a projection | PARTIAL | Use "140,000 homes (as reported by MyShelter to the BBC, 2013)". Other counts (200k, 350k, 360k) are secondary and inconsistent |
| BBC headline "…proud to be poorly paid" | The actual headline is **"Bottle light inventor proud to be poor"** | Corrected | Use the real title |
| M-Pesa lifted 2% of Kenyan households out of poverty | Abstract: "194,000 households, or 2% of Kenyan households" | VERIFIED (`suri2016`) | Always pair with the `bateman2019` critique |
| Suri & Jack replied to Bateman et al. | **No published reply found** | UNVERIFIED | Do not cite a reply |
| DFID seeded M-Pesa with ~£1m | Hughes & Lonie: "nearly £1 million, which was matched by Vodafone". The exact £910,000 (and £990,000 from Vodafone) comes from a DFID blog | VERIFIED (`hughes2007`, `phillips2013dfid`) | Use both |
| Constraint research finds an inverted U | Acar et al. **propose** an inverted U as an integrative framework built on mixed evidence. It is not a meta-analytic estimate | VERIFIED (`acar2019`) | Say "proposes", and label the figure conceptual |
| Jaipur Foot cost (primary) | Sethi et al. 1978: "cost only about [£]2.00 (sterling)" (currency sign garbled online, almost certainly £) | PARTIAL (`sethi1978`) | Usable, with the year and currency stated |
| "Sethi et al. 1971, JBJS" | **No such paper found.** The main paper is POI 1978; the JBJS item is a 2008 review | Corrected | Use `sethi1978` and `arya2008` |
| Jaipur Foot ~$45 today vs ~$8,000–12,000 in the US | **Secondary only** (Science Museum blog; PBS; an unretrieved 2003 Michigan case) | UNVERIFIED | `\placeholder` unless a primary source turns up |
| Aravind: ~US$120 per cataract operation, $195 per QALY | Le et al. 2016 abstract | VERIFIED (`le2016aravind`) | Use |
| Aravind "£100 vs NHS £1,000" | **No source makes this comparison** | UNVERIFIED | Needs a specific NHS Payment Scheme year and HRG code; until then, `\placeholder` |
| Aravind complications "half the NHS rate" | Only a Bridgespan case study; full Le et al. text paywalled | UNVERIFIED | `\placeholder` |
| Embrace warmer $25 vs $20,000 incubator | Stanford GSB 2011: "$25 to $100" vs "up to $20,000". No clinical trials published (Nimbalkar et al. 2014) | PARTIAL (`routson2011embrace`, `nimbalkar2014`) | Say "$25–$100 (2011 estimate)". $25 is the bottom of a range |
| NeoNurture (car-part incubator) failed to reach adoption | Prototype target under $1,000 vs $30,000+ (Sci Am blog, 2008). The failure framing has no primary source here | UNVERIFIED | Possible survivorship-bias example. Needs a source |
| WWII synthetic rubber output figures | ACS wording ("231 tons … 1941 … 70,000 tons a month in 1945") seen only in search extracts; acs.org blocks automated access and no archived copy was found | UNVERIFIED | **Dropped.** The paper uses the verified Baruch committee figure (90% of pre-war natural rubber supply lost) and `herbert1985` |
| Iceland oil share of heating | Orkustofnun table OS-2020-T008-01 (share of heated building volume): geothermal 49.6/74.2/79.9%, oil 46.0/14.2/6.2% in 1970/1980/1985 | VERIFIED (`orkustofnun2020heating`) | Used. The Icelandic Times "53% to 7%" is not used |
| CHAT: average adoption lag ~45 years | Comin & Hobijn 2010, AER abstract | VERIFIED (`comin2010`) | Use |

## 4. Not yet checked

- `comin2004`: NBER asks users of CHAT to cite this paper. Its volume and pages are from memory and still need checking.
- Morton, *Rubber Technology*: not looked at; probably unnecessary.
- `immelt2009`: pages 56–65 come from secondary listings, so the bib entry omits them.
- Pay-as-you-go solar: no source chosen yet. Candidates are GOGLA PAYG data and
  peer-reviewed RCTs of solar lanterns (e.g. Aklin et al.). **To research before §3.1.**
- Hidden-abundance supply chain (semiconductors, lithium, the PV module supply
  chain): candidates are the IEA *Solar PV Global Supply Chains* (2022) and the USGS
  Mineral Commodity Summaries. **To research before §4.**

## 5. Sources added while drafting (all VERIFIED against the primary document)

Every quantity from these is in `data/manual/literature_figures.csv` with its
page. Keys refer to `paper/references.bib`.

| Topic | Keys | What we use |
|---|---|---|
| Solar PV and battery supply chains | `iea2022pv`, `iea2022evbatt`, `irena2024costs` | China's 2021 share of capacity by stage (PDF pp. 58–59); 76% of battery production capacity (PDF p. 36); module costs fell 93%, 2009–2023 (p. 82) |
| Evidence on off-grid solar and the grid | `grimm2017`, `aklin2017`, `barry2020`, `lee2020` | Abstract-level findings only; Barry & Creti's 10% from the author manuscript |
| M-Pesa conditions | `afi2010` | CBK letter of no objection (Feb 2007); 27% phone ownership in 2006 (PDF p. 11) |
| GSMA regional figures | `gsma2026sotir` | SSA 1.2bn registered, $1.4tn value (PDF p. 11, infographic labels) |
| Slack and innovation; psychology of poverty | `nohria1996`, `haushofer2014` | Abstract-level findings |
| Cataract cost and quality | `monitor2014tariff`, `haripriya2019`, `buchan2020nod` | NHS 2014/15 tariff £699 (BZ02Z); Aravind PCR 1.37%; UK consultant benchmark 1.1% |
| Prosthesis cost; Jaipur Foot reach | `hermodsson1998`, `cms2026dmepos`, `bmvss2026` | Median $898 (Sweden, 1997); Medicare L5100 $2,845–$3,794 (2026); 724,503+ limbs |
| Embrace evidence; NeoNurture | `morgaonkar2021`, `gopalakrishnan2022`, `prestero2012ted` | Trial findings (abstracts); Prestero's own account |
| History | `baruch1942rubber`, `ragnars1980`, `orkustofnun2020heating` | 90% of rubber lost; Reykjavík citywide in the 1960s; heating shares |
| Bottle light at night | `npr2011literoflight` | "the bottles don't shine in the night" |

Still partial and therefore **not** used as figures: Vodafone's exact 2007
stake in Safaricom (35–40%); M-Pesa Romania's closure; US Medicare payment for
cataract surgery; UNICEF/UNFPA incubator catalogue prices.
