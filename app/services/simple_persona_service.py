"""
Simple Persona Service - Fixed version without enum serialization issues
"""
from typing import Dict, Any

class SimplePersonaService:
    """Simple persona service that returns clean string responses"""
    
    def get_persona_info(self, persona_type: str) -> Dict[str, Any]:
        """Get persona information by string type"""
        
        # Complete persona configurations
        persona_configs = {
            "detail-oriented": {
                "name": "The Analyst",
                "category": "Detail-Focused Management", 
                "description": "You love diving deep into your health data and tracking every detail",
                "strengths": ["Thorough data analysis", "Consistent tracking", "Pattern recognition"],
                "focus_areas": ["Avoid analysis paralysis", "Set actionable goals"]
            },
            "analytical": {
                "name": "The Data Scientist",
                "category": "Analytics-Driven Health",
                "description": "You use analytical thinking and data science approaches to health",
                "strengths": ["Statistical analysis", "Hypothesis testing", "Pattern recognition"],
                "focus_areas": ["Actionable insights", "Practical implementation"]
            },
            "tech-savvy": {
                "name": "The Tech Expert", 
                "category": "Technology-Focused Health",
                "description": "You leverage technology and data for optimal health management",
                "strengths": ["Tech integration", "Data optimization", "Innovation adoption"],
                "focus_areas": ["Balancing tech with human needs", "Avoiding over-optimization"]
            },
            "quick-bold": {
                "name": "The Quick Decision Maker",
                "category": "Fast Decision Health",
                "description": "You make quick, bold decisions about your health and wellness",
                "strengths": ["Quick decision making", "Bold choices", "Risk-taking"],
                "focus_areas": ["Thoughtful consideration", "Long-term planning"]
            },
            "casual": {
                "name": "The Casual User",
                "category": "Simple Health Tracking", 
                "description": "You prefer simple, easy-to-understand health information",
                "strengths": ["Simplicity", "Low stress", "Easy adoption"],
                "focus_areas": ["Building consistency", "Gradual improvement"]
            },
            "fast-action": {
                "name": "The Quick Responder",
                "category": "Fast-Action Health",
                "description": "You want quick insights and immediate actionable recommendations",
                "strengths": ["Quick decision making", "Goal-oriented", "Action-focused"],
                "focus_areas": ["Patience for long-term trends", "Detailed planning"]
            },
            "health-conscious": {
                "name": "The Guardian", 
                "category": "Preventive Health Focus",
                "description": "You prioritize managing specific health conditions and prevention",
                "strengths": ["Health awareness", "Preventive mindset", "Medical compliance"],
                "focus_areas": ["Stress management", "Lifestyle balance"]
            },
            "balanced": {
                "name": "The Balanced User",
                "category": "Balanced Health Management",
                "description": "You take a moderate approach to health management",
                "strengths": ["Balanced perspective", "Consistent habits", "Realistic goals"],
                "focus_areas": ["Maintaining consistency", "Building healthy routines"]
            },
            "passive": {
                "name": "The Observer",
                "category": "Passive Health Monitoring", 
                "description": "You prefer to monitor your health data without active intervention",
                "strengths": ["Patient observation", "Stress-free approach", "Long-term perspective"],
                "focus_areas": ["Taking action when needed", "Setting gentle goals"]
            },
            "beginner": {
                "name": "The Newcomer",
                "category": "Health Journey Starter",
                "description": "You're new to health tracking and want guidance and support",
                "strengths": ["Openness to learning", "Fresh perspective", "Motivation"],
                "focus_areas": ["Building habits", "Understanding basics"]
            },
            "intermediate": {
                "name": "The Progressor",
                "category": "Intermediate Health Management",
                "description": "You have some experience with health tracking and want to advance",
                "strengths": ["Growing knowledge", "Established habits", "Motivation to improve"],
                "focus_areas": ["Advanced strategies", "Optimization techniques"]
            },
            "goal-focused": {
                "name": "The Achiever", 
                "category": "Goal-Oriented Health",
                "description": "You set specific health goals and work systematically to achieve them",
                "strengths": ["Goal setting", "Systematic approach", "Persistence"],
                "focus_areas": ["Flexibility", "Enjoying the journey"]
            },
            "action-oriented": {
                "name": "The Doer",
                "category": "Action-Based Health",
                "description": "You prefer taking immediate action on health insights and recommendations",
                "strengths": ["Quick implementation", "Results-driven", "Proactive"],
                "focus_areas": ["Strategic thinking", "Long-term planning"]
            }
        }
        
        # Get persona config or return default
        if persona_type in persona_configs:
            config = persona_configs[persona_type]
            config["persona_id"] = persona_type
            return config
        else:
            # Return a generic config for unknown personas
            return {
                "persona_id": persona_type,
                "name": f"The {persona_type.title().replace('-', ' ')} User",
                "category": f"{persona_type.title().replace('-', ' ')} Health Management",
                "description": f"You have a {persona_type.replace('-', ' ')} approach to health management",
                "strengths": ["Personalized approach", "Unique perspective"],
                "focus_areas": ["Finding your optimal health strategy"]
            }
    
    def calculate_simple_persona(self, age: int = 30, tech_comfort: str = "intermediate") -> str:
        """Simple persona calculation based on age and tech comfort"""
        
        if age < 25:
            if tech_comfort == "high":
                return "tech-savvy"
            else:
                return "casual"
        elif age < 35:
            if tech_comfort == "high":
                return "analytical"
            else:
                return "balanced"
        elif age < 50:
            if tech_comfort == "low":
                return "casual"
            else:
                return "detail-oriented"
        elif age < 65:
            return "health-conscious"
        else:
            if tech_comfort == "low":
                return "passive"
            else:
                return "beginner"