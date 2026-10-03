@echo off
REM Start the Kiro screen pet by hand (it walks around the Kiro window).
REM Usually you don't need this: pick "Screen pet" from the paw in Kiro's
REM status bar and the ThaiDevPet extension starts and stops it for you.
REM Extra options, e.g.:  "Kiro Pet.bat" --style pixel --mascot lunar
start "" "C:\Users\wangyun\AppData\Local\Programs\Python\Python313\pythonw.exe" "%~dp0kiro_pet.py" %*
