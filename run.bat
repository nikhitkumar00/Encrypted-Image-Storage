@echo off
setlocal

REM Define your project directory
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM Check if venv directory exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip to avoid issues with older versions
python -m pip install --upgrade pip

REM Install required packages
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found!
)

REM Run the Python script
echo Running application...
python app.py

REM Deactivate the virtual environment
deactivate

REM Pause to see any output
pause
