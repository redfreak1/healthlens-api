from fastapi import APIRouter, HTTPException
from app.models.schemas import PersonaCalculationRequest, PersonaResult, QuestionnaireResponse, UserProfile
from app.services.persona_service import PersonaService

router = APIRouter()
persona_service = PersonaService()

@router.post("/calculate", response_model=PersonaResult)
async def calculate_persona(request: PersonaCalculationRequest):
    """Calculate user persona based on profile and questionnaire responses"""
    try:
        persona = await persona_service.calculate_persona_from_questionnaire(
            request.user_profile,
            request.questionnaire_responses
        )
        
        # Get persona info for reasoning
        persona_info = persona_service.get_persona_info(persona)
        
        # Ensure persona is properly converted to enum if it's a string
        if isinstance(persona, str):
            from app.models.schemas import PersonaType
            persona = PersonaType(persona)
        
        return PersonaResult(
            persona=persona,
            confidence=0.85,  # Mock confidence score
            reasoning=f"Based on age ({request.user_profile.age}) and responses, determined as {persona_info['name']}"
        )
    except Exception as e:
        print(f"❌ Persona calculation error: {e}")
        # Return a default response instead of raising exception
        from app.models.schemas import PersonaType
        return PersonaResult(
            persona=PersonaType.BALANCED,
            confidence=0.75,
            reasoning=f"Error occurred during calculation, defaulting to balanced persona: {str(e)}"
        )

@router.get("/info/{persona_type}")
async def get_persona_info(persona_type: str):
    """Get detailed information about a specific persona"""
    try:
        from app.models.schemas import PersonaType
        persona = PersonaType(persona_type)
        return persona_service.get_persona_info(persona)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid persona type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/{persona_type}")
async def get_persona_template_preferences(persona_type: str):
    """Get UI template preferences for a persona"""
    try:
        from app.models.schemas import PersonaType
        persona = PersonaType(persona_type)
        return await persona_service.get_ui_template_preferences(persona)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid persona type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))