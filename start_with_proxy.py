"""
HealthLens API - Proxy-Aware Configuration
Startup script configured for corporate proxy environments
"""
import os
import sys
import uvicorn
from pathlib import Path

def setup_proxy_environment():
    """Configure proxy environment variables for corporate network"""
    proxy_url = "http://tproxy02.qdx.com:9090"
    
    # Set environment variables for all HTTP/HTTPS requests
    proxy_env_vars = {
        'HTTP_PROXY': proxy_url,
        'HTTPS_PROXY': proxy_url,
        'http_proxy': proxy_url,
        'https_proxy': proxy_url,
        'no_proxy': 'localhost,127.0.0.1,::1'  # Don't proxy local requests
    }
    
    for var, value in proxy_env_vars.items():
        os.environ[var] = value
        print(f"✅ Set {var}={value}")
    
    print(f"🌐 Corporate proxy configured: {proxy_url}")

def setup_python_path():
    """Add current directory to Python path for imports"""
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
        print(f"✅ Added to Python path: {current_dir}")

def main():
    """Start the HealthLens API server with proxy configuration"""
    print("🚀 Starting HealthLens API with Corporate Proxy Support...")
    print("=" * 60)
    
    # Setup environment
    setup_proxy_environment()
    setup_python_path()
    
    # Server configuration
    host = "localhost"
    port = 8000
    
    print(f"🏥 HealthLens API Configuration:")
    print(f"   📍 Host: {host}")
    print(f"   🔌 Port: {port}")
    print(f"   🌐 Full URL: http://{host}:{port}")
    print(f"   📖 API Docs: http://{host}:{port}/docs")
    print(f"   🔧 Proxy: http://tproxy02.qdx.com:9090")
    print("=" * 60)
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload for development
            access_log=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\n🔧 Troubleshooting Tips:")
        print("   1. Check if port 8000 is available")
        print("   2. Verify proxy connectivity")
        print("   3. Ensure all dependencies are installed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)