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
            },
            PersonaType.BALANCED: {
                "name": "THE BALANCED USER",
                "category": "Balanced Health Management",
                "description": "You take a moderate approach to health management, balancing detail with simplicity",
                "strengths": ["Practical decisions", "Balanced information needs", "Flexible approach"],
                "focus_areas": ["Maintain consistency", "Find sustainable habits"],
                "dashboard_type": "Balanced view with moderate detail and clear summaries",
                "ui_preferences": {
                    "show_detailed_charts": True,
                    "show_trends": True,
                    "show_raw_data": False,
                    "complexity_level": "medium",
                    "show_medical_context": True,
                    "highlight_abnormal": True,
                    "simple_language": False
                }
            },
            PersonaType.GOAL_FOCUSED: {
                "name": "THE GOAL SETTER",
                "category": "Goal-Oriented Health",
                "description": "You are motivated by setting and achieving specific health goals",
                "strengths": ["Target achievement", "Motivation", "Progress tracking"],
                "focus_areas": ["Realistic goal setting", "Long-term sustainability"],
                "dashboard_type": "Goal-focused dashboard with progress tracking",
                "ui_preferences": {
                    "show_progress_bars": True,
                    "highlight_goals": True,
                    "show_achievements": True,
                    "complexity_level": "medium"
                }
            },
            PersonaType.ANALYTICAL: {
                "name": "THE ANALYST",
                "category": "Data-Driven Health",
                "description": "You prefer detailed analysis and comprehensive data views",
                "strengths": ["Data interpretation", "Pattern recognition", "Thorough analysis"],
                "focus_areas": ["Actionable insights", "Avoiding analysis paralysis"],
                "dashboard_type": "Analytics-heavy dashboard with detailed charts and trends",
                "ui_preferences": {
                    "show_detailed_charts": True,
                    "show_trends": True,
                    "show_raw_data": True,
                    "complexity_level": "high",
                    "show_correlations": True
                }
            },
            PersonaType.FAST_ACTION: {
                "name": "THE EXECUTOR",
                "category": "Immediate Action Health",
                "description": "You prefer quick, actionable health insights with immediate next steps",
                "strengths": ["Quick implementation", "Action orientation", "Decisiveness"],
                "focus_areas": ["Comprehensive planning", "Long-term thinking"],
                "dashboard_type": "Action-focused dashboard with immediate recommendations",
                "ui_preferences": {
                    "show_action_items": True,
                    "highlight_urgent": True,
                    "minimal_analysis": True,
                    "complexity_level": "low"
                }
            },
            PersonaType.INTERMEDIATE: {
                "name": "THE STEADY TRACKER",
                "category": "Consistent Health Management",
                "description": "You maintain steady engagement with moderate detail preferences",
                "strengths": ["Consistency", "Steady progress", "Balanced approach"],
                "focus_areas": ["Avoiding monotony", "Finding motivation"],
                "dashboard_type": "Standard dashboard with consistent features",
                "ui_preferences": {
                    "show_trends": True,
                    "moderate_detail": True,
                    "consistent_layout": True,
                    "complexity_level": "medium"
                }
            },
            PersonaType.CASUAL: {
                "name": "THE CASUAL USER",
                "category": "Low-Maintenance Health",
                "description": "You prefer simple, low-effort health tracking with minimal complexity",
                "strengths": ["Simplicity", "Low maintenance", "Easy adoption"],
                "focus_areas": ["Staying engaged", "Finding value in simplicity"],
                "dashboard_type": "Simple dashboard with essential information only",
                "ui_preferences": {
                    "simple_language": True,
                    "minimal_features": True,
                    "easy_navigation": True,
                    "complexity_level": "low"
                }
            },
            PersonaType.PASSIVE: {
                "name": "THE OBSERVER",
                "category": "Passive Health Monitoring",
                "description": "You prefer automated tracking with minimal active engagement",
                "strengths": ["Automated data collection", "Background monitoring", "Low effort"],
                "focus_areas": ["Relevant notifications", "When to take action"],
                "dashboard_type": "Automated dashboard with smart alerts and summaries",
                "ui_preferences": {
                    "automated_insights": True,
                    "minimal_interaction": True,
                    "smart_alerts": True,
                    "complexity_level": "low"
                }
            }
        }
        
        return persona_configs.get(persona, persona_configs[PersonaType.BALANCED])
    
    async def get_ui_template_preferences(self, persona: PersonaType) -> Dict[str, Any]:
        """Get UI template preferences for a specific persona"""
        persona_info = self.get_persona_info(persona)
        return persona_info.get("ui_preferences", {})