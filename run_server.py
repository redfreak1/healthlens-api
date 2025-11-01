"""
HealthLens API - Server Startup Script
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
    print("📍 Server URL: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🌐 Proxy: http://tproxy02.qdx.com:9090")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "main:app",
            host="localhost",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())