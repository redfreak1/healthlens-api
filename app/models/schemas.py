from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class PersonaType(str, Enum):
    DETAIL_ORIENTED = "detail-oriented"
    ANALYTICAL = "analytical"
    TECH_SAVVY = "tech-savvy"
    QUICK_BOLD = "quick-bold"
    CASUAL = "casual"
    FAST_ACTION = "fast-action"
    HEALTH_CONSCIOUS = "health-conscious"
    BALANCED = "balanced"
    PASSIVE = "passive"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    GOAL_FOCUSED = "goal-focused"
    ACTION_ORIENTED = "action-oriented"

class LabResultStatus(str, Enum):
    NORMAL = "normal"
    HIGH = "high"
    LOW = "low"

class LabResult(BaseModel):
    name: str
    value: float
    unit: str
    reference_range: Dict[str, float]  # {"min": float, "max": float}
    category: str
    status: LabResultStatus

class UserProfile(BaseModel):
    id: str
    age: int
    gender: str
    conditions: Optional[str] = None
    created_at: Optional[str] = None

class QuestionnaireResponse(BaseModel):
    tracking_style: str
    motivation: str
    time_spent: str
    tech_comfort: str
    dashboard_preference: str

class PersonaCalculationRequest(BaseModel):
    user_profile: UserProfile
    questionnaire_responses: QuestionnaireResponse

class PersonaResult(BaseModel):
    persona: PersonaType
    confidence: float
    reasoning: str

class AdaptiveViewRequest(BaseModel):
    user_id: str
    report_id: Optional[str] = None

class AdaptiveViewResponse(BaseModel):
    persona: PersonaType
    ui_components: Dict[str, Any]
    lab_results: List[LabResult]
    recommendations: List[str]
    cache_hit: bool = False

class AIGenerationRequest(BaseModel):
    persona: PersonaType
    lab_results: List[LabResult]
    template_type: str
    user_context: Optional[Dict[str, Any]] = None

class AIGenerationResponse(BaseModel):
    content: str
    ui_components: Dict[str, Any]
    recommendations: List[str]