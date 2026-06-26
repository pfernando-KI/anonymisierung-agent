% Anonymisierungs-Agent – Schritt-für-Schritt-Anleitung
% Für Anwenderinnen und Anwender ohne Programmiererfahrung

```{=typst}
#pagebreak()
```

# Was macht dieses Programm?

Der **Anonymisierungs-Agent** entfernt persönliche Daten aus Ihren Dokumenten,
bevor Sie diese an eine KI weitergeben. Namen, E-Mail-Adressen, Telefonnummern,
Firmen und Adressen werden durch neutrale Platzhalter ersetzt – zum Beispiel
`[NAME]` oder `[EMAIL]`.

Das Besondere: **Alles läuft lokal auf Ihrem Computer.** Es werden keine Daten
ins Internet geschickt. Das KI-Modell, das die Anonymisierung übernimmt, läuft
über ein kostenloses Programm namens **LM Studio** direkt auf Ihrem Gerät.

```{=typst}
#pagebreak()
```

# Überblick: die vier Schritte

1. **LM Studio installieren** und ein Modell laden
2. **Den Agenten installieren** (einmalig, per Doppelklick-Skript)
3. **Den Agenten starten** und ein Dokument anonymisieren
4. **Das fertige Dokument abholen**

```{=typst}
#pagebreak()
```

# Schritt 1 – LM Studio installieren

1. Öffnen Sie die Webseite **https://lmstudio.ai/**
2. Laden Sie LM Studio für Ihr Betriebssystem herunter (Windows oder macOS)
3. Installieren Sie das Programm wie gewohnt und öffnen Sie es

## Modell laden

1. Suchen Sie in LM Studio nach einem Modell (z. B. `gemma`)
2. Laden Sie das Modell herunter (einmalig, kann einige Minuten dauern)
3. Wählen Sie das Modell oben im Fenster aus und laden Sie es

## Nur lokale Modelle – automatischer Schutz

LM Studio kann auch **Cloud-Modelle** einbinden – zum Beispiel ChatGPT (OpenAI),
Claude (Anthropic) oder Gemini (Google). Solche Modelle schicken Ihre Daten **ins
Internet**. Das widerspricht dem ganzen Zweck dieses Programms.

**Sie müssen sich darum nicht selbst kümmern:** Der Agent erkennt Cloud-Modelle
automatisch, blendet sie in der Auswahl aus und bietet Ihnen nur lokale Modelle an.
Findet er gar kein lokales Modell, **stoppt** er mit einer klaren Meldung, statt
versehentlich Daten in die Cloud zu schicken.

**Ihre Empfehlung beim Laden in LM Studio:**

- Nur Modelle laden, die als lokale Dateien (GGUF) auf Ihrem Computer liegen
- Keine Verbindungen zu OpenAI, Anthropic, Google o. ä. aktivieren

## Den lokalen Server starten

1. Klicken Sie links auf **„Developer"**
2. Wechseln Sie in den Reiter **„Local Server"**
3. Stellen Sie den Schalter auf **„Running"**
4. Wenn alles läuft, zeigt LM Studio **Status: Running** in Grün an
5. Notieren Sie sich die Adresse – in der Regel `http://localhost:1234`

> **Wichtig:** LM Studio muss laufen, solange Sie den Agenten benutzen.

```{=typst}
#pagebreak()
```

# Schritt 2 – Den Agenten installieren

Sie brauchen die Programmdateien des Agenten (als Ordner auf Ihrem Computer).
Außerdem muss **Python 3.10 oder neuer** installiert sein. Falls nicht:
laden Sie es von **https://www.python.org/downloads/** und installieren Sie es.

## Installation per Skript

**Windows:**

1. Öffnen Sie den Ordner des Agenten
2. Doppelklicken Sie auf **`install.bat`**
3. Warten Sie, bis „Installation abgeschlossen" erscheint

**macOS:**

1. Öffnen Sie das Programm **„Terminal"**
2. Tippen Sie `cd ` (mit Leerzeichen) und ziehen Sie den Agenten-Ordner ins
   Terminal-Fenster, dann **Enter**
3. Tippen Sie `./install.sh` und **Enter**
4. Warten Sie, bis „Installation abgeschlossen" erscheint

Das Skript richtet alles automatisch ein. Diesen Schritt müssen Sie nur **einmal**
ausführen.

```{=typst}
#pagebreak()
```

# Schritt 3 – Den Agenten starten

**Windows** – im Agenten-Ordner nacheinander ausführen:

```
venv\Scripts\activate.bat
python agent.py
```

**macOS** – im Terminal (im Agenten-Ordner):

```
source venv/bin/activate
python3 agent.py
```

Wenn alles funktioniert, erscheint zuerst eine **Modellauswahl**:

```
Anonymisierungs-Agent gestartet

Verfuegbare Modelle in LM Studio:
  1) google/gemma-3-4b  (Default)
  2) qwen2.5-7b-instruct
Wahl [Enter = google/gemma-3-4b]:
```

Drücken Sie einfach **Enter** für das vorgeschlagene Modell, oder tippen Sie die Nummer
eines anderen Modells. Wählen Sie ein Modell, das zu Ihrem Arbeitsspeicher passt –
größere Modelle brauchen mehr RAM.

