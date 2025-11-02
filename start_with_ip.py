#!/usr/bin/env python3
"""
Startup script for HealthLens API with automatic IP detection
"""
import uvicorn
import sys
import os
import socket

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # Fallback to localhost if can't determine IP
        return "127.0.0.1"

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Get local IP address
    host_ip = get_local_ip()
    port = 4192  # Changed to 8080 to avoid permission issues
    
    print("🚀 HealthLens API Server Starting with DEBUG MODE...")
    print("=" * 60)
    print(f"📍 Server URL: http://{host_ip}:{port}")
    print(f"📖 API Documentation: http://{host_ip}:{port}/docs")
    print(f"🔗 Interactive API: http://{host_ip}:{port}/redoc")
    print(f"💻 Local IP: {host_ip}")
    print(f"🐛 Debug Mode: ENABLED")
    print(f"📋 Log Level: DEBUG")
    print(f"🔄 Auto-reload: ENABLED")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",  # Listen on all interfaces
            port=port,
            reload=True,
            log_level="debug",  # Enable debug logging
            access_log=True,    # Show access logs
            use_colors=True     # Enable colored output
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)