FLY INVASION - STANDALONE WINDOWS EXE BUILD

This ZIP contains the Windows desktop overlay source and two build methods.
The ZIP does NOT already contain an EXE.

Option A: Build on a Windows PC with Python installed (only builder needs Python):
  Double-click build_exe.bat
  The standalone program appears at dist\FlyInvasion.exe.
  Copy the EXE to any Windows 10/11 PC; Python is not needed to run it.

Option B: Build using GitHub Actions (no local Python needed):
  1. Create a GitHub repository and upload these files, preserving .github/workflows/.
  2. Open Actions > Build Windows EXE > Run workflow.
  3. After the workflow finishes, download the FlyInvasion-Windows-EXE artifact.
  4. Unzip it to get FlyInvasion.exe.

Use Ctrl+Shift+Q to quit. The prank only animates copies of icons and never
moves or deletes actual desktop items or Recycle Bin contents.

Note: This prototype has not been tested on Windows in this environment.
