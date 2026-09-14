# Nordic44-2015 DC baseline validation

Source case: pinned `ALSETLab/Nordic44-Nordpool` commit `49d467a017afb8f70a6ed9f60ac1cb278c35f282`, file `nordic44/models/N44_BC.raw`.

This baseline is a numerical sanity check before building the 2026 operating snapshot. It is not a replacement for the original AC power flow.

## CI-validated model size

| Item | Count |
|---|---:|
| buses | 44 |
| loads | 48 |
| generators | 80 |
| AC branches | 67 |
| two-winding transformers | 12 |

The slack bus is **3300 OSKARSHAMN**. The specified non-slack active-power mismatch is 20.002 MW, which the slack balances.

## DC-versus-historical angle check

The DC model solves

\[
B'\theta = P/S_{base}, \qquad S_{base}=1000\;\text{MVA}.
\]

Branches and two-winding transformers use their historical series reactances. Voltage magnitudes, resistance, reactive power, shunts and tap effects are deliberately omitted.

After shifting the historical RAW angles to the same slack reference, the comparison is:

| metric | result |
|---|---:|
| mean absolute angle error | **0.3709 deg** |
| maximum absolute angle error | **1.7456 deg** |

For a deliberately simple DC reconstruction, this is a useful connectivity and parsing check. It does not imply AC equivalence.

## NO3-NO4 corridor

The two historical 6500 TRONDHEIM - 6700 ROSSAGA circuits give:

| circuit | defined direction | DC flow | Rate A | loading proxy |
|---|---|---:|---:|---:|
| 1 | NO3 -> NO4 | -131.17 MW | 800 MVA | 16.4% |
| 2 | NO3 -> NO4 | -181.61 MW | 1000 MVA | 18.2% |

Therefore the net flow is

\[
P_{NO3\rightarrow NO4}=-312.78\;\text{MW},
\]

or approximately **312.78 MW from NO4 toward NO3** in this 2015 operating case.

The 2026-v0 overlay does **not** change the 6500-6700 R/X/rating values yet. Nedre Rossaga-Namsos and other north-central reinforcements are real physical changes, but their reduced equivalent must be calibrated rather than copied directly into Nordic44.

## Sweden-Finland AC ties

The historical reduced model gives:

| branch | defined direction | DC flow | Rate A | loading proxy |
|---|---|---:|---:|---:|
| 3115 PORJUS - 7100 OULU | SE1 -> FI | -324.75 MW | 1300 MVA | 25.0% |
| 3249 GRUNDFORS - 7100 OULU | SE2 -> FI | +464.74 MW | 1900 MVA | 24.5% |

The simple net of these two AC ties is approximately

\[
P_{SE\rightarrow FI}=139.99\;\text{MW}.
\]

This is a solved-flow result for the **2015 dispatch**, not a 2026 flow forecast.

## First 2026-v0 comparison

Aurora Line is represented initially by the documented transfer-capability change

\[
\Delta C_{FI-SE}=+700\;\text{MW}.
\]

We do not add 700 MW to the solved 2015 flow and we do not convert this to a 700 MVA synthetic branch. Until a 2026 generation/load/exchange snapshot is selected, the honest comparison is:

| quantity | 2015 solved baseline | 2026-v0 structural overlay |
|---|---:|---:|
| FI-SE solved operating flow | 139.99 MW SE -> FI | unchanged in v0; new dispatch not yet supplied |
| FI-SE transfer capability | historical reference | **+700 MW relative capability** |
| NO3-NO4 equivalent R/X/rating | historical Nordic44 | unchanged until calibrated |
| 2026 generation/load dispatch | not applicable | pending operating snapshot |

## Why this matters

The project now has a numerical gate. A future 2026 case must be produced by an explicit parameter overlay, not by silently changing a picture of the network. The next stage is to select a reproducible 2026 operating hour, update area injections and synchronous-machine availability, and then solve the same network metrics for both cases.

The CI workflow downloads the pinned RAW source, runs unit tests, solves this baseline, and uploads bus-angle and branch-flow CSV artifacts on every push.
