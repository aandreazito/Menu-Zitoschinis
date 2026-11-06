# Pubblicare il menu su Firebase

Alla fine avrete l'app su un indirizzo vostro (per esempio `https://menu-zitoschinis.web.app`).
Ciascuno entra con il proprio account Google e il menu è lo stesso sui due telefoni.
Il piano gratuito di Firebase (Spark) basta e avanza: non serve la carta di credito.

Tempo: circa 30 minuti, la prima volta.

**Cosa serve sul computer:** [Node.js](https://nodejs.org) (versione LTS), Python 3 e git.
Su Mac Python e git di solito ci sono già; per controllare, nel Terminale: `node -v`, `python3 --version`, `git --version`.

---

## 1. Scarica il codice

```bash
git clone https://github.com/aandreazito/menu-zitoschinis.git
cd menu-zitoschinis
git checkout menu-digitale
```

## 2. Crea il progetto Firebase

1. Vai su <https://console.firebase.google.com> ed entra con il tuo account Google.
2. **Crea un progetto** → nome `menu-zitoschinis` (se è già preso, Firebase propone una variante: segnati il nome esatto, lo chiamo *NOME-PROGETTO* qui sotto).
3. Google Analytics: **disattivalo**, non serve. → **Crea progetto**.

## 3. Registra l'app web e copia la configurazione

1. Nella pagina del progetto tocca l'icona **`</>`** (Web).
2. Nickname: `menu`. Non serve spuntare "Firebase Hosting" qui. → **Registra app**.
3. Ti mostra un blocco di codice con `const firebaseConfig = { apiKey: ..., ... }`. **Tienilo aperto**: ti serve al punto 6.
   (Lo ritrovi sempre in ⚙️ *Impostazioni progetto* → *Le tue app* → *Configurazione SDK*.)

## 4. Attiva l'accesso con Google

1. Menu a sinistra: **Build → Authentication** → **Inizia**.
2. Scheda **Metodo di accesso** → **Google** → attiva l'interruttore, scegli la tua email come email di assistenza → **Salva**.
3. Scheda **Impostazioni → Domini autorizzati**: controlla che ci sia `NOME-PROGETTO.web.app`. Se manca, aggiungilo.

### 4b. Accesso con link via email (per chi non ha un account Google)

1. Sempre in **Authentication → Metodo di accesso** → **Aggiungi nuovo provider** → **Email/password**.
2. Attiva **entrambi** gli interruttori: *Email/password* e **Link via email (accesso senza password)** → **Salva**.

Nell'app comparirà "oppure con la tua email": si scrive l'indirizzo, arriva una mail da
`noreply@NOME-PROGETTO.firebaseapp.com` con un link, e toccandolo si entra.
Anche in questo caso entra solo chi è scritto in `firestore.rules`.

## 5. Crea il database

1. Menu a sinistra: **Build → Firestore Database** → **Crea database**.
2. Posizione: **`eur3 (europe-west)`** (non si può cambiare dopo).
3. Modalità: **produzione**. → **Crea**.
   Le regole vere le carichiamo noi al punto 8: fino ad allora il database è chiuso a tutti.

## 6. Configura i file del progetto

**a) La configurazione.** Copia il file di esempio:

```bash
cp docs/firebase-config.example.js docs/firebase-config.js
```

Apri `docs/firebase-config.js` e incolla i valori del punto 3.
**Unica differenza:** in `authDomain` scrivi `NOME-PROGETTO.web.app` invece di `NOME-PROGETTO.firebaseapp.com`:
serve perché l'accesso con Google funzioni su iPhone (Safari blocca i cookie tra domini diversi).

**b) Chi può entrare.** Apri `firestore.rules` e sostituisci `EMAIL_DI_ANDREA` ed `EMAIL_DI_ALICE`
con i vostri due indirizzi Google, tra apici, per esempio `'nome.cognome@gmail.com'`.
Chiunque altro provi ad accedere vedrà "account non autorizzato" e nessun dato.

## 7. Autorizza il ritorno dall'accesso Google (per iPhone)

Va fatto una volta sola, perché al punto 6 hai messo `authDomain` su `.web.app`.

