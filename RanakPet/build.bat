@echo off
REM ---------------------------------------------------------------------------
REM Build RanakPet.exe (single-file, no console). Output: dist\RanakPet.exe
REM Requires: Python 3.13 with pyinstaller + pillow installed:
REM     pip install pyinstaller pillow
REM ---------------------------------------------------------------------------
setlocal
set PY="C:\Users\wangyun\AppData\Local\Programs\Python\Python313\python.exe"
if not exist %PY% set PY=python

REM (re)generate the Lunar-head icon
%PY% make_icon.py

REM bundle to a single exe; --add-data ships the .ico for the runtime window icon
%PY% -m PyInstaller --onefile --noconsole --name RanakPet ^
    --icon ranak.ico --add-data "ranak.ico;." --clean --noconfirm ranak_pet.py

echo.
echo Done. Send this file to others:  dist\RanakPet.exe
endlocal
