from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.orchestrator import router as orchestrator_router
from app.api.persona import router as persona_router
from app.api.data import router as data_router
from app.api.ai import router as ai_router

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

# Import settings with error handling
try:
    from app.config import settings
    cors_origins = settings.cors_origins
except ImportError:
    # Fallback if settings can't be imported
    cors_origins = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"]

app = FastAPI(
    title="HealthLens API",
    description="Personalized health dashboard API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "HealthLens API",
        "version": "1.0.0",
        "message": "API is running successfully"
    }

@app.get("/")
async def root():
    return {"message": "HealthLens API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}