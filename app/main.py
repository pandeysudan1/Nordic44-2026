from pathlib import Path
import csv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Nordic44-2026", version="0.1.0")
ROOT = Path(__file__).resolve().parents[1]
CHANGE_FILE = ROOT / "data" / "overlays_2026" / "change_register.csv"

@app.get("/health")
def health():
    return {"status": "ok", "project": "Nordic44-2026"}

@app.get("/api/changes")
def changes():
    if not CHANGE_FILE.exists():
        return []
    with CHANGE_FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

@app.get("/", response_class=HTMLResponse)
def home():
    rows = changes()
    counts = {}
    for row in rows:
        action = row.get("action", "UNKNOWN")
        counts[action] = counts.get(action, 0) + 1
    cards = "".join(f"<li><b>{k}</b>: {v}</li>" for k, v in sorted(counts.items())) or "<li>No overlay entries yet.</li>"
    return f"""
    <html><head><title>Nordic44-2026</title>
    <style>body{{font-family:system-ui;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.5}}code{{background:#eee;padding:2px 5px}}</style>
    </head><body>
    <h1>Nordic44-2026</h1>
    <p>Auditable 2015 → 2026 Nordic44 benchmark overlays for power-flow and frequency-dynamic studies.</p>
    <h2>Change register</h2><ul>{cards}</ul>
    <p>Machine-readable endpoint: <code>/api/changes</code></p>
    </body></html>
    """
