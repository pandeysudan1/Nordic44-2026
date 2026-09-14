# Nordic44-2026

A reproducible research benchmark for updating the Nordic44 power-system model from a 2015 operating reference toward a documented 2026 snapshot.

## Research idea

Keep the original Nordic44 case immutable and represent 2026 as transparent overlays:

- operating-point updates: load, generation, voltage, inter-area exchange;
- dynamic updates: inertia, governor/FCR participation, turbine and converter assumptions;
- structural updates: commissioned lines, transformers, substations, HVDC links and ratings;
- provenance: every modified parameter carries a source, date, confidence level and mapping rationale.

The project is designed for static power flow, disturbance sharing, COI frequency, tie-line response, RoCoF and FCR-oriented studies.

## Model layers

```text
Nordic44-2015 immutable base
          |
          +--> 2026 operating overlay
          |      P/Q load, P/Q generation, online units, inertia,
          |      reserves, HVDC schedules
          |
          +--> 2026 structural overlay
                 new/retired corridors, transformer/substation changes,
                 ratings and equivalent-bus mapping
```

## Repository structure

```text
app/                    FastAPI dashboard/API service
src/nordic44_2026/      model-building and validation code
data/base_2015/         untouched Nordic44 reference data
data/overlays_2026/     2026 parameter/topology overlays
data/sources/            source register and provenance
docs/                   methodology and mapping rules
notebooks/               reproducible studies
tests/                   validation tests
.github/workflows/       CI
```

## Core 2026 update table

Each change is represented as a row in `data/overlays_2026/change_register.csv` with one of four actions:

`KEEP | MODIFY | REPLACE | ADD`

Important fields are `element_type`, `element_id`, `parameter`, `value_2015`, `value_2026`, `unit`, `source`, `source_date`, `confidence`, and `mapping_note`.

## First research questions

1. For the same disturbance, how does 2026 system inertia change regional RoCoF and frequency nadir?
2. How much disturbance is shared across NO/SE/FI/DK equivalent areas through AC and HVDC interfaces?
3. Which 2015-to-2026 transmission upgrades materially change inter-area power transfer?
4. How sensitive are FCR conclusions to uncertain generator online status and hydro governor parameters?

## Local run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `/` for the project landing page, `/health` for Railway health checks and `/api/changes` for the change register.

## Railway

The repository contains a `Dockerfile` and `railway.toml`. Railway can deploy directly from GitHub once the repository is connected.

## Data policy

Do not overwrite the original 2015 benchmark. Public 2026 data should be cited directly; inferred/equivalent parameters must be marked as estimates. This makes the model auditable instead of presenting an approximate reduced model as an exact TSO network model.