> **Hinweis:** In dieser Liste erscheinen nur lokale Modelle. Erkannte Cloud-Modelle
> werden automatisch ausgeblendet (siehe „Nur lokale Modelle – automatischer Schutz").

Danach erscheint:

```
LM Studio erreichbar - Modell: google/gemma-3-4b
Ueberwache input_docs/ ...
```

Das Fenster bleibt offen. Der Agent wartet jetzt auf Dokumente.

> Erscheint stattdessen „LM Studio ist nicht erreichbar"? Dann läuft der Server
> nicht. Zurück zu Schritt 1 und den Server auf „Running" stellen.

```{=typst}
#pagebreak()
```

# Schritt 4 – Ein Dokument anonymisieren

1. Legen Sie Ihr Originaldokument in den Ordner **`input_docs/`**
2. Der Agent erkennt die Datei automatisch (nach wenigen Sekunden)
3. Im Fenster sehen Sie den Fortschritt
4. Das fertige, anonymisierte Dokument finden Sie im Ordner **`output_docs/`**
5. Ihr Originaldokument wird automatisch nach **`processed/`** verschoben
   (es bleibt also erhalten)

## Welche Dateien funktionieren?

| Format | Beispiel |
|--------|----------|
| Textdateien | `.txt` |
| Word-Dokumente | `.docx` |
| PDF-Dateien | `.pdf` |
| Excel-Tabellen | `.xlsx` |
| E-Mails | `.eml`, `.msg` |

> **Hinweis zu E-Mail-Anhängen:** Anhänge (PDFs, Word, Bilder) innerhalb einer E-Mail werden **nicht** automatisch mitverarbeitet. Wenn Sie Anhänge anonymisieren möchten, speichern Sie diese separat ab und legen Sie sie ebenfalls in `input_docs/`.

```{=typst}
#pagebreak()
```

# Den Agenten beenden

Drücken Sie im Fenster **`Strg + C`** (macOS: `Ctrl + C`).
Der Agent zeigt zum Abschluss eine Bilanz: wie viele Daten er ersetzt hat sowie drei
Kontrollzeilen – echte Fehler, Zellen mit Fallback und Absätze mit Fallback (siehe
Abschnitt „Selbstkontrolle des Agenten").

# Wichtiger Hinweis zur Sorgfalt

Die KI arbeitet sehr zuverlässig, aber nicht zu 100 % garantiert fehlerfrei.
**Prüfen Sie jedes anonymisierte Dokument kurz**, bevor Sie es weitergeben –
besonders bei sensiblen Inhalten.

Der Agent ist absichtlich **vorsichtig**: Im Zweifel ersetzt er einen Namen lieber, als
ihn zu übersehen. Deshalb werden manchmal auch **öffentliche Stellen, Studienquellen oder
Plattformen** (z. B. IHK, Bitkom, KfW, LinkedIn) als `[FIRMA]` markiert, obwohl sie nicht
geheim sind. Das ist **kein Fehler** – Sie können solche Namen im fertigen Dokument von
Hand wieder einsetzen.

```{=typst}
#pagebreak()
```

# Selbstkontrolle des Agenten

Der Agent **prüft jede Antwort der KI noch einmal nach**. Manchmal „erfindet" die KI
einen falschen Platzhalter (z. B. `[BERUF]`) oder ersetzt etwas, das gar nicht persönlich
ist – etwa eine Abteilung wie „Vertrieb" oder eine Spalte wie „Jahr 1".

In so einem Fall **versucht es der Agent automatisch ein zweites Mal**, mit einer
strengeren Anweisung an die KI. Klappt auch das nicht, lässt der Agent die betroffene
Stelle lieber **unverändert im Original** stehen – und merkt sie sich in der Datei
**`anonymisierung_fallback.txt`**.

Am Ende eines Laufs zeigt der Agent drei Zahlen:

- wie viele **echte Fehler** auftraten,
- wie viele **Tabellenzellen** auf das Original zurückgesetzt wurden,
- wie viele **Absätze** auf das Original zurückgesetzt wurden.

> **Wichtig:** Genau diese zurückgesetzten Stellen sollten Sie anschließend **von Hand
> prüfen** – dort konnte die KI nicht sicher anonymisieren.

# Hilfe bei Problemen

| Problem | Lösung |
|---------|--------|
| „LM Studio ist nicht erreichbar" | Server in LM Studio auf „Running" stellen |
| „Keine lokalen Modelle gefunden" | In LM Studio ein lokales (GGUF-)Modell laden, kein Cloud-Modell |
| Datei landet im Ordner `fehler/` | Datei ist beschädigt – Original prüfen |
| „X Zellen/Absätze mit Fallback" | `anonymisierung_fallback.txt` öffnen, diese Stellen von Hand prüfen |
| Öffentliche Institution/Quelle als `[FIRMA]` ersetzt | So gewollt (Vorsicht) – Namen bei Bedarf manuell wieder einsetzen |
| „Datei gesperrt" | Dokument noch in Word/Excel offen – schließen |
| Klartext noch im Ergebnis | Dokument erneut in `input_docs/` legen |
