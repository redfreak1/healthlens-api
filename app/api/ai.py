from fastapi import APIRouter, HTTPException
from app.models.schemas import AIGenerationRequest, AIGenerationResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/generate", response_model=AIGenerationResponse)
async def generate_ai_content(request: AIGenerationRequest):
    """Generate AI content based on persona and lab results"""
    try:
        # Convert lab results from dict to LabResult objects if needed
        from app.models.schemas import LabResult
        lab_results = []
        for result in request.lab_results:
            if isinstance(result, dict):
                lab_results.append(LabResult(**result))
            else:
                lab_results.append(result)
        
        # Get template for persona
        from app.services.template_service import TemplateService
        template_service = TemplateService()
        template = await template_service.get_template_for_persona(request.persona)
        
        # Generate content
        response = await ai_service.generate_content(
            persona=request.persona,
            lab_results=lab_results,
            template=template,
            user_context=request.user_context
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prompt/{persona_type}")
async def get_ai_prompt_for_persona(persona_type: str):
    """Get AI prompt template for a specific persona"""
    try:
        from app.models.schemas import PersonaType
        from app.services.template_service import TemplateService
        
        persona = PersonaType(persona_type)
        template_service = TemplateService()
        prompt = await template_service.get_ai_prompt_for_persona(persona)
        
        return {"persona": persona_type, "prompt": prompt}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid persona type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))