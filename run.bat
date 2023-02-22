@echo off

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

REM Check if required Node packages are already installed
echo Checking if required Node packages are already installed...
IF NOT EXIST "node_modules\autoprefixer" (
  echo Installing autoprefixer...
  npm install -D autoprefixer
)

IF NOT EXIST "node_modules\browserify" (
  echo Installing browserify...
  npm i browserify
)

IF NOT EXIST "node_modules\postcss-cli" (
  echo Installing postcss-cli...
  npm install -D postcss-cli
)

IF NOT EXIST "node_modules\tailwindcss" (
  echo Installing tailwindcss...
  npm install -D tailwindcss
)

REM Run the postcss command
echo Running postcss...
start cmd /c "npm run postcss"

REM Run the browserify command
echo Running browserify...
start cmd /c "npm run bfy"

call start.bat
