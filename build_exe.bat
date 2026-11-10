@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
 echo Python is required only on the computer building the EXE.
 echo Alternatively use the included GitHub Actions workflow.
 pause
 exit /b 1
)
py -m pip install --upgrade pyinstaller
if errorlevel 1 exit /b 1
py -m PyInstaller --noconfirm --clean --onefile --windowed --name FlyInvasion fly_prank.py
if errorlevel 1 exit /b 1
echo Built: dist\FlyInvasion.exe
pause
