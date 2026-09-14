from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO


@dataclass(frozen=True)
class Bus:
    bus_id: int
    name: str
    base_kv: float
    bus_type: int
    area: int
    vm_pu: float
    va_deg: float


@dataclass(frozen=True)
class Load:
    bus_id: int
    load_id: str
    status: int
    p_mw: float
    q_mvar: float


@dataclass(frozen=True)
class Generator:
    bus_id: int
    gen_id: str
    p_mw: float
    q_mvar: float
    mbase_mva: float
    status: int


@dataclass(frozen=True)
class Branch:
    from_bus: int
    to_bus: int
    circuit: str
    r_pu: float
    x_pu: float
    b_pu: float
    rate_a_mva: float
    status: int


@dataclass(frozen=True)
class Transformer:
    from_bus: int
    to_bus: int
    circuit: str
    r_pu: float
    x_pu: float
    status: int


@dataclass(frozen=True)
class RawCase:
    base_mva: float
    buses: tuple[Bus, ...]
    loads: tuple[Load, ...]
    generators: tuple[Generator, ...]
    branches: tuple[Branch, ...]
    transformers: tuple[Transformer, ...]


def _csv(line: str) -> list[str]:
    return next(csv.reader(StringIO(line), skipinitialspace=True, quotechar="'"))


def _between(lines: list[str], start_marker: str | None, end_marker: str) -> list[str]:
    start = 0
    if start_marker is not None:
        for i, line in enumerate(lines):
            if start_marker in line:
                start = i + 1
                break
    out: list[str] = []
    for line in lines[start:]:
        if end_marker in line:
            break
        if line.strip() and not line.lstrip().startswith("0 /"):
            out.append(line)
    return out


def parse_raw(text: str) -> RawCase:
    lines = text.splitlines()
    header = _csv(lines[0])
    base_mva = float(header[1])

    bus_lines = []
    for line in lines[3:]:
        if "END OF BUS DATA" in line:
            break
        if line.strip():
            bus_lines.append(line)

    buses = []
    for line in bus_lines:
        f = _csv(line)
        buses.append(Bus(int(f[0]), f[1].strip(), float(f[2]), int(f[3]), int(f[4]), float(f[7]), float(f[8])))

    loads = []
    for line in _between(lines, "BEGIN LOAD DATA", "END OF LOAD DATA"):
        f = _csv(line)
        loads.append(Load(int(f[0]), f[1].strip(), int(f[2]), float(f[5]), float(f[6])))

    generators = []
    for line in _between(lines, "BEGIN GENERATOR DATA", "END OF GENERATOR DATA"):
        f = _csv(line)
        generators.append(Generator(int(f[0]), f[1].strip(), float(f[2]), float(f[3]), float(f[8]), int(f[14])))

    branches = []
    for line in _between(lines, "BEGIN BRANCH DATA", "END OF BRANCH DATA"):
        f = _csv(line)
        branches.append(Branch(int(f[0]), int(f[1]), f[2].strip(), float(f[3]), float(f[4]), float(f[5]), float(f[6]), int(f[13])))

    transformers: list[Transformer] = []
    tlines = _between(lines, "BEGIN TRANSFORMER DATA", "END OF TRANSFORMER DATA")
    i = 0
    while i < len(tlines):
        f1 = _csv(tlines[i])
        if len(f1) < 12:
            i += 1
            continue
        k = int(f1[2])
        if k != 0:
            raise NotImplementedError("Only two-winding transformers are supported in the Nordic44 baseline parser")
        f2 = _csv(tlines[i + 1])
        transformers.append(
            Transformer(
                from_bus=int(f1[0]),
                to_bus=int(f1[1]),
                circuit=f1[3].strip(),
                r_pu=float(f2[0]),
                x_pu=float(f2[1]),
                status=int(f1[11]),
            )
        )
        i += 4

    return RawCase(
        base_mva=base_mva,
        buses=tuple(buses),
        loads=tuple(loads),
        generators=tuple(generators),
        branches=tuple(branches),
        transformers=tuple(transformers),
    )
