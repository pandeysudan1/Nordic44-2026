# First numerical screening: Nordic44-2015 vs 2026-v0

Snapshot date: **2026-09-14**.

This is the first numerical layer before a full AC power-flow rebuild. It deliberately separates quantities present in the 2015 reduced model from public 2026 transfer-capability statements.

## 1. NO3-NO4 corridor in the 2015 reduced model

The original RAW model contains two parallel branches between bus 6500 (TRONDHEIM, NO3) and bus 6700 (ROSSAGA, NO4):

| circuit | R | X | B | Rate A | Rate B | Rate C |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.17 | 1.80 | 0.10 | 800 MVA | 900 MVA | 950 MVA |
| 2 | 0.10 | 1.30 | 0.12 | 1000 MVA | 1200 MVA | 1300 MVA |

Simple thermal proxies:

\[
S_{A,parallel}=800+1000=1800\;\text{MVA}
\]

For a worst single-circuit outage, the remaining Rate-A proxy is

\[
S_{A,N-1}^{proxy}=\min(1000,800)=800\;\text{MVA}.
\]

**Important:** these are branch-rating screens, not secure area-transfer limits. Voltage, reactive power, stability and flows on the rest of Nordic44 can produce a lower transfer limit.

## 2. What changes in 2026?

The physical Nedre Rossaga-Namsos upgrade and other north-central reinforcements are verified structural candidates, but no public source used here gives a parameter that can safely replace the 6500-6700 reduced-model R/X/rating values directly. Therefore v0 does **not** invent a new MVA rating.

The 2026-v0 model keeps the original NO3-NO4 electrical branch parameters until a reduction/calibration step is performed against a 2026 network representation.

This is intentional: a real 420 kV upgrade does not imply that the synthetic reduced branch should simply be changed from 300 kV to 420 kV or assigned the physical conductor rating.

## 3. Aurora Line screen

The 2025 Aurora Line is represented initially as an FI-SE **interface** update. Fingrid reports an increase of about 700 MW in Finland-Sweden transfer capability.

Thus the first update is

\[
\Delta C_{FI-SE}^{2026}=+700\;\text{MW}.
\]

This is not converted to MVA and is not assigned to a fabricated 7000-3115 branch. The historical Nordic44/Nord Pool workflow models FI-SE exchange through an exchange injection, so an interface-capability overlay is the least-assumptive first implementation.

## 4. Dynamic subset sanity check

Representative GENSAL inertia constants parsed from the historical DYR file are:

| bus | area | representative H |
|---|---|---:|
| 3115 PORJUS | SE1 | 4.741 s |
| 6500 TRONDHEIM | NO3 | 3.558 s |
| 6700 ROSSAGA | NO4 | 3.592 s |
| 7100 OULU | FI | 3.200 s |

These are **machine-model values**, not 2026 regional equivalent inertia. The 2026 operating overlay must be built from which synchronous units are actually online in the selected hour.

## 5. Decision from v0

We can already freeze three rules for the project:

1. **Keep physical-project evidence separate from reduced-model parameters.**
2. **Use interface capability for Aurora before changing AC topology.**
3. **Calibrate NO3-NO4 equivalent impedance/rating instead of copying a physical line parameter into Nordic44.**

The next numerical milestone is a complete RAW parser and a solvable 2015 AC/DC power-flow case. Once that reproduces the historical case, a 2026 overlay can be applied one change at a time and validated by voltage, branch loading and inter-area transfer metrics.
