# Menu Zitoschinis

Il menu settimanale di casa (Andrea = **AZ**, Alice = **AT**) in versione web app da telefono.

- **Settimana**: colazione, pranzo e cena giorno per giorno, oggi in evidenza. Swipe o frecce per cambiare settimana.
  Un pasto può essere diverso per AZ e AT; un pasto "fuori casa / evento" (deli, ufficio, pizza con amici…) non entra nelle ricette.
  Tocca l'intestazione di un giorno per segnare chi è in ufficio, fuori, in palestra.
- **Settimana nuova** (nel weekend): "Proponi pranzi e cene" riempie lun–ven con piatti di stagione presi dallo storico, evitando quelli mangiati negli ultimi 12 giorni.
  Ogni pasto in modifica mostra proposte di stagione e cerca nell'archivio mentre scrivi.
- **Ricette**: archivio costruito da solo da tutte le settimane, diviso per stagione e pasto, con quante volte e quando l'avete fatta,
  i contorni abituali, note e preferite.
- **Storico**: tutte le settimane, dalla più recente.

## Dove gira

1. **Artifact su claude.ai** (consigliato) – dati condivisi e sincronizzati tra i telefoni.
   Per far modificare il menu anche ad Alice: menu *Condividi* → invitala per email come **Editor**.
2. **Firebase** – indirizzo vostro, accesso con Google, dati condivisi su Firestore.
   Passo passo in [GUIDA-FIREBASE.md](GUIDA-FIREBASE.md).
3. **GitHub Pages / file locale** – `docs/index.html` senza `docs/firebase-config.js`: i dati restano nel browser del telefono (non sincronizzati).

## File

- `app/menu.html` – l'app (sorgente unico).
- `data/storico-2026.txt` – trascrizione dei 32 fogli cartacei (gen–nov 2026), facile da correggere a mano.
- `tools/converti_storico.py` – txt → `data/storico-2026.json`.
- `tools/build_pages.py` – crea `docs/index.html` con lo storico incorporato (e Firebase, se configurato).
- `firebase.json`, `firestore.rules`, `docs/firebase-config.example.js` – configurazione Firebase.
