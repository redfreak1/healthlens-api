"""
HealthLens API - Corporate Environment Server Startup
Uses port 5000 to avoid Windows permission issues
"""
import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Set working directory
    os.chdir(Path(__file__).parent)
    
    # Set proxy environment variables
    os.environ['HTTP_PROXY'] = 'http://tproxy02.qdx.com:9090'
    os.environ['HTTPS_PROXY'] = 'http://tproxy02.qdx.com:9090'
    os.environ['no_proxy'] = 'localhost,127.0.0.1'
    
    print("🚀 HealthLens API Server Starting...")
    print("=" * 50)
    print("📍 Server URL: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000/docs")
    print("🔍 Health Check: http://localhost:5000/health")
    print("🌐 Proxy: http://tproxy02.qdx.com:9090")
    print("💡 Using port 5000 for corporate environment compatibility")
    print("=" * 50)
    
    try:
        # Start the FastAPI server on port 5000
        uvicorn.run(
            "main:app",
            host="127.0.0.1",  # Use 127.0.0.1 instead of localhost for better compatibility
            port=5000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except PermissionError as e:
        print(f"❌ Permission denied on port 5000: {e}")
        print("💡 Trying alternative port 5173...")
        try:
            uvicorn.run(
                "main:app",
                host="127.0.0.1",
                port=5173,
                reload=True,
                log_level="info"
            )
        except Exception as e2:
            print(f"❌ Alternative port also failed: {e2}")
            return 1
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("\n🔧 Troubleshooting suggestions:")
        print("   1. Run PowerShell as Administrator")
        print("   2. Check Windows Firewall settings")
        print("   3. Try different ports (3000, 8080, 8888)")
        print("   4. Contact IT for port access permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())