@echo off
REM Stops the Kiro screen pet from starting by itself at Windows login.
REM It removes Startup-folder shortcuts that launch kiro_pet.py / "Kiro Pet.bat",
REM so the pet only starts when you pick it in the KiroPet extension
REM (click the paw in the status bar, or "KiroPet: Choose pet").
REM RanakPet and everything else in the Startup folder is left alone.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$dirs = @([Environment]::GetFolderPath('Startup'), [Environment]::GetFolderPath('CommonStartup'));" ^
  "$sh = New-Object -ComObject WScript.Shell; $n = 0;" ^
  "foreach ($d in $dirs) { Get-ChildItem -Path $d -File -ErrorAction SilentlyContinue | ForEach-Object {" ^
  "  $t = $_.Name; if ($_.Extension -eq '.lnk') { $l = $sh.CreateShortcut($_.FullName); $t = $t + ' ' + $l.TargetPath + ' ' + $l.Arguments };" ^
  "  if ($t -match 'kiro_pet|Kiro Pet') { Write-Host ('Removing ' + $_.FullName); Remove-Item -LiteralPath $_.FullName; $n++ } } };" ^
  "if ($n -eq 0) { Write-Host 'No KiroPet startup item found. If the pet still starts by itself, check Task Scheduler for a Kiro Pet task.' } else { Write-Host ('Done - removed ' + $n + ' startup item(s).') }"
pause
