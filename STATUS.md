# HealthLens API - Simple Demo Version

This is a simplified demo version that runs without external dependencies.

## Features Implemented:
- All microservices architecture
- Persona-based logic
- Mock data integration  
- Complete API endpoints

## To run with full dependencies:
1. Install Python packages: `pip install fastapi uvicorn redis pydantic python-dotenv`
2. Run: `python start.py`

## Current Status:
- ✅ Complete FastAPI backend structure
- ✅ All microservices implemented
- ✅ React frontend updated to use API
- ⏳ Package installation pending (SSL certificate issue)

## API Endpoints:
- `GET /health` - Health check
- `POST /api/adaptive-view` - Get personalized view
- `POST /api/persona/calculate` - Calculate user persona
- `GET /api/persona/{persona_id}` - Get persona details
- `GET /api/data/health-summary/{user_id}` - Health summary
- `GET /api/data/lab-results/{user_id}` - Lab results
- `GET /api/data/medications/{user_id}` - Medications
- `POST /api/ai/generate-content` - AI content generation

## Architecture:
The backend follows a microservices pattern with:
- Orchestrator Service (main coordinator)
- Persona Service (user profiling)
- Data Service (health data)
- Template Engine (UI generation)
- AI Service (content generation)
- Cache Service (Redis caching)
- Audit Service (interaction logging)
- Behavior Service (user tracking)

## Frontend Integration:
The React app has been updated with:
- API client library (`src/lib/api.ts`)
- React Query hooks (`src/lib/useApi.ts`)
- Environment configuration
- Real API calls with mock fallback

The AIQuerySection component now calls the real API instead of using mock data.