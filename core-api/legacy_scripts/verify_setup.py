"""
Quick verification script to check if everything is set up correctly.

Run this before starting the API server to ensure all dependencies are installed.
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python version is compatible (3.10+)")
        return True
    else:
        print("❌ Python 3.10 or higher is required")
        return False

def check_virtual_env():
    """Check if running in virtual environment."""
    print_header("Checking Virtual Environment")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print(f"✅ Running in virtual environment: {sys.prefix}")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("   Recommendation: Activate venv with: venv\\Scripts\\activate")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print_header("Checking Dependencies")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pandas',
        'pydantic',
        'openpyxl',
        'numpy',
        'scipy',
        'statsmodels',
        'scikit-learn'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package} - NOT INSTALLED")
    
    print(f"\nInstalled: {len(installed)}/{len(required_packages)}")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required packages are installed")
        return True

def check_database():
    """Check if database exists and is accessible."""
    print_header("Checking Database")
    
    db_path = Path("financial_analysis.db")
    
    if db_path.exists():
        print(f"✅ Database found: {db_path.absolute()}")
        print(f"   Size: {db_path.stat().st_size / 1024:.2f} KB")
        return True
    else:
        print("⚠️  Database not found")
        print("   Initialize with: python src/financial_analysis/database/init_db.py")
        return False

def check_project_structure():
    """Check if project structure is correct."""
    print_header("Checking Project Structure")
    
    required_dirs = [
        'src/financial_analysis',
        'src/financial_analysis/api',
        'src/financial_analysis/services',
        'src/financial_analysis/database',
        'tests',
        'data',
        'logs'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - NOT FOUND")
            all_exist = False
    
    if all_exist:
        print("\n✅ Project structure is correct")
    else:
        print("\n⚠️  Some directories are missing")
    
    return all_exist

def check_api_import():
    """Check if API can be imported."""
    print_header("Checking API Import")
    
    try:
        from src.financial_analysis.api.main import app
        print("✅ API application imported successfully")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ Failed to import API: {e}")
        return False

def check_analysis_service():
    """Check if analysis service can be imported."""
    print_header("Checking Analysis Service")
    
    try:
        from src.financial_analysis.services.analysis_service import AnalysisService
        print("✅ Analysis service imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import analysis service: {e}")
        return False

def run_quick_test():
    """Run a quick database test."""
    print_header("Running Quick Database Test")
    
    try:
        from src.financial_analysis.database.base import SessionLocal
        from src.financial_analysis.database.models import TransactionClassification
        
        db = SessionLocal()
        count = db.query(TransactionClassification).count()
        db.close()
        
        print(f"✅ Database connection successful")
        print(f"   Transaction classifications in database: {count}")
        
        if count == 0:
            print("   ⚠️  No classifications found - database may need initialization")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all verification checks."""
    print("\n" + "🔍 "*20)
    print("  FINANCIAL ANALYSIS - SETUP VERIFICATION")
    print("🔍 "*20)
    
    results = {
        "Python Version": check_python_version(),
        "Virtual Environment": check_virtual_env(),
        "Dependencies": check_dependencies(),
        "Database": check_database(),
        "Project Structure": check_project_structure(),
        "API Import": check_api_import(),
        "Analysis Service": check_analysis_service(),
        "Database Test": run_quick_test()
    }
    
    print_header("Verification Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {check}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "="*80)
        print("  🎉 ALL CHECKS PASSED!")
        print("="*80)
        print("\n✅ Your setup is ready!")
        print("\nNext steps:")
        print("  1. Start the API server:")
        print("     - Windows: start_api.bat")
        print("     - Or: python run_api.py")
        print("  2. Open browser: http://localhost:8000/api/docs")
        print("  3. Run verification tests: python test_analysis_api.py")
    else:
        print("\n" + "="*80)
        print("  ⚠️  SOME CHECKS FAILED")
        print("="*80)
        print("\n❌ Please fix the issues above before starting the server")
        print("\nCommon fixes:")
        print("  - Activate virtual environment: venv\\Scripts\\activate")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Initialize database: python src/financial_analysis/database/init_db.py")
    
    print("\n")

if __name__ == "__main__":
    main()

