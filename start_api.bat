@echo off
echo Starting Expense Tracker API...
echo.
echo Navigate to project directory...
cd /d "C:\Users\ADMIN\Downloads\expense-tracker-api-main (1)"

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting API server...
echo Server will be available at: http://localhost:5000
echo.
echo Test URLs:
echo   GET  http://localhost:5000/health
echo   GET  http://localhost:5000/
echo   POST http://localhost:5000/api/test
echo.
echo Press Ctrl+C to stop the server
echo.

python minimal_api.py

pause
