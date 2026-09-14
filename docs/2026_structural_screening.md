# Nordic44-2026 structural screening

This note records how candidate 2015->2026 network changes are screened before they are allowed to modify the benchmark model.

## Principle

Nordic44 is an equivalent synthetic transmission model, not a one-to-one substation model. A real 2026 project is therefore not inserted automatically. It must first be mapped to an existing Nordic44 electrical area, corridor or exchange representation.

A candidate is promoted to `change_register.csv` only when all of the following are known:

1. the asset was commissioned before the selected 2026 snapshot date;
2. an official source confirms the relevant electrical change;
3. the Nordic44 equivalent buses/area/interface are identified;
4. the modelling action is defensible: `MODIFY`, `ADD`, `REPLACE` or `KEEP`;
5. the changed parameter can be quantified or a transparent equivalent can be derived;
6. a power-flow sanity check does not destroy the benchmark operating logic.

## First verified structural candidates

| Candidate | Verified fact | 2026 treatment |
|---|---|---|
| Sogndal-Orskog | 420 kV connection operational in Dec 2016 | map before applying |
| Ofoten-Balsfjord | new 420 kV connection operational Sep 2017 | map before applying |
| Nedre Rossaga-Namsos | upgraded to 420 kV Oct 2017 | map existing corridor and quantify new equivalent |
| Aurland-Sogndal | commissioned in autumn 2025 | map and quantify transfer effect |
| Aurora Line FI-SE | 400 kV cross-border link commissioned Nov 2025; Fingrid reports about 700 MW additional FI-SE transfer capability | strong candidate for new/reparameterized equivalent interface |
| NordSyd | multi-decade reinforcement programme | do not apply programme wholesale; include only assets commissioned by snapshot date |
| Skaidi-Hammerfest | under construction in 2026 | exclude from base 2026 snapshot; retain for future scenario |

## Mapping strategy

The historical Nordic44-Nordpool workflow already maps market areas and external exchanges to representative buses. Examples include NO1-NO5, SE1-SE4 and FI, with exchange representations on specific buses. We will reuse that area logic rather than pretending every real substation has a unique Nordic44 node.

For each candidate project we will determine:

`real asset -> bidding/control area -> Nordic44 area -> representative buses/interface -> equivalent parameter change`

For an interface reinforcement the first test is whether the existing equivalent branch can be reparameterized. A new equivalent branch is added only when the new physical corridor creates a materially different electrical path.

## 2026 snapshot definition

The project must use a dated snapshot rather than the vague label "2026". The initial target is **2026-09-14**. Assets still in construction or planning on that date are not part of the base case. They may appear in separate future-scenario overlays.

## Next quantitative step

The next work package is to freeze the original Nordic44 bus/area/interface tables, then produce `mapping_2015_to_2026.csv` with one row per relevant equivalent element. After that, operating data (generation, load, HVDC exchange, online synchronous capacity and inertia assumptions) can be layered on top of the structural case.
