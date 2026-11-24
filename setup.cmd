@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "SCRIPT=%~dp0scripts\setup.py"

where py >nul 2>&1
if not errorlevel 1 goto run_py

where python >nul 2>&1
if not errorlevel 1 goto run_python

echo DevWorkbench setup needs Python 3. Install Python from https://www.python.org/downloads/ and run setup.cmd again. 1>&2
exit /b 1

:run_py
py -3 "%SCRIPT%" %*
exit /b %ERRORLEVEL%

:run_python
python "%SCRIPT%" %*
exit /b %ERRORLEVEL%
