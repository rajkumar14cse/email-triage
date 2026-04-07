@echo off
REM Email Triage System - Deployment Helper Script (Windows)

setlocal enabledelayedexpansion

echo.
echo 🚀 Email Triage System - Deployment Setup
echo ===========================================
echo.

REM Check for Docker
where docker >nul 2>nul
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH
    echo    Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('docker --version') do set docker_version=%%i
echo ✅ Docker found: %docker_version%

REM Check for Docker Compose
where docker-compose >nul 2>nul
if errorlevel 1 (
    echo ❌ Docker Compose is not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('docker-compose --version') do set compose_version=%%i
echo ✅ Docker Compose found: %compose_version%

REM Check for .env file
if not exist .env (
    echo ⚠️  .env file not found. Creating template...
    (
        echo # Email Triage Environment Variables
        echo HF_TOKEN=your_huggingface_token_here
        echo API_BASE_URL=https://router.huggingface.co/openai/v1
        echo MODEL_NAME=google/flan-t5-large
        echo ENV_URL=http://localhost:8000
        echo PORT=8000
    ) > .env
    echo 📝 Created .env file. Please edit it with your HF_TOKEN
)

REM Menu
echo.
echo Select deployment option:
echo 1. Run locally with Docker Compose (default)
echo 2. Build Docker image only
echo 3. Stop running containers
echo 4. View logs
echo.
set /p choice="Enter choice (1-4, or press Enter for 1): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo 🐳 Starting Docker Compose...
    docker-compose up -d
    echo.
    echo ✅ Deployment complete!
    echo 📍 API available at: http://localhost:8000
    echo 📚 API Docs at: http://localhost:8000/docs
    echo.
    echo Commands:
    echo   View logs: docker-compose logs -f
    echo   Stop: docker-compose down
) else if "%choice%"=="2" (
    echo 🔨 Building Docker image...
    docker build -t email-triage:latest .
    echo ✅ Build complete!
    echo Run with: docker run -p 8000:8000 email-triage:latest
) else if "%choice%"=="3" (
    echo ⏹️  Stopping containers...
    docker-compose down
    echo ✅ Stopped
) else if "%choice%"=="4" (
    docker-compose logs -f
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

echo.
echo 📖 For more deployment options, see DEPLOYMENT.md
pause
