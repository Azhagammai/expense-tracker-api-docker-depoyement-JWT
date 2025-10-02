@echo off
echo Starting Expense Tracker API with Docker...
echo.

echo Building and starting all services...
docker-compose up --build -d

echo.
echo Services starting...
echo - API: http://localhost:5000
echo - MongoDB: localhost:27017
echo - Nginx: http://localhost:80
echo.

echo Waiting for services to be ready...
timeout /t 10 /nobreak > nul

echo.
echo Testing API health...
curl -s http://localhost:5000/health

echo.
echo.
echo Docker services are running!
echo.
echo To view logs: docker-compose logs -f
echo To stop services: docker-compose down
echo To scale API: docker-compose up -d --scale api=3
echo.
pause
