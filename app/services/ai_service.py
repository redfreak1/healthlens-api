from app.models.schemas import AIGenerationRequest, AIGenerationResponse, PersonaType, LabResult
from app.services.template_service import TemplateService
from typing import List, Dict, Any
import asyncio

# Try to import config gracefully
try:
    from app.config import settings
    SETTINGS_AVAILABLE = True
except ImportError:
    SETTINGS_AVAILABLE = False
    print("⚠️  Settings not available - using defaults for AI service")

# Try to import httpx gracefully
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("⚠️  HTTPX not available - AI service will use mock responses only")

class AIService:
    def __init__(self):
        self.template_service = TemplateService()
        # Initialize HTTP client with proxy support for external AI calls
        if HTTPX_AVAILABLE and SETTINGS_AVAILABLE:
            try:
                self.client = httpx.AsyncClient(
                    proxies={'http': 'http://tproxy02.qdx.com:9090', 'https': 'http://tproxy02.qdx.com:9090'},
                    timeout=30.0,
                    verify=False  # For corporate environments with custom certificates
                )
            except Exception:
                self.client = None
        else:
            self.client = None
    
    async def generate_content(
        self, 
        persona: PersonaType, 
        lab_results: List[LabResult], 
        template: Dict[str, Any],
        user_context: Dict[str, Any] = None
    ) -> AIGenerationResponse:
        """
        Mock AI service that simulates Vertex AI content generation.
        In production, this would call the actual AI service.
        """
        # Simulate API call delay
        await asyncio.sleep(0.5)
        
        # Analyze lab results
        abnormal_results = [r for r in lab_results if r.status != "normal"]
        normal_count = len(lab_results) - len(abnormal_results)
        
        # Generate persona-specific content
        content = await self._generate_persona_content(persona, lab_results, abnormal_results, user_context)
        
        # Generate UI components based on template
        ui_components = await self.template_service.structure_ui_response(
            persona, content, [r.dict() for r in lab_results]
        )
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(persona, abnormal_results, user_context)
        
        return AIGenerationResponse(
            content=content,
            ui_components=ui_components,
            recommendations=recommendations
        )
    
    async def _generate_persona_content(
        self, 
        persona: PersonaType, 
        lab_results: List[LabResult], 
        abnormal_results: List[LabResult],
        user_context: Dict[str, Any] = None
    ) -> str:
        """Generate content based on persona type"""
        
        if len(abnormal_results) == 0:
            return self._generate_normal_results_content(persona)
        
        if persona == PersonaType.HEALTH_CONSCIOUS:
            # Senior Sue - simple, caring language
            items = []
            for result in abnormal_results:
                direction = "higher" if result.status == "high" else "lower"
                items.append(f"• {result.name}: {direction} than normal")
            
            content = f"You have {len(abnormal_results)} result(s) that need attention:\n\n"
            content += "\n".join(items)
            content += "\n\nPlease discuss these with your doctor."
            return content
            
        elif persona == PersonaType.DETAIL_ORIENTED:
            # Analyst Alex - detailed, technical
            items = []
            for result in abnormal_results:
                ref_range = result.reference_range
                deviation = (result.value - ref_range["max"]) if result.status == "high" else (result.value - ref_range["min"])
                direction = "+" if result.status == "high" else ""
                items.append(
                    f"• {result.name}: {result.value} {result.unit} "
                    f"(Ref: {ref_range['min']}-{ref_range['max']}). "
                    f"Status: {result.status.upper()}. "
                    f"Deviation: {direction}{deviation:.1f} {result.unit}"
                )
            
            content = f"Abnormal findings detected ({len(abnormal_results)} total):\n\n"
            content += "\n".join(items)
            content += "\n\nRecommendation: Clinical correlation advised."
            return content
            
        elif persona == PersonaType.QUICK_BOLD:
            # Quick action focused
            high_priority = [r for r in abnormal_results if r.status == "high"]
            if high_priority:
                content = f"⚠️ {len(high_priority)} values need immediate attention:\n"
                content += "\n".join([f"• {r.name}" for r in high_priority[:3]])
                content += f"\n\n🎯 Next step: Contact your healthcare provider."
            else:
                content = f"📊 {len(abnormal_results)} values are low but monitoring needed.\n"
                content += "🎯 Schedule follow-up in 2-4 weeks."
            return content
            
        elif persona == PersonaType.BEGINNER:
            # Educational, simple language
            content = "Let me explain your results in simple terms:\n\n"
            for result in abnormal_results[:2]:  # Limit to avoid overwhelming
                direction = "higher" if result.status == "high" else "lower"
                content += f"• Your {result.name} is {direction} than the healthy range. "
                content += f"This test measures {self._get_simple_explanation(result.name)}.\n"
            
            if len(abnormal_results) > 2:
                content += f"\n...and {len(abnormal_results) - 2} other values to discuss with your doctor."
            
            content += "\n\nDon't worry - your doctor will help you understand what this means for your health."
            return content
            
        else:
            # Default balanced approach
            content = f"Your lab results show {len(abnormal_results)} values outside the normal range:\n\n"
            for result in abnormal_results:
                direction = "elevated" if result.status == "high" else "below normal"
                content += f"• {result.name} is {direction}\n"
            content += "\nPlease review these results with your healthcare provider."
            return content
    
    async def _generate_normal_results_content(self, persona: PersonaType) -> str:
        """Generate content when all results are normal"""
        if persona == PersonaType.HEALTH_CONSCIOUS:
            return "Good news! All your results are in the healthy range."
        elif persona == PersonaType.DETAIL_ORIENTED:
            return "Analysis complete: All biomarkers are within reference ranges. No abnormal values detected."
        elif persona == PersonaType.QUICK_BOLD:
            return "✅ All clear! Your results look great. Keep up the good work!"
        elif persona == PersonaType.BEGINNER:
            return "Great news! All your test results are healthy. This means your body is working well in the areas we tested."
        else:
            return "All your lab results are within normal ranges. This is a positive indicator of your current health status."
    
    async def _generate_recommendations(
        self, 
        persona: PersonaType, 
        abnormal_results: List[LabResult],
        user_context: Dict[str, Any] = None
    ) -> List[str]:
        """Generate persona-specific recommendations"""
        
        if len(abnormal_results) == 0:
            return [
                "Continue maintaining your current health routine",
                "Schedule regular check-ups as recommended by your doctor",
                "Keep tracking your health metrics"
            ]
        
        recommendations = []
        
        # Common recommendations based on abnormal results
        if any(r.name.lower().contains("glucose") for r in abnormal_results):
            if persona == PersonaType.HEALTH_CONSCIOUS:
                recommendations.append("Monitor your blood sugar levels daily")
                recommendations.append("Follow your diabetes management plan")
            elif persona == PersonaType.QUICK_BOLD:
                recommendations.append("Check glucose 2x daily - track in app")
                recommendations.append("Review carb intake this week")
            else:
                recommendations.append("Consider glucose monitoring")
        
        if any(r.name.lower().contains("cholesterol") for r in abnormal_results):
            recommendations.append("Consider heart-healthy diet modifications")
            recommendations.append("Discuss cholesterol management with your doctor")
        
        if any(r.name.lower().contains("blood") for r in abnormal_results):
            recommendations.append("Follow up with your healthcare provider")
            recommendations.append("Consider additional blood work if recommended")
        
        # Persona-specific additions
        if persona == PersonaType.TECH_SAVVY:
            recommendations.append("Sync results with your health tracking app")
            recommendations.append("Set up automated health monitoring")
        elif persona == PersonaType.DETAIL_ORIENTED:
            recommendations.append("Track trends over time for pattern analysis")
            recommendations.append("Request historical lab data for comparison")
        
        return recommendations[:4]  # Limit to 4 recommendations
    
    def _get_simple_explanation(self, test_name: str) -> str:
        """Get simple explanations for common lab tests"""
        explanations = {
            "glucose": "blood sugar levels",
            "cholesterol": "fat levels in your blood",
            "hemoglobin": "oxygen-carrying protein in your blood",
            "white blood cell": "infection-fighting cells",
            "red blood cell": "oxygen-carrying cells",
            "platelet": "blood clotting cells",
            "creatinine": "kidney function",
            "sodium": "salt levels in your blood",
            "potassium": "an important mineral for heart function"
        }
        
        for key, explanation in explanations.items():
            if key.lower() in test_name.lower():
                return explanation
        
        return "an important health marker"