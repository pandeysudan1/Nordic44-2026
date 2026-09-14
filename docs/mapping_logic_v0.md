# Nordic44-2026 equivalent mapping logic v0

Snapshot date: 2026-09-14.

## Principle

Do not copy the real transmission grid into the reduced Nordic44 model one substation at a time. First preserve the historical Nordic44 area structure, then translate each commissioned physical change into an equivalent change only when the electrical effect is material and the mapping is defensible.

Physical asset -> Nordic bidding area/interface -> Nordic44 representative area/interface -> equivalent parameter -> validation.

## Historical market-to-Nordic44 anchors

The historical Nord Pool mapping used representative buses for the bidding areas: NO1 5500, NO2 5600, NO3 6500, NO4 6700, NO5 5300, SE1 3115, SE2 3249, SE3 3500, SE4 8500 and FI 7000. The workflow also represents selected external exchanges as loads, including FI-SE3 at bus 7000 and NO-DK/NO-NL in NO2.

These are anchors, not proof that every 2026 physical line terminates at those exact reduced buses.

## First implementation decision

Aurora Line is the best first structural update because it is a new FI-SE transfer path commissioned before the snapshot and its transfer effect is publicly quantified. In v0 we therefore represent Aurora as an increase in the FI-SE1 equivalent interface capability rather than creating a new physical substation bus.

This choice preserves the 44-bus abstraction and allows a clean sensitivity study. A later structural version may add or split equivalent branches if power-flow validation shows that a simple interface-capacity update is insufficient.

## Validation gate

A candidate is promoted to the executable change register only when:

1. commissioning status is verified before the snapshot date;
2. Nordic44 area or branch mapping is documented;
3. the changed parameter is quantified or explicitly estimated;
4. the 2015 base and 2026 overlay both solve;
5. voltage, branch loading and area interchange remain plausible;
6. the expected directional effect is reproduced.

## Next numerical experiment

Run a FI-SE transfer sweep for the 2015 and 2026 cases. Keep the original topology first and increase the FI-SE1 transfer ceiling by 700 MW for the Aurora candidate. Compare convergence margin, interface loading, bus-voltage extrema and sensitivity of active-power redistribution. This is a screening experiment, not yet a claim that a single 700 MW branch parameter exactly represents Aurora Line.
