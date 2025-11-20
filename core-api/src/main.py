"""Script to run the FastAPI application."""

import uvicorn
from src.financial_analysis.config import settings

if __name__ == "__main__":
    print("="*80)
    print("  Financial Analysis API Server")
    print("="*80)
    print(f"  Environment: {settings.APP_ENV}")
    print(f"  Debug Mode: {settings.DEBUG}")
    print(f"  Host: {settings.API_HOST}")
    print(f"  Port: {settings.API_PORT}")
    print(f"  Database: {settings.DATABASE_URL}")
    print("="*80)
    print(f"\nAPI will be available at:")
    print(f"   - http://localhost:{settings.API_PORT}/api/docs (Swagger UI)")
    print(f"   - http://127.0.0.1:{settings.API_PORT}/api/docs (Swagger UI)")
    print(f"   - http://localhost:{settings.API_PORT}/api/health (Health Check)")
    print(f"\nPress CTRL+C to stop the server\n")
    print("="*80 + "\n")

    try:
        uvicorn.run(
            "src.financial_analysis.api.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower()
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("  Server stopped by user")
        print("="*80)

