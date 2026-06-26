"""Zentrale Konfiguration des Anonymisierungs-Agenten.

Alle Einstellungen an einem Ort. Anpassungen nur hier vornehmen,
nicht in agent.py.

LM_STUDIO_URL und MODEL lassen sich zusaetzlich per Umgebungsvariable
ueberschreiben (z.B. in einer .env oder direkt im Terminal), ohne diese
Datei zu aendern:

    export LM_STUDIO_URL="http://192.168.1.50:1234/v1"
    export MODEL="google/gemma-3-4b"
"""
import os
from pathlib import Path

# Optional: Werte aus einer .env-Datei laden, falls python-dotenv installiert
# ist. Ohne python-dotenv gelten weiterhin die Standardwerte bzw. echte
# Umgebungsvariablen (export LM_STUDIO_URL=...).
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

# --- LM Studio / lokales LLM ---------------------------------------------
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
# MODEL ist die Vorauswahl. Beim Start kann (bei aktivem MODELL_BEIM_START_WAEHLEN)
# eines der in LM Studio verfuegbaren Modelle gewaehlt werden; Enter nimmt diesen Wert.
MODEL = os.getenv("MODEL", "google/gemma-3-4b")
API_KEY = "lm-studio"          # LM Studio ignoriert den Wert, muss aber gesetzt sein
TEMPERATURE = 0.1              # niedrig = moeglichst deterministische Anonymisierung

# Beim Start ein Modell aus der LM-Studio-Liste waehlen lassen (interaktiv).
# Auf False setzen, um immer fest MODEL zu verwenden (z.B. headless/Server).
MODELL_BEIM_START_WAEHLEN = os.getenv("MODELL_BEIM_START_WAEHLEN", "1") not in ("0", "false", "False")

# Namensmuster, an denen Cloud-Modelle (OpenAI, Anthropic, Google, ...) erkannt
# werden. Solche Modelle wuerden Daten in die Cloud schicken und werden daher
# beim Start hart blockiert (siehe agent._ist_cloud_modell / waehle_modell).
# WICHTIG: Diese Liste muss regelmaessig gepflegt werden - Cloud-Anbieter aendern
# ihre Namensschemata. Bei falsch-positiven Treffern hier anpassen.
CLOUD_MODEL_MUSTER = [
    "gpt-", "gpt4", "gpt3", "claude", "anthropic", "openai",
    "gemini-pro", "gemini-1.5", "gemini-2", "/api/",
    "azure", "bedrock", "mistral-large", "mistral-medium",
    "command-r", "cohere",
]

# --- Verzeichnisse --------------------------------------------------------
BASIS_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASIS_DIR / "input_docs"       # Originaldokumente (rote Rohdaten)
OUTPUT_DIR = BASIS_DIR / "output_docs"     # anonymisierte Ergebnisse (gruen)
PROCESSED_DIR = BASIS_DIR / "processed"    # Originale nach erfolgreicher Verarbeitung
FEHLER_DIR = BASIS_DIR / "fehler"          # beschaedigte / nicht lesbare Dateien

# --- Logging --------------------------------------------------------------
FEHLER_LOG = BASIS_DIR / "anonymisierung_fehler.txt"      # echte technische Fehler
FALLBACK_LOG = BASIS_DIR / "anonymisierung_fallback.txt"  # Halluzinations-Rollbacks (Tabellen)

# --- Verhalten ------------------------------------------------------------
POLL_SEKUNDEN = 5              # Intervall, in dem input_docs/ geprueft wird
RETRY_SEKUNDEN = 30           # Wartezeit fuer gesperrte (z.B. in Word offene) Dateien

# --- Anonymisierungsregeln -----------------------------------------------
# Platzhalter, die ersetzt UND in der Endzusammenfassung gezaehlt werden.
# Token -> Klartextbezeichnung fuer den Bericht.
PLATZHALTER = {
    "[NAME]": "Personennamen",
    "[FIRMA]": "Firmennamen",
    "[EMAIL]": "E-Mail-Adressen",
    "[TELEFON]": "Telefonnummern",
    "[ADRESSE]": "Adressen",
    "[ORT]": "Orte",
    "[DATUM]": "Datumsangaben",
}

# Dateiendungen, die der Agent verarbeitet.
UNTERSTUETZTE_FORMATE = {".txt", ".pdf", ".docx", ".xlsx", ".eml", ".msg"}

# --- Prompts --------------------------------------------------------------
# Alle Prompts an einem Ort. Anpassungen der Anonymisierungs-Anweisungen nur hier.

# VOLLTEXT-Modus: gesamten Text anonymisieren.
PROMPT_VOLLTEXT = """Du bist ein Datenschutz-Assistent. Anonymisiere den folgenden Text vollstaendig.

Ersetze:
- Namen von Personen -> [NAME]
- Firmennamen -> [FIRMA]
- E-Mail-Adressen -> [EMAIL]
- Telefonnummern -> [TELEFON]
- Adressen -> [ADRESSE]
- Spezifische Orte -> [ORT]
- Datum wenn personenbezogen -> [DATUM]

Erfinde KEINE neuen Saetze. Fuege KEINE Erklaerungen, Beispiele oder Kontaktbloecke hinzu.
Wenn ein Absatz keine personenbezogenen Daten enthaelt, gib ihn 1:1 unveraendert zurueck.

Gib NUR den anonymisierten Text zurueck. Keine Erklaerungen.

Text:
"""

