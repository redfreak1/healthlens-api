"""
HealthLens API - Simple Test Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class SimplePersonaResponse(BaseModel):
    persona: str
    status: str
    message: str

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "status": "success",
        "message": "HealthLens API is working!",
        "timestamp": "2024-10-31T10:30:00Z"
    }

@router.post("/calculate-simple")
async def calculate_persona_simple(data: Dict[str, Any] = None):
    """Simplified persona calculation endpoint for testing"""
    try:
        # Simple logic based on age
        age = data.get("age", 30) if data else 30
        
        if age < 25:
            persona = "tech-savvy"
        elif age < 50:
            persona = "balanced"
        elif age < 65:
            persona = "detail-oriented"
        else:
            persona = "casual"
        
        return SimplePersonaResponse(
            persona=persona,
            status="success",
            message=f"Calculated persona for age {age}"
        )
    except Exception as e:
        return SimplePersonaResponse(
            persona="balanced",
            status="error",
            message=f"Error: {str(e)}"
        )

@router.get("/personas")
async def list_personas():
    """List all available personas"""
    return {
        "personas": [
            "detail-oriented",
            "analytical", 
            "tech-savvy",
            "quick-bold",
            "casual",
            "fast-action",
            "health-conscious",
            "balanced",
            "passive",
            "beginner",
            "intermediate",
            "goal-focused",
            "action-oriented"
        ],
        "count": 13,
        "status": "success"
    }