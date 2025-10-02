@echo off
echo Stopping Expense Tracker API Docker services...
echo.

docker-compose down

echo.
echo All services stopped!
echo.
echo To remove all data (WARNING: Data loss):
echo docker-compose down -v
echo.
pause
