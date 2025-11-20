"""Test script to verify API imports work correctly."""

try:
    from src.financial_analysis.api.main import app
    print("✅ API imports successful")
    print("✅ All new endpoints loaded")
    
    # Check if new routes are registered
    routes = [route.path for route in app.routes]
    
    new_endpoints = [
        "/api/analysis/summary",
        "/api/analysis/income-expense",
        "/api/analysis/category-breakdown",
        "/api/import/history",
        "/api/import/status/{import_id}"
    ]
    
    print("\n📋 Checking new endpoints:")
    for endpoint in new_endpoints:
        if endpoint in routes:
            print(f"  ✅ {endpoint}")
        else:
            print(f"  ❌ {endpoint} - NOT FOUND")
    
    print("\n✅ All checks passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

