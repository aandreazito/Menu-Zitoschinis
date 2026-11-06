"""Converte data/storico-2026.txt in data/storico-2026.json (formato dell'app)."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = root / "data" / "storico-2026.txt"
out = root / "data" / "storico-2026.json"

def meal(s):
    s = s.strip()
    if s in ("", "-"):
        return None
    def one(t):
        t = t.strip()
        if t in ("", "-"):
            return None
        if t.startswith("!"):
            return {"t": t[1:].strip(), "x": 1}
        return {"t": t}
    m = re.match(r"^(AZ|AT):\s*(.*?)\s*/\s*(AZ|AT):\s*(.*)$", s)
    if m:
        d = {m.group(1).lower(): one(m.group(2)), m.group(3).lower(): one(m.group(4))}
        return {"split": 1, "az": d.get("az"), "at": d.get("at")}
    return one(s)

weeks = []
cur = None
for line in src.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    if line.startswith("=="):
        parts = [p.strip() for p in line[2:].split("|")]
        cur = {"id": parts[0], "note": parts[1] if len(parts) > 1 else "", "days": []}
        weeks.append(cur)
        continue
    body, _, tagpart = line.partition("  #")
    c, p, d = [x for x in body.split("|")]
    day = {"c": meal(c), "p": meal(p), "d": meal(d)}
    tags = {}
    for t in re.findall(r"(AZ|AT):\s*([\w\- ]+)", tagpart):
        tags[t[0].lower()] = t[1].strip()
    if tags:
        day["tags"] = tags
    cur["days"].append(day)

for w in weeks:
    assert len(w["days"]) == 7, (w["id"], len(w["days"]))
out.write_text(json.dumps({"weeks": weeks}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(len(weeks), "settimane ->", out, out.stat().st_size, "bytes")
