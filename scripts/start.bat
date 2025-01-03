@echo off

:: Move out of 'scripts' directory if executed from there
for %%I in ("%~dp0.") do set "SCRIPT_DIR=%%~fI"
for %%I in ("%SCRIPT_DIR%") do set "PARENT_DIR=%%~dpI"
for %%I in ("%SCRIPT_DIR%") do set "CURRENT_DIR_NAME=%%~nI"

if /i "%CURRENT_DIR_NAME%"=="scripts" (
    cd /d "%PARENT_DIR%"
    echo Moved out of 'scripts' directory to %cd%
)

:: Create virtual environment if not exists
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
)

:: Activate virtual environment
call venv\Scripts\activate
echo Virtual environment activated.

:: Install requirements
if exist "requirements.txt" (
    pip install --upgrade pip
    pip install -r requirements.txt
    echo Dependencies installed.
)

jupyter notebook fornagiel_miklas_projekt.ipynb
