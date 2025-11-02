from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import AdaptiveViewRequest, AdaptiveViewResponse
from app.services.cache_service import CacheService
from app.services.data_service import DataService
from app.services.persona_service import PersonaService
from app.services.template_service import TemplateService
from app.services.ai_service import AIService
from app.services.audit_service import AuditService
from app.services.behavior_service import BehaviorService
import time

router = APIRouter()

# Service dependencies
cache_service = CacheService()
data_service = DataService()
persona_service = PersonaService()
template_service = TemplateService()
ai_service = AIService()
audit_service = AuditService()
behavior_service = BehaviorService()

@router.get("/adaptive-view")
async def get_adaptive_view(user_id: str, report_id: str = None):
    """
    Main adaptive view endpoint that implements the sequence diagram flow:
    1. Check cache for existing response
    2. If cache miss: fetch data, determine persona, generate AI content
    3. Cache response and return
    """
    start_time = time.time()
    
    try:
        # Step 1: Check cache
        cache_key = f"{user_id}:{report_id or 'default'}"
        cached_response = await cache_service.get(cache_key)
        
        if cached_response:
            # Log cache hit
            await audit_service.log_interaction(user_id, "adaptive_view", "cache_hit", time.time() - start_time)
            # Update cache_hit flag for cached response
            cached_response['cache_hit'] = True
            return AdaptiveViewResponse(**cached_response)
        
        # Step 2: Cache miss - fetch fresh data
        # Fetch user profile + lab data + history
        user_profile = await data_service.get_user_profile(user_id)
        lab_results = await data_service.get_lab_results(user_id, report_id)
        user_history = await data_service.get_user_history(user_id)
        
        # Step 3: Determine persona
        persona = await persona_service.determine_persona(
            age=user_profile.age,
            history=user_history,
            conditions=user_profile.conditions
        )
        
        print(f"DEBUG: Determined persona: {persona}")

        # Step 4: Select template for persona
        template = await template_service.get_template_for_persona(persona)

        print(f"DEBUG: Selected template: {template}")  # Add this debug line
        
        # Step 5: Call AI service with persona-specific prompt
        ai_content = await ai_service.generate_content(
            persona=persona,
            lab_results=lab_results,
            template=template,
            user_context={
                "age": user_profile.age,
                "conditions": user_profile.conditions,
                "history": user_history
            }
        )
        
        print(f"DEBUG: AI content ui_components: {ai_content.ui_components}")  # Add this debug line
        # Step 6: Structure response with UI components
        response = AdaptiveViewResponse(
            persona=persona,
            ui_components=ai_content.ui_components,
            lab_results=lab_results,
            recommendations=ai_content.recommendations,
            cache_hit=False
        )
        
        # Step 7: Cache response (1 hour TTL)
        await cache_service.set(cache_key, response.dict(), ttl=3600)
        
        # Step 8: Log full interaction
        await audit_service.log_interaction(
            user_id, 
            "adaptive_view", 
            "cache_miss", 
            time.time() - start_time,
            {"persona": persona, "lab_results_count": len(lab_results)}
        )
        
        # Step 9: Send anonymized behavior data
        await behavior_service.track_behavior(
            user_id=user_id,  # Will be anonymized internally
            action="view_adaptive_dashboard",
            persona=persona,
            response_time=time.time() - start_time
        )
        
        return response
        
    except Exception as e:
        await audit_service.log_error(user_id, "adaptive_view", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the orchestrator"""
    return {"status": "healthy", "service": "api_orchestrator"}