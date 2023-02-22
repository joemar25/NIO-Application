@echo off

REM Navigate back to the main folder
cd ..

REM Start Flask server
echo Starting Flask server...
set FLASK_APP=api.py
set FLASK_ENV=development
python api.py
