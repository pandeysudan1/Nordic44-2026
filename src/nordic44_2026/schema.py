from dataclasses import dataclass
from typing import Literal

Action = Literal["KEEP", "MODIFY", "REPLACE", "ADD"]
Confidence = Literal["high", "medium", "low"]

@dataclass(frozen=True)
class ChangeRecord:
    action: Action
    element_type: str
    element_id: str
    parameter: str
    value_2015: str
    value_2026: str
    unit: str
    source: str
    source_date: str
    confidence: Confidence
    mapping_note: str
