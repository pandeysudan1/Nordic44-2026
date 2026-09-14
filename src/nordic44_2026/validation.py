REQUIRED_COLUMNS = {
    "action", "element_type", "element_id", "parameter",
    "value_2015", "value_2026", "unit", "source",
    "source_date", "confidence", "mapping_note"
}

ALLOWED_ACTIONS = {"KEEP", "MODIFY", "REPLACE", "ADD"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}

def validate_change_rows(rows):
    errors = []
    for i, row in enumerate(rows, start=2):
        missing = REQUIRED_COLUMNS - set(row)
        if missing:
            errors.append(f"row {i}: missing columns {sorted(missing)}")
        if row.get("action") not in ALLOWED_ACTIONS:
            errors.append(f"row {i}: invalid action {row.get('action')}")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"row {i}: invalid confidence {row.get('confidence')}")
        if row.get("action") != "KEEP" and not row.get("source"):
            errors.append(f"row {i}: changed parameter requires a source")
    return errors