# TABELLEN-/Antwort-Modus: nur direkte personenbezogene Daten ersetzen, Kontext schonen.
PROMPT_ANTWORT = """Du bist ein Datenschutz-Assistent. Anonymisiere den folgenden Text.

Ersetze NUR direkte personenbezogene Daten:
- Vor- und Nachnamen von Personen -> [NAME]
- Firmennamen und Unternehmensnamen -> [FIRMA]
- E-Mail-Adressen -> [EMAIL]
- Telefonnummern -> [TELEFON]
- Strasse, Hausnummer, PLZ, Stadt -> [ADRESSE]
- Jahreszahlen die Personen identifizieren (z.B. Gruendungsjahr) -> [DATUM]

Ersetze NICHT:
- Spaltenueberschriften und Tabellenkoepfe (z.B. "Jahr 1", "Jahr 2", "M01", "M12")
- Kostenarten und Buchhaltungsbegriffe (z.B. "Steuerberater", "Krankenkasse",
  "Rohgewinn", "Privatentnahme", "Gruendungskosten", "Betriebsausgaben")
- Berufsbezeichnungen (z.B. Geschaeftsfuehrer, Inhaberin, Buchhalter)
- Software-/Produktnamen (z.B. Claude, ChatGPT, M365, Excel, DATEV)
- Kuerzel und Codes (z.B. "B1", "B3")
- Allgemeine Beschreibungen, Taetigkeiten und Zahlen ohne Personenbezug

Erlaubt sind ausschliesslich diese 7 Platzhalter:
[NAME] [FIRMA] [EMAIL] [TELEFON] [ADRESSE] [ORT] [DATUM]
Erfinde KEINE anderen Tokens und schreibe NIEMALS das Wort UNVERAENDERT in den Text.

Wenn der Text keine personenbezogenen Daten enthaelt, gib ihn wortwoertlich zurueck.
Gib NUR den anonymisierten Text zurueck. Keine Erklaerungen.

Text:
"""

# Strikter Wiederholungs-Prompt fuer den 2. Versuch, wenn der Guard die erste
# Modellantwort verworfen hat (z.B. erfundene Tokens). Identisch zu PROMPT_ANTWORT
# plus expliziter Negativliste aus dem realen Live-Test.
PROMPT_ANTWORT_STRIKT = PROMPT_ANTWORT.replace(
    "\nText:\n",
    "\nWICHTIG: Diese Tokens sind VERBOTEN: [BERUF], [TEXT], [ROHGEWINN], UNVERAENDERT, "
    "sowie alle anderen ausser den 7 erlaubten Platzhaltern [NAME], [FIRMA], [EMAIL], "
    "[TELEFON], [ADRESSE], [ORT], [DATUM]. Wenn du unsicher bist, ob etwas ein Name oder "
    "eine Firma ist, lass es woertlich stehen.\n\nText:\n",
)

# Strikter Volltext-Prompt fuer den 2. Versuch im VOLLTEXT-Modus, wenn der Guard
# die erste Antwort verworfen hat. Identisch zu PROMPT_VOLLTEXT plus Negativliste
# und Klarstellungen (Geschaeftsbereiche/Rollen/Geschaeftsjahre sind keine PII).
PROMPT_VOLLTEXT_STRIKT = PROMPT_VOLLTEXT.replace(
    "\nGib NUR den anonymisierten Text zurueck. Keine Erklaerungen.\n",
    "\nWICHTIG: Diese Tokens sind VERBOTEN: [J1], [J2], [J3], [BETRAG], [UMSATZ], [VERLUST], "
    "[POSITIV], [TEXT], [BERUF], [KMU], UNVERAENDERT, sowie alle anderen ausser den 7 "
    "erlaubten Platzhaltern [NAME], [FIRMA], [EMAIL], [TELEFON], [ADRESSE], [ORT], [DATUM].\n"
    "Geschaeftsbereiche (Vertrieb, Finanzen, Marketing, Einkauf) sind KEINE Firmen. "
    "Unternehmenskategorien (KMU, Startup, Konzern) sind KEINE Firmen. Rollenbezeichnungen "
    "(Beraterin, Geschaeftsfuehrer, Kunde, Berater*innen, Kund*innen) sind KEINE Namen. "
    "Geschaeftsjahre (Jahr 1, J1, 2026) sind KEINE personenbezogenen Daten.\n"
    "Erfinde KEINE neuen Saetze. Fuege KEINE Erklaerungen hinzu. Wenn ein Absatz keine "
    "personenbezogenen Daten enthaelt, gib ihn 1:1 unveraendert zurueck.\n\n"
    "Gib NUR den anonymisierten Text zurueck. Keine Erklaerungen.\n",
)
