@echo off
REM Start the FastAPI backend server

echo.
echo ========================================
echo   Starting Spearmint API Server
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [WARNING] Virtual environment not detected
    echo Attempting to activate .venv...
    
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    ) else (
        echo [ERROR] Virtual environment not found at .venv
        echo Please create it with: python -m venv .venv
        echo Then activate it with: .venv\Scripts\activate
        pause
        exit /b 1
    )
)

echo [OK] Virtual environment activated
echo.

REM Set PYTHONPATH to include core-api directory
set PYTHONPATH=%CD%\core-api;%PYTHONPATH%

REM Navigate to core-api directory
cd core-api

REM Start the API server with uvicorn
echo Starting API server...
echo.
uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000 --reload

REM Return to root directory
cd ..

