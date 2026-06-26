#!/usr/bin/env bash
# Installations-Skript fuer den Anonymisierungs-Agenten (macOS / Linux).
# Legt eine virtuelle Umgebung an, installiert Abhaengigkeiten und erstellt
# die Arbeitsordner. Mehrfaches Ausfuehren ist unschaedlich.

set -euo pipefail

cd "$(dirname "$0")"

echo "=================================================="
echo " Anonymisierungs-Agent - Installation"
echo "=================================================="

# 1. Python pruefen
if ! command -v python3 >/dev/null 2>&1; then
    echo "FEHLER: python3 ist nicht installiert."
    echo "Bitte Python 3.10 oder neuer installieren: https://www.python.org/downloads/"
    exit 1
fi

PY_VERSION="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
echo "Gefundene Python-Version: $PY_VERSION"

REQUIRED_MAJOR=3
REQUIRED_MINOR=10
ACTUAL_MAJOR="$(python3 -c 'import sys; print(sys.version_info[0])')"
ACTUAL_MINOR="$(python3 -c 'import sys; print(sys.version_info[1])')"
if [ "$ACTUAL_MAJOR" -lt "$REQUIRED_MAJOR" ] || \
   { [ "$ACTUAL_MAJOR" -eq "$REQUIRED_MAJOR" ] && [ "$ACTUAL_MINOR" -lt "$REQUIRED_MINOR" ]; }; then
    echo "FEHLER: Python ${REQUIRED_MAJOR}.${REQUIRED_MINOR} oder neuer wird benoetigt."
    exit 1
fi

# 2. Virtuelle Umgebung anlegen (falls noch nicht vorhanden)
if [ ! -d "venv" ]; then
    echo "Lege virtuelle Umgebung an (venv/) ..."
    python3 -m venv venv
else
    echo "Virtuelle Umgebung existiert bereits - wird wiederverwendet."
fi

# 3. Abhaengigkeiten installieren
echo "Installiere Abhaengigkeiten ..."
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

# 4. Arbeitsordner sicherstellen
echo "Erstelle Arbeitsordner ..."
mkdir -p input_docs output_docs processed fehler

echo ""
echo "=================================================="
echo " Installation abgeschlossen."
echo "=================================================="
echo ""
echo "Naechste Schritte:"
echo "  1. LM Studio oeffnen, ein Modell laden und den Local Server starten."
echo "  2. Agent starten:"
echo "       source venv/bin/activate"
echo "       python3 agent.py"
echo "  3. Dokumente in input_docs/ ablegen, Ergebnisse aus output_docs/ abholen."
echo ""
