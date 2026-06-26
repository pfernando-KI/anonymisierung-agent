# CLAUDE.md – Projektkontext

Kurzkontext fuer KI-Assistenten (z. B. Claude Code), die in diesem Repository arbeiten.

## Zweck

Lokaler Anonymisierungs-Agent: pseudonymisiert beliebige Dokumente (Volltexte,
Tabellen, E-Mails), bevor sie an externe KI-Systeme weitergegeben werden. Die
Verarbeitung laeuft vollstaendig lokal ueber LM Studio – es verlassen keine
personenbezogenen Daten das Geraet.

## Technischer Stack

- Python 3.10+
- Lokales LLM ueber LM Studio (OpenAI-kompatible API)
- Standard-URL: `http://localhost:1234/v1` (per `LM_STUDIO_URL` ueberschreibbar)

## Verzeichnisstruktur

```
.
├── input_docs/      → Originaldokumente hier ablegen (gitignored)
├── output_docs/     → anonymisierte Ergebnisse hier abholen (gitignored)
├── processed/       → Originale nach erfolgreicher Verarbeitung (gitignored)
├── fehler/          → beschaedigte / nicht lesbare Dateien (gitignored)
├── agent.py         → Hauptagent (Verarbeitungsschleife, Format-Handler)
├── config.py        → zentrale Konfiguration (alle Einstellungen hier)
├── test_offline.py  → Offline-Tests mit Stub-LLM (kein LM Studio noetig)
└── requirements.txt → Abhaengigkeiten
```

## Verarbeitungsmodi (automatisch erkannt)

- **VOLLTEXT** – TXT, PDF, einfache DOCX, E-Mails → gesamter Inhalt
- **TABELLE** – XLSX, Tabellen in DOCX → nur Zellen mit Personenbezug
  (Regex-Vorfilter fuer E-Mail/Telefon, LLM nur fuer mehrdeutige Zellen)

## Konventionen

- Alle Einstellungen ausschliesslich in `config.py` aendern, nicht in `agent.py`.
- Deutschsprachige Bezeichner, Kommentare und Ausgaben.
- Vor Aenderungen an der Logik: `python3 test_offline.py` muss gruen bleiben.
- Keine echten/personenbezogenen Testdaten einchecken – nur Mock-Daten wie in
  `test_offline.py`.

## Tests

```bash
python3 test_offline.py
```

Prueft Format-Erkennung, Modus-Wahl, XLSX-/EML-Verarbeitung, Regex-Vorfilter und
Zaehler ohne erreichbares Modell (Stub-LLM).
