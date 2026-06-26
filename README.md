# Anonymisierungs-Agent

Lokales Werkzeug zum Pseudonymisieren von Dokumenten **bevor** sie an externe
KI-Systeme weitergegeben werden.

Originaldokumente mit Personenbezug werden lokal anonymisiert und als
LLM-sichere Dokumente ausgegeben – **ohne dass persönliche Daten das Gerät
verlassen**. Das Sprachmodell läuft vollständig lokal über
[LM Studio](https://lmstudio.ai/).

> ⚠️ **Wichtig:** Dieses Tool ist eine **Vorverarbeitung**. Anonymisierte Dokumente
> müssen vor Weitergabe an Dritte oder externe KI-Systeme **manuell geprüft** werden.
> Die Genauigkeit liegt bei etwa 90 % – die letzten 10 % sind die kritischen.
> **Außerdem: LM Studio kann auch Cloud-Modelle einbinden – der Agent blockiert diese
> automatisch, prüfe aber im Zweifel die Modellauswahl beim Start.**
> Der Agent verhält sich konservativ: Im Zweifel werden Firmennamen ersetzt. Das gilt auch
> für öffentliche Institutionen, Studienquellen und Plattformen (z. B. IHK, Bitkom, KfW,
> LinkedIn). Diese müssen bei Bedarf manuell restauriert werden.

---

## Hintergrund

Als Transformationsberaterin für KMU verarbeite ich Dokumente, die unter keinen
Umständen in Cloud-LLMs gelangen dürfen. Statt mich auf Drittanbieter-Versprechen zu
verlassen, habe ich eine lokale Lösung gebaut: Gemma via LM Studio, kein Datenleck
möglich. Dieses Repository dokumentiert die Umsetzung und macht den Ansatz für andere
nutzbar.

---

## Features

- **6 Dateiformate:** `.txt`, `.docx`, `.pdf`, `.xlsx`, `.eml`, `.msg`
- **2 automatisch erkannte Modi:**
  - **VOLLTEXT** – TXT, PDF, einfache DOCX, E-Mails → gesamter Inhalt
  - **TABELLE** – XLSX, Tabellen in DOCX → nur Zellen mit Personenbezug
    (schneller Regex-Vorfilter für E-Mail/Telefon, LLM nur bei mehrdeutigen Zellen)
- **Vollständig lokal** – keine Cloud, kein Datenleck
- **Formaterhaltend** – DOCX-Formatierung und XLSX-Formeln/Zahlen bleiben unverändert
- **Robust** – erkennt in Word/Excel geöffnete (gesperrte) Dateien und versucht es erneut

---

## Voraussetzungen

- **Python 3.10** oder neuer (`python3 --version`)
- **LM Studio** installiert mit einem geladenen Modell (z. B. `google/gemma-3-4b`)

---

## Schnellstart

```bash
# Vorher prüfen: Python 3.10 oder neuer muss installiert sein
python3 --version

git clone https://github.com/pfernando-KI/anonymisierung-agent.git
cd anonymisierung-agent

# macOS / Linux
./install.sh

# Windows
install.bat
```

Das Install-Skript legt eine virtuelle Umgebung an, installiert alle
Abhängigkeiten und erstellt die Arbeitsordner.

---

## Manuelle Installation

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## LM Studio einrichten

1. **LM Studio öffnen**
2. Ein Modell auswählen und laden (Standard in der Konfiguration: `google/gemma-3-4b`)
3. Links auf **„Developer"** → Tab **„Local Server"**
4. Server auf **„Running"** stellen
5. Standard-Adresse ist `http://localhost:1234` – läuft LM Studio auf einem anderen
   Gerät oder Port, die Adresse über die Umgebungsvariable `LM_STUDIO_URL` setzen
   (siehe [Konfiguration](#konfiguration)).

---

## Lokales Modell sicher auswählen

**Wichtig:** LM Studio kann sowohl lokale als auch Cloud-Modelle (OpenAI, Anthropic,
Google) einbinden. Dieser Agent ist ausschließlich für lokale Modelle gedacht. Wenn du
versehentlich ein Cloud-Modell wählst, verlassen deine Daten den Rechner.

**Schutz im Agenten:** Beim Start prüft der Agent automatisch, ob die in LM Studio
gemeldeten Modelle lokal sind. Erkannte Cloud-Modelle werden ausgeblendet und nicht zur
Auswahl angeboten. Wenn keine lokalen Modelle gefunden werden, bricht der Agent mit einer
Fehlermeldung ab.

**Empfehlung zur Modellauswahl in LM Studio:**

1. In LM Studio nur Modelle laden, die als GGUF-Dateien lokal gespeichert sind
2. Keine API-Bridges zu OpenAI, Anthropic, Google oder anderen Cloud-Anbietern aktivieren
3. Im Tab „Local Server" prüfen: nur lokale Modelle dürfen geladen sein

**Wenn der Agent unerwartet Modelle ausblendet:** Prüfe `CLOUD_MODEL_MUSTER` in `config.py`.
Diese Liste filtert nach Namensmustern und kann bei falsch-positiven Treffern angepasst
werden.

---

## Modell wählen

Beim Start zeigt der Agent die in LM Studio verfügbaren Modelle als nummerierte Liste.
Du wählst per Zahl; **Enter** nimmt den Standard (`MODEL` aus `config.py`). So kann jeder
das Modell nutzen, das zu seinem Arbeitsspeicher passt – ohne Code zu ändern.

Das Menü lässt sich abschalten (fester Wert aus `config.py`): Flag
`MODELL_BEIM_START_WAEHLEN = False` setzen oder Umgebungsvariable
`MODELL_BEIM_START_WAEHLEN=0`. Im Headless-Betrieb (kein Terminal) wird automatisch der
Standard verwendet.

### Welches Modell passt zu meinem RAM?

Die folgenden Angaben sind **Erfahrungswerte aus eigener Nutzung – keine Garantie**.
Der tatsächliche Speicherbedarf hängt von Modell, Quantisierung und Kontextlänge ab.
Maßgeblich sind die Angaben auf der jeweiligen **Modellkarte in LM Studio** sowie die
[LM-Studio-Dokumentation](https://lmstudio.ai/docs):

| RAM (ungefähr) | Erfahrungswert |
|----------------|----------------|
| 8–16 GB | kleinere Modelle (~1B–3B, z. B. quantisiert) |
| ab 24–32 GB | größere Modelle (~7B–8B) für genauere Urteile |

Lädt LM Studio ein Modell wegen zu wenig Speicher nicht (HTTP-400-Meldung), gibt der Agent
einen klaren Hinweis: kleineres Modell wählen oder Speicher freigeben.

---

## Nutzung

```bash
source venv/bin/activate        # Windows: venv\Scripts\activate.bat
python3 agent.py
```

Beispiel eines typischen Laufs:

```
$ python3 agent.py
==================================================
Anonymisierungs-Agent gestartet
Unterstuetzte Formate: .docx, .eml, .msg, .pdf, .txt, .xlsx
Modi: VOLLTEXT | TABELLE (automatisch erkannt)
==================================================

Verfuegbare Modelle in LM Studio:
  1) google/gemma-3-4b  (Default)
  2) qwen2.5-7b-instruct
Wahl [Enter = google/gemma-3-4b]: <Enter>

LM Studio erreichbar - Modell: google/gemma-3-4b
Ueberwache input_docs/ ...

==================================================
Verarbeite: testdokument.docx
  Modus: VOLLTEXT (DOCX)
Gespeichert: output_docs/testdokument_anonymisiert.docx
Zusammenfassung fuer testdokument.docx:
  Personennamen: 3
  E-Mail-Adressen: 2
  Telefonnummern: 1
Original verschoben nach: processed/

Sitzungs-Bilanz:
  Echte Fehler: 0
  Zellen mit Fallback: 0
  Absätze mit Fallback: 0
```

Dann:

1. Originaldokument in **`input_docs/`** ablegen
2. Der Agent erkennt die Datei automatisch (Wartezeit bis ~5 Sekunden)
3. Anonymisiertes Dokument aus **`output_docs/`** abholen
4. Das Original liegt anschließend in **`processed/`** (zur Sicherheit aufbewahrt)

Beenden mit **`Strg + C`** – der Agent zeigt eine Sitzungsbilanz: ersetzte Daten,
echte Fehler und Zellen mit Fallback (die manuell zu prüfen sind).

---

## Unterstützte Formate

| Dateiformat | Modus | Was passiert |
|-------------|-------|--------------|
| `.txt` | VOLLTEXT | Gesamter Text wird anonymisiert |
| `.pdf` | VOLLTEXT | Seitenweise verarbeitet, Ausgabe als `.txt` |
| `.docx` (Fließtext) | VOLLTEXT | Gesamter Text wird anonymisiert |
| `.docx` (mit Tabelle) | TABELLE | Tabellenzellen mit Personenbezug + Fließtext |
| `.xlsx` | TABELLE | Formeln und Zahlen bleiben unverändert |
| `.eml` / `.msg` | VOLLTEXT | Von, An, Cc, Betreff und Textinhalt |

> **Hinweis zu E-Mail-Anhängen:** Anhänge in `.eml`/`.msg`-Dateien werden **nicht** automatisch mitverarbeitet. Wenn Anhänge anonymisiert werden sollen, müssen sie separat in `input_docs/` abgelegt werden.

---

## Was wird anonymisiert?

| Platzhalter | Ersetzt |
|-------------|---------|
| `[NAME]` | Personennamen |
| `[FIRMA]` | Firmennamen |
| `[EMAIL]` | E-Mail-Adressen |
| `[TELEFON]` | Telefonnummern |
| `[ADRESSE]` | Straße, Hausnummer, Postleitzahl |
| `[ORT]` | Städte und spezifische Orte |
| `[DATUM]` | Personenbezogene Datumsangaben |

> **Hinweis:** Anonymisierung durch ein Sprachmodell ist sehr zuverlässig, aber nicht
> garantiert vollständig. Ausgabedokumente vor der Weitergabe stichprobenartig prüfen.

**Halluzinations-Schutz im Tabellen-Modus:** Pro Zelle sind nur die 7 obigen Platzhalter
erlaubt. Erfindet das Modell ein anderes Token (z. B. `[BERUF]`), wird die Antwort verworfen,
ein zweiter, strengerer Versuch gestartet und – falls auch der scheitert – die Zelle auf den
sicheren Regex-Vorfilter zurückgesetzt. Solche Fälle landen in `anonymisierung_fallback.txt`
und werden am Ende als „X Zellen mit Fallback – bitte manuell prüfen" gemeldet.

---

## Konfiguration

Alle Einstellungen stehen in **`config.py`** – dort ändern, nie in `agent.py`:

| Einstellung | Standardwert | Beschreibung |
|-------------|--------------|--------------|
| `LM_STUDIO_URL` | `http://localhost:1234/v1` | Adresse des LM-Studio-Servers |
| `MODEL` | `google/gemma-3-4b` | Modell-ID / Vorauswahl (muss mit LM Studio übereinstimmen) |
| `MODELL_BEIM_START_WAEHLEN` | `True` | Modell-Auswahlmenü beim Start (False = fester Wert) |
| `POLL_SEKUNDEN` | `5` | Wie oft `input_docs/` geprüft wird |
| `RETRY_SEKUNDEN` | `30` | Wartezeit bei gesperrten Dateien |

`LM_STUDIO_URL` und `MODEL` lassen sich auch ohne Codeänderung über eine
`.env`-Datei oder Umgebungsvariablen überschreiben:

```bash
cp .env.example .env
# .env bearbeiten, z. B. LM_STUDIO_URL=http://192.168.1.50:1234/v1
```

---

## Tests (ohne LM Studio)

Prüft die Logik des Agenten mit einem Stub-Modell – kein laufendes LM Studio nötig:

```bash
python3 test_offline.py
```

Erwartetes Ergebnis: alle Prüfungen bestanden.

---

## Verzeichnisübersicht

```
anonymisierung-agent/
├── input_docs/      ← Originaldokumente hier ablegen
├── output_docs/     ← anonymisierte Dokumente hier abholen
├── processed/       ← Originale nach erfolgreicher Verarbeitung
├── fehler/          ← Dateien, die nicht gelesen werden konnten
├── agent.py         ← Hauptagent
├── config.py        ← zentrale Konfiguration
├── test_offline.py  ← Offline-Tests
├── install.sh       ← Installation (macOS / Linux)
└── install.bat      ← Installation (Windows)
```

`input_docs/`, `output_docs/`, `processed/` und `fehler/` werden **nicht** versioniert
(siehe `.gitignore`) – sie können personenbezogene Daten enthalten.

---

## Fehlerbehebung

| Meldung / Problem | Ursache | Lösung |
|-------------------|---------|--------|
| „LM Studio ist nicht erreichbar" | Server nicht gestartet | LM Studio → Developer → Local Server → Running |
| „Modell konnte nicht geladen werden" | Modell zu groß für den RAM | kleineres Modell wählen oder Speicher freigeben |
| Datei wandert nach `fehler/` | Datei beschädigt / nicht lesbar | `anonymisierung_fehler.txt` für Details öffnen |
| „X Zellen mit Fallback" | Modell-Antwort(en) verworfen | `anonymisierung_fallback.txt` öffnen, betroffene Zellen manuell prüfen |
| „Datei gesperrt" | Datei noch in Word/Excel offen | Datei schließen – Agent versucht es nach 30 s erneut |
| Klartext im Ausgabedokument | Modell hat eine Stelle übersehen | Ausgabe prüfen, Datei ggf. erneut einlegen |

---

## Lessons Learned aus der Entwicklung

- **Kleine Modelle halluzinieren bei Tabellenzellen.** Ohne Kontext erfindet ein 3B-Modell
  Platzhalter wie [BERUF] oder [ROHGEWINN]. Gelöst über einen Guard, der nur die definierten
  7 Platzhalter erlaubt.

- **Lokal heißt nicht automatisch DSGVO-konform.** Auch der lokale LLM-Pfad braucht
  Validierung, Logging und manuelle Stichproben – sonst entsteht nur eine andere Art von
  Blackbox.

- **Modellauswahl beim Start statt Hardcoding.** Nutzer haben unterschiedliche
  RAM-Ausstattungen. Eine interaktive Auswahl mit Default-Vorschlag ist robuster als ein
  fester Wert in der Config.

- **Tests ohne LLM.** `test_offline.py` mit Stub-LLM erlaubt schnelle Iteration ohne
  LM Studio – kritisch für CI/CD und Reproduzierbarkeit.

---

## Sicherheit

Sicherheitslücken bitte **nicht** über öffentliche Issues melden, sondern über die private
Reporting-Funktion – siehe [SECURITY.md](SECURITY.md).

---

## Geplante Verbesserungen (v1.1+)

Diese Verbesserungen sind für künftige Versionen vorgesehen und werden nach
Praxis-Feedback priorisiert:

- **Schonung öffentlicher Institutionen und Quellen:** Erweiterung des Prompts um eine
  Negativ-Liste bekannter Institutionen (IHK, Bitkom, KfW, Destatis etc.), damit diese im
  Volltext erhalten bleiben. Aktuell werden sie konservativ als [FIRMA] markiert und
  müssen manuell restauriert werden.
- **Weitere Verbesserungen entstehen aus echtem Nutzer-Feedback** – wenn du auf
  systematische Über- oder Unter-Anonymisierung stößt, freue ich mich über ein Issue
  (private vulnerability reporting für Privacy-relevante Funde, normales Issue für alles
  andere).

---

## Lizenz

[MIT](LICENSE) © 2026 Patricia Fernando
