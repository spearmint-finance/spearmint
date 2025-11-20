@echo off
echo ================================================================================
echo   Financial Analysis Tool - Frontend Development Server
echo ================================================================================
echo.
echo Starting Vite development server...
echo.
echo The application will be available at:
echo   - http://localhost:5173
echo   - http://127.0.0.1:5173
echo.
echo API requests will be proxied to:
echo   - http://localhost:8000/api
echo.
echo Press CTRL+C to stop the server
echo.
echo ================================================================================
echo.

npm run dev

echo.
echo ================================================================================
echo   Server stopped
echo ================================================================================
pause

