"""
HealthLens API - Diagnostic and Restart Script
"""
import os
import sys
import uvicorn
from pathlib import Path

def diagnose_and_start():
    # Set working directory
    os.chdir(Path(__file__).parent)
    
    # Set proxy environment variables
    os.environ['HTTP_PROXY'] = 'http://tproxy02.qdx.com:9090'
    os.environ['HTTPS_PROXY'] = 'http://tproxy02.qdx.com:9090'
    os.environ['no_proxy'] = 'localhost,127.0.0.1'
    
    print("🔍 HealthLens API Diagnostics")
    print("=" * 50)
    
    # Test imports
    try:
        from main import app
        print("✅ Main app imports successfully")
        print(f"✅ App title: {app.title}")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return 1
    
    # Test FastAPI
    try:
        import fastapi
        print(f"✅ FastAPI version: {fastapi.__version__}")
    except Exception as e:
        print(f"❌ FastAPI import failed: {e}")
        return 1
    
    print("\n🚀 Starting server with error handling...")
    print("📍 URL: http://localhost:5000")
    print("📖 Docs: http://localhost:5000/docs")
    print("🔍 Health: http://localhost:5000/health")
    print("🧪 Test: http://localhost:5000/api/v1/test/test")
    print("=" * 50)
    
    try:
        # Start with detailed logging
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=5000,
            reload=True,
            log_level="debug",  # More detailed logging
            access_log=True,
            reload_includes=["*.py"],
            reload_excludes=["*.pyc", "__pycache__"]
        )
    except PermissionError:
        print("❌ Permission denied on port 5000, trying 5173...")
        try:
            uvicorn.run(
                "main:app",
                host="127.0.0.1", 
                port=5173,
                reload=True,
                log_level="debug"
            )
        except Exception as e:
            print(f"❌ Failed on port 5173: {e}")
            return 1
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(diagnose_and_start())