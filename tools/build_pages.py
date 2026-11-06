"""Crea docs/index.html (versione Firebase / GitHub Pages / offline) da app/menu.html.
Aggiunge lo scheletro HTML e incorpora lo storico come dati iniziali.
Se esiste docs/firebase-config.js, carica anche Firebase: i dati vanno su Firestore, con accesso Google."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
app = (root / "app" / "menu.html").read_text(encoding="utf-8")
seed = (root / "data" / "storico-2026.json").read_text(encoding="utf-8")
head = ('<!doctype html><html lang="it"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="apple-mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-title" content="Menu">'
        '<link rel="apple-touch-icon" href="icon-180.png">'
        '<link rel="icon" type="image/png" sizes="32x32" href="icon-32.png">'
        '<link rel="manifest" href="manifest.webmanifest">'
        '<meta name="theme-color" content="#3f6680">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
FIREBASE_VERSION = "10.12.2"
firebase = ""
if (root / "docs" / "firebase-config.js").exists():
    base = f"https://www.gstatic.com/firebasejs/{FIREBASE_VERSION}"
    firebase = "".join(f'<script src="{base}/firebase-{m}-compat.js"></script>' for m in ("app", "auth", "firestore"))
    firebase += '<script src="firebase-config.js"></script>'
    print("Firebase: attivo (docs/firebase-config.js trovato)")
else:
    print("Firebase: non configurato, i dati restano nel browser")
out = head + firebase + f"<script>window.MENU_SEED={seed};</script>" + app + "</body></html>"
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(out, encoding="utf-8")
print("docs/index.html", len(out), "bytes")
