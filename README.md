# HealthLens API

A FastAPI-based backend service for the HealthLens personalized health dashboard application.

## Architecture

This API implements the following services as shown in the system architecture:

- **API Orchestrator**: Main endpoint handler and service coordinator
- **Persona Service**: Determines user personas based on profile and questionnaire data
- **Data Services**: Manages user profiles, lab data, and health history
- **Template Engine**: Selects and structures UI templates based on persona
- **Cache Service**: Redis-based caching for performance
- **AI Service**: Integration with AI services for content generation
- **Audit Ledger**: Logging and interaction tracking
- **Behavior Service**: Anonymized behavior data collection

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the development server:
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

- `GET /adaptive-view?user_id={id}&report_id={id}` - Main adaptive UI endpoint
- `POST /persona/calculate` - Calculate user persona
- `GET /data/profile/{user_id}` - Get user profile
- `GET /data/lab-results/{user_id}` - Get lab results
- `POST /ai/generate` - Generate AI content

## Environment Variables

- `REDIS_URL`: Redis connection URL
- `DATABASE_URL`: Database connection URL
- `AI_SERVICE_URL`: AI service endpoint
- `CORS_ORIGINS`: Allowed CORS origins