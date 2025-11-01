from app.models.schemas import PersonaType, UserProfile, QuestionnaireResponse
from typing import Optional, Dict, Any

class PersonaService:
    def __init__(self):
        # Persona determination logic based on age, health history, and responses
        pass
    
    async def determine_persona(
        self, 
        age: int, 
        history: Optional[Dict[str, Any]] = None, 
        conditions: Optional[str] = None,
        questionnaire_responses: Optional[QuestionnaireResponse] = None
    ) -> PersonaType:
        """
        Determine user persona based on age, health history, and questionnaire responses.
        This implements the logic: age:72, history:diabetic → 'senior_sue'
        """
        
        # Age-based persona determination
        if age >= 65:
            # Senior personas
            if conditions and ("diabetes" in conditions.lower() or "diabetic" in conditions.lower()):
                return PersonaType.HEALTH_CONSCIOUS  # "senior_sue" equivalent
            elif questionnaire_responses:
                if questionnaire_responses.tech_comfort == "beginner":
                    return PersonaType.BEGINNER
                elif questionnaire_responses.tracking_style == "detail-oriented":
                    return PersonaType.DETAIL_ORIENTED
            return PersonaType.CASUAL
        
        elif age >= 45:
            # Middle-aged personas
            if conditions:
                return PersonaType.HEALTH_CONSCIOUS
            elif questionnaire_responses:
                if questionnaire_responses.motivation == "goal-focused":
                    return PersonaType.GOAL_FOCUSED
                elif questionnaire_responses.tracking_style == "tech-savvy":
                    return PersonaType.TECH_SAVVY
            return PersonaType.BALANCED
        
        else:
            # Younger personas
            if questionnaire_responses:
                if questionnaire_responses.tracking_style == "quick-bold":
                    return PersonaType.QUICK_BOLD
                elif questionnaire_responses.tracking_style == "detail-oriented":
                    return PersonaType.ANALYTICAL
                elif questionnaire_responses.tech_comfort == "power":
                    return PersonaType.TECH_SAVVY
                elif questionnaire_responses.motivation == "fast-action":
                    return PersonaType.FAST_ACTION
            return PersonaType.INTERMEDIATE
    
    async def calculate_persona_from_questionnaire(
        self, 
        user_profile: UserProfile, 
        responses: QuestionnaireResponse
    ) -> PersonaType:
        """Calculate persona based on questionnaire responses and user profile"""
        return await self.determine_persona(
            age=user_profile.age,
            conditions=user_profile.conditions,
            questionnaire_responses=responses
        )
    
    def get_persona_info(self, persona: PersonaType) -> Dict[str, Any]:
        """Get persona configuration and UI preferences"""
        persona_configs = {
            PersonaType.DETAIL_ORIENTED: {
                "name": "THE ANALYST",
                "category": "Detail-Focused Management",
                "description": "You love diving deep into your health data and tracking every detail",
                "strengths": ["Thorough data analysis", "Consistent tracking", "Pattern recognition"],
                "focus_areas": ["Avoid analysis paralysis", "Set actionable goals"],
                "dashboard_type": "Comprehensive analytics with detailed charts and trends",
                "ui_preferences": {
                    "show_detailed_charts": True,
                    "show_trends": True,
                    "show_raw_data": True,
                    "complexity_level": "high"
                }
            },
            PersonaType.HEALTH_CONSCIOUS: {
                "name": "THE GUARDIAN",
                "category": "Preventive Health Focus",
                "description": "You prioritize managing specific health conditions and prevention",
                "strengths": ["Health awareness", "Preventive mindset", "Medical compliance"],
                "focus_areas": ["Stress management", "Lifestyle balance"],
                "dashboard_type": "Condition-focused dashboard with medical insights",
                "ui_preferences": {
                    "show_medical_context": True,
                    "highlight_abnormal": True,
                    "simple_language": True,
                    "complexity_level": "medium"
                }
            },
            PersonaType.BEGINNER: {
                "name": "THE LEARNER",
                "category": "Simple Health Start",
                "description": "You prefer straightforward, easy-to-understand health information",
                "strengths": ["Willingness to learn", "Appreciation for simplicity", "Step-by-step approach"],
                "focus_areas": ["Building confidence", "Gradual complexity increase"],
                "dashboard_type": "Simplified interface with educational content",
                "ui_preferences": {
                    "simple_language": True,
                    "show_explanations": True,
                    "minimal_complexity": True,
                    "complexity_level": "low"
                }
            },
            PersonaType.TECH_SAVVY: {
                "name": "THE INNOVATOR",
                "category": "Technology-Enhanced Health",
                "description": "You leverage technology and devices to automate your health tracking",
                "strengths": ["Device integration", "Automation", "Tech adoption"],
                "focus_areas": ["Data accuracy validation", "Human touch points"],
                "dashboard_type": "Connected dashboard with device integrations",
                "ui_preferences": {
                    "show_technical_details": True,
                    "enable_integrations": True,
                    "advanced_features": True,
                    "complexity_level": "high"
                }
            },
            PersonaType.QUICK_BOLD: {
                "name": "THE ACHIEVER",
                "category": "Fast-Action Health",
                "description": "You want quick insights and immediate actionable recommendations",
                "strengths": ["Quick decision making", "Goal-oriented", "Action-focused"],
                "focus_areas": ["Patience for long-term trends", "Detailed planning"],
                "dashboard_type": "Streamlined view with key metrics and instant actions",
                "ui_preferences": {
                    "show_summary_only": True,
                    "highlight_actions": True,
                    "minimal_details": True,
                    "complexity_level": "low"
                }
            }
        }
        
        return persona_configs.get(persona, persona_configs[PersonaType.BALANCED])
    
    async def get_ui_template_preferences(self, persona: PersonaType) -> Dict[str, Any]:
        """Get UI template preferences for a specific persona"""
        persona_info = self.get_persona_info(persona)
        return persona_info.get("ui_preferences", {})