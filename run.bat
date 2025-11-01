@echo off
echo Starting Indian Election Data Dashboard...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Dashboard will be available at: http://localhost:5000
echo.
python app.py
pause

