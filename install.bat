@echo off
REM Installations-Skript fuer den Anonymisierungs-Agenten (Windows).
REM Legt eine virtuelle Umgebung an, installiert Abhaengigkeiten und erstellt
REM die Arbeitsordner. Mehrfaches Ausfuehren ist unschaedlich.

setlocal
cd /d "%~dp0"

echo ==================================================
echo  Anonymisierungs-Agent - Installation
echo ==================================================

REM 1. Python pruefen
where python >nul 2>nul
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH.
    echo Bitte Python 3.10 oder neuer installieren: https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version') do echo Gefundene Python-Version: %%v

REM 2. Virtuelle Umgebung anlegen (falls noch nicht vorhanden)
if not exist venv (
    echo Lege virtuelle Umgebung an ^(venv^) ...
    python -m venv venv
) else (
    echo Virtuelle Umgebung existiert bereits - wird wiederverwendet.
)

REM 3. Abhaengigkeiten installieren
echo Installiere Abhaengigkeiten ...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo FEHLER: Installation der Abhaengigkeiten fehlgeschlagen.
    exit /b 1
)

REM 4. Arbeitsordner sicherstellen
echo Erstelle Arbeitsordner ...
if not exist input_docs mkdir input_docs
if not exist output_docs mkdir output_docs
if not exist processed mkdir processed
if not exist fehler mkdir fehler

echo.
echo ==================================================
echo  Installation abgeschlossen.
echo ==================================================
echo.
echo Naechste Schritte:
echo   1. LM Studio oeffnen, ein Modell laden und den Local Server starten.
echo   2. Agent starten:
echo        venv\Scripts\activate.bat
echo        python agent.py
echo   3. Dokumente in input_docs\ ablegen, Ergebnisse aus output_docs\ abholen.
echo.
endlocal
