@echo off
REM restart-docker.bat
REM Wrapper script to call the PowerShell restart script

echo.
echo ================================================================================
echo   Spearmint Docker Compose - Update ^& Restart
echo ================================================================================
echo.

REM Check if PowerShell is available
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell is not available
    echo Please run the PowerShell script directly: .\scripts\restart-docker.ps1
    exit /b 1
)

REM Forward all arguments to PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0restart-docker.ps1" %*

