"""
Simple test script to verify FastAPI installation and proxy configuration
"""
import os

def test_environment():
    print("🧪 Testing HealthLens API Environment")
    print("=" * 50)
    
    # Test Python imports
    try:
        import fastapi
        print(f"✅ FastAPI version: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    try:
        import httpx
        print(f"✅ HTTPX version: {httpx.__version__}")
    except ImportError:
        print("❌ HTTPX not installed")
        return False
    
    # Test proxy configuration
    proxy_url = "http://tproxy02.qdx.com:9090"
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    print(f"✅ Proxy configured: {proxy_url}")
    
    # Test basic FastAPI import
    try:
        from fastapi import FastAPI
        app = FastAPI(title="Test API")
        print("✅ FastAPI app creation successful")
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False
    
    print("=" * 50)
    print("🎉 All tests passed! Environment is ready.")
    print("\n🚀 To start the server manually:")
    print("   cd c:\\vivek\\director\\hackathon\\healthlens-api")
    print("   set HTTP_PROXY=http://tproxy02.qdx.com:9090")
    print("   set HTTPS_PROXY=http://tproxy02.qdx.com:9090")
    print("   python -m uvicorn main:app --host localhost --port 8000 --reload")
    print("\n📖 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    test_environment()