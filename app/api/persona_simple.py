"""
Simple Persona Router - Clean implementation without enum issues
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
sys.path.append('.')

from app.services.simple_persona_service import SimplePersonaService

router = APIRouter(prefix="/api/v1/persona-simple", tags=["persona-simple"])

# Initialize the simple persona service
persona_service = SimplePersonaService()

class PersonaCalculationRequest(BaseModel):
    age: Optional[int] = 30
    tech_comfort: Optional[str] = "intermediate"

@router.get("/info/{persona_type}")
async def get_persona_info(persona_type: str) -> Dict[str, Any]:
    """Get persona information by persona type"""
    try:
        info = persona_service.get_persona_info(persona_type)
        return {
            "success": True,
            "data": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate")
async def calculate_persona(request: PersonaCalculationRequest) -> Dict[str, Any]:
    """Calculate persona based on user inputs"""
    try:
        persona_type = persona_service.calculate_simple_persona(
            age=request.age,
            tech_comfort=request.tech_comfort
        )
        
        persona_info = persona_service.get_persona_info(persona_type)
        
        return {
            "success": True,
            "data": {
                "calculated_persona": persona_type,
                "persona_info": persona_info
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types")
async def get_available_persona_types() -> Dict[str, Any]:
    """Get list of all available persona types"""
    try:
        persona_types = [
            "detail-oriented", "analytical", "tech-savvy", "quick-bold",
            "casual", "fast-action", "health-conscious", "balanced",
            "passive", "beginner", "intermediate", "goal-focused", "action-oriented"
        ]
        
        return {
            "success": True,
            "data": {
                "persona_types": persona_types,
                "count": len(persona_types)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def persona_health_check() -> Dict[str, Any]:
    """Health check for persona service"""
    return {
        "success": True,
        "data": {
            "service": "Simple Persona Service",
            "status": "healthy",
            "version": "1.0"
        }
    }