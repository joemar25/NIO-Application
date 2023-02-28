@echo off

echo Mar-Automation...

REM Check if virtual environment exists
if not exist .venv\Scripts\activate.bat (
  echo Creating a new virtual environment...
  python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install required Python packages
echo Installing Python packages...
pip install --upgrade --no-deps -r others/requirements.txt

REM Change directory to the project folder
cd /d "%~dp0..\NIO-APPLICATION\project"

REM Run the postcss command
echo Running npm...
start cmd /c "npm install"

call start.bat