1. Vai su <https://console.cloud.google.com/apis/credentials> e in alto scegli il progetto `NOME-PROGETTO`.
2. Sotto **ID client OAuth 2.0** apri **Web client (auto created by Google Service)**.
3. In **URI di reindirizzamento autorizzati** → **Aggiungi URI** →
   `https://NOME-PROGETTO.web.app/__/auth/handler` → **Salva**.
   La modifica può metterci qualche minuto.

## 8. Installa gli strumenti e pubblica

Nella cartella `menu-zitoschinis`:

```bash
npm install -g firebase-tools        # su Mac, se dà errore di permessi: sudo npm install -g firebase-tools
firebase login                        # si apre il browser: entra con lo stesso account del punto 2
firebase use --add                    # scegli NOME-PROGETTO, come alias scrivi: default
python3 tools/build_pages.py          # deve scrivere "Firebase: attivo"
firebase deploy
```

Alla fine il terminale scrive l'indirizzo: **Hosting URL: https://NOME-PROGETTO.web.app**.
`firebase deploy` pubblica l'app e carica le regole del database (`firestore.rules`).

## 9. Primo accesso e storico

1. Apri `https://NOME-PROGETTO.web.app` → **Accedi con Google** (con la tua email).
2. L'archivio è vuoto: tocca **Carica lo storico**. Carica le 32 settimane trascritte dai fogli. Va fatto **una volta sola**.
3. Le settimane e le ricette compaiono subito, anche sul telefono di Alice.

> Le modifiche fatte nel frattempo nell'artifact su claude.ai non passano da sole su Firebase:
> se ne avete fatte, rifatele qui (oppure chiedimi di esportarle).

## 10. Sul telefono

- **iPhone:** apri l'indirizzo in **Safari** → tasto Condividi → **Aggiungi alla schermata Home**. Si apre a tutto schermo, come un'app.
- **Android:** Chrome → menu ⋮ → **Aggiungi a schermata Home**.
- Alice fa lo stesso. Se non ha un account Google, sceglie **oppure con la tua email**:
  1. scrive la sua email e tocca **Mandami il link di accesso**;
  2. apre la mail **sullo stesso telefono** e tocca il link: si apre l'app già dentro (se non la trova, guardare nello spam);
  3. se usa l'icona sulla schermata Home, su iPhone il link si apre in Safari e non nell'icona:
     nella mail **tiene premuto il link → Copia**, apre l'icona e lo incolla nel campo *Link della mail* → **Entra con il link**.
  Il link vale una volta sola e scade dopo qualche ora: se serve, se ne chiede un altro.

---

## Aggiornare l'app in futuro

```bash
git pull
python3 tools/build_pages.py
firebase deploy --only hosting           # solo l'app
firebase deploy --only firestore:rules   # solo le regole (se cambiate le email)
```

I dati non si toccano: stanno nel database, non nei file.

## Se qualcosa non va

| Cosa vedi | Cosa fare |
|---|---|
| "L'account … non è tra quelli autorizzati" | Controlla le email in `firestore.rules` (scritte uguali all'account Google), poi `firebase deploy --only firestore:rules`. |
| Su iPhone "Accedi con Google" non fa niente o torna indietro senza entrare | Rivedi i punti 6a (`authDomain` con `.web.app`) e 7, aspetta qualche minuto e riprova. Prova anche da Safari prima che dall'icona sulla Home. |
| "l'accesso via email non è attivo in Firebase" | Passo 4b: attiva *Link via email*. |
| La mail con il link non arriva | Guarda nello spam; il mittente è `noreply@NOME-PROGETTO.firebaseapp.com`. |
| "il link è scaduto o è già stato usato" | Tocca *Cambia email o rimanda il link* e usa il link della mail più recente. |
| `build_pages.py` scrive "Firebase: non configurato" | Manca `docs/firebase-config.js` (punto 6a). |
| Dopo un aggiornamento vedi la versione vecchia | Chiudi e riapri l'app, oppure ricarica la pagina. |
| "Firebase non è partito: …" | Di solito è un valore copiato male in `docs/firebase-config.js`. |

`docs/firebase-config.js` non contiene segreti (la protezione la fanno le regole),
quindi potete salvarlo nel repository con `git add docs/firebase-config.js && git commit -m "Config Firebase"`.
