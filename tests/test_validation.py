import csv
from pathlib import Path
from nordic44_2026.validation import validate_change_rows

def test_change_register_schema():
    p = Path(__file__).resolve().parents[1] / "data" / "overlays_2026" / "change_register.csv"
    with p.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert validate_change_rows(rows) == []
