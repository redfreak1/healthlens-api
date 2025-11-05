from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.orchestrator import router as orchestrator_router
from app.api.persona import router as persona_router
from app.api.data import router as data_router
from app.api.ai import router as ai_router

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import test router for debugging
try:
    from app.api.test import router as test_router
    TEST_ROUTER_AVAILABLE = True
except ImportError:
    TEST_ROUTER_AVAILABLE = False

# Import fixed persona router
try:
    from app.api.persona_fixed import router as persona_fixed_router
    PERSONA_FIXED_AVAILABLE = True
except ImportError:
    PERSONA_FIXED_AVAILABLE = False

# Import simple persona router
try:
    from app.api.persona_simple import router as persona_simple_router
    PERSONA_SIMPLE_AVAILABLE = True
except ImportError:
    PERSONA_SIMPLE_AVAILABLE = False

# Import Gemini test router
try:
    from app.api.gemini_test import router as gemini_test_router
    GEMINI_TEST_AVAILABLE = True
except ImportError:
    GEMINI_TEST_AVAILABLE = False

# Import settings with error handling
try:
    from app.config import settings
    cors_origins = settings.cors_origins
    # Ensure localhost:8080 is included
    if "http://localhost:8080" not in cors_origins:
        cors_origins.append("http://localhost:8080")
except ImportError:
    # Fallback if settings can't be imported
    cors_origins = [
        "http://localhost:8080",  # Frontend origin causing CORS issue
        "http://localhost:5173", 
        "http://localhost:3000", 
        "https://localhost:3000",
        "https://localhost:5173",
        "https://healthlens-ui-main-320501699885.us-central1.run.app",  # Production frontend
        "http://10.44.215.180:4192"
    ]

# Add production frontend URL to existing cors_origins if it exists
if cors_origins and "https://healthlens-ui-main-320501699885.us-central1.run.app" not in cors_origins:
    cors_origins.append("https://healthlens-ui-main-320501699885.us-central1.run.app")

app = FastAPI(
    title="HealthLens API",
    description="Personalized health dashboard API",
    version="1.0.0"
)

# CORS middleware - Updated to ensure production frontend is included
print(f"🔧 CORS Origins: {cors_origins}")  # Debug info
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight for 24 hours
)

# Include routers
app.include_router(orchestrator_router, prefix="/api/v1")
app.include_router(persona_router, prefix="/api/v1/persona")
app.include_router(data_router, prefix="/api/v1/data")
app.include_router(ai_router, prefix="/api/v1/ai")

# Include test router if available
if TEST_ROUTER_AVAILABLE:
    app.include_router(test_router, prefix="/api/v1/test")

# Include fixed persona router if available
if PERSONA_FIXED_AVAILABLE:
    app.include_router(persona_fixed_router, prefix="/api/v1/persona-fixed")

# Include simple persona router if available
if PERSONA_SIMPLE_AVAILABLE:
    app.include_router(persona_simple_router, prefix="/api/v1/persona-simple")

# Include Gemini test router if available
if GEMINI_TEST_AVAILABLE:
    app.include_router(gemini_test_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "HealthLens API",
        "version": "1.0.0",
        "message": "API is running successfully",
        "cors_origins": cors_origins  # Debug info
    }

@app.get("/")
async def root():
    return {"message": "HealthLens API", "version": "1.0.0"}