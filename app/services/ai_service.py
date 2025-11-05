from app.models.schemas import AIGenerationRequest, AIGenerationResponse, PersonaType, LabResult
from app.services.template_service import TemplateService
from app.services.gemini_service import get_gemini_service
from typing import List, Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

# Try to import config gracefully
try:
    from app.config import settings
    SETTINGS_AVAILABLE = True
except ImportError:
    SETTINGS_AVAILABLE = False
    print("⚠️  Settings not available - using defaults for AI service")

class AIService:
    def __init__(self):
        self.template_service = TemplateService()
        # Initialize Gemini service
        try:
            self.gemini_service = get_gemini_service()
            self.ai_enabled = True
            logger.info("AI service initialized with Gemini")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini service: {e}")
            self.gemini_service = None
            self.ai_enabled = False
    
    async def generate_content(
        self, 
        persona: PersonaType, 
        lab_results: List[LabResult], 
        template: Dict[str, Any],
        user_context: Dict[str, Any] = None
    ) -> AIGenerationResponse:
        """
        Generate AI-powered health content using Gemini API.
        Falls back to mock responses if AI service is unavailable.
        """
        
        # If Gemini AI is available, use it for content generation
        if self.ai_enabled and self.gemini_service:
            try:
                # Prepare user data for Gemini
                user_data = {
                    'demographics': user_context or {},
                    'lab_results': [
                        {
                            'test_name': result.name,
                            'value': result.value,
                            'unit': result.unit,
                            'normal_range': f"{result.reference_range.get('min', 'N/A')}-{result.reference_range.get('max', 'N/A')}",
                            'status': result.status
                        }
                        for result in lab_results
                    ],
                    'vitals': user_context.get('vitals', {}) if user_context else {}
                }
                
                # Map persona types to Gemini persona strings
                persona_mapping = {
                    PersonaType.HEALTH_CONSCIOUS: "simple",
                    PersonaType.DETAIL_ORIENTED: "detailed", 
                    PersonaType.ANALYTICAL: "detailed",
                    PersonaType.TECH_SAVVY: "detailed",
                    PersonaType.QUICK_BOLD: "simple",
                    PersonaType.CASUAL: "simple",
                    PersonaType.FAST_ACTION: "simple",
                    PersonaType.BALANCED: "simple",
                    PersonaType.PASSIVE: "simple",
                    PersonaType.BEGINNER: "simple",
                    PersonaType.INTERMEDIATE: "detailed",
                    PersonaType.GOAL_FOCUSED: "detailed",
                    PersonaType.ACTION_ORIENTED: "simple"
                }
                
                gemini_persona = persona_mapping.get(persona, "simple")
                
                # Generate insights using Gemini
                ai_insights = await self.gemini_service.generate_health_insights(
                    user_data, gemini_persona
                )
                
                # Convert Gemini response to our format
                content = self._format_gemini_content(ai_insights, persona)
                recommendations = ai_insights.get('recommendations', [])
                
                # Generate UI components based on template
                ui_components = await self.template_service.structure_ui_response(
                    persona, content, [r.dict() for r in lab_results]
                )
                
                logger.info(f"Generated AI content using Gemini for persona: {persona}")
                
                return AIGenerationResponse(
                    content=content,
                    ui_components=ui_components,
                    recommendations=recommendations
                )
                
            except Exception as e:
                logger.error(f"Gemini AI generation failed: {e}")
                # Fall back to mock response
        
        # Fallback to mock generation
        logger.info("Using mock AI content generation")
        return await self._generate_mock_content(persona, lab_results, template, user_context)
    
    def _format_gemini_content(self, ai_insights: Dict[str, Any], persona: PersonaType) -> str:
        """Format Gemini AI insights into content string"""
        
        summary = ai_insights.get('summary', '')
        key_insights = ai_insights.get('key_insights', [])
        health_score = ai_insights.get('overall_health_score', 75)
        
        # Format content based on persona
        if persona == PersonaType.HEALTH_CONSCIOUS:
            # Simple, encouraging format for health-conscious users
            content = f"Health Overview (Score: {health_score}/100)\n\n"
            content += f"{summary}\n\n"
            if key_insights:
                content += "Key Insights:\n"
                for insight in key_insights[:3]:  # Limit to top 3
                    content += f"• {insight}\n"
            return content
            
        elif persona == PersonaType.DETAIL_ORIENTED:
            # Detailed format with more information
            content = f"Comprehensive Health Analysis\n\n"
            content += f"Overall Health Score: {health_score}/100\n\n"
            content += f"Summary: {summary}\n\n"
            
            if key_insights:
                content += "Detailed Insights:\n"
                for i, insight in enumerate(key_insights, 1):
                    content += f"{i}. {insight}\n"
                content += "\n"
            
            # Add risk factors if available
            risk_factors = ai_insights.get('risk_factors', [])
            if risk_factors:
                content += "Risk Factors to Monitor:\n"
                for risk in risk_factors:
                    content += f"⚠️ {risk}\n"
                content += "\n"
            
            # Add positive indicators
            positive_indicators = ai_insights.get('positive_indicators', [])
            if positive_indicators:
                content += "Positive Health Indicators:\n"
                for positive in positive_indicators:
                    content += f"✅ {positive}\n"
            
            return content
        
        else:  # BASIC persona
            # Simple overview
            content = f"Health Score: {health_score}/100\n\n{summary}"
            if key_insights:
                content += f"\n\nKey Point: {key_insights[0]}"
            return content
    
    async def _generate_mock_content(
        self, 
        persona: PersonaType, 
        lab_results: List[LabResult], 
        template: Dict[str, Any],
        user_context: Dict[str, Any] = None
    ) -> AIGenerationResponse:
        """Generate mock content when AI service is unavailable"""
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
            return await self._generate_normal_results_content(persona)
        
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
                direction = "elevated" if result.status == "high" else "below normal"
                items.append(f"• {result.name}: {direction} ({result.value} {result.unit})")
            
            content = f"Abnormal findings detected ({len(abnormal_results)} total):\n\n"
            content += "\n".join(items)
            content += "\n\nRecommendation: Clinical correlation advised."
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
        if any("glucose" in r.name.lower() for r in abnormal_results):
            if persona == PersonaType.HEALTH_CONSCIOUS:
                recommendations.append("Monitor your blood sugar levels daily")
                recommendations.append("Follow your diabetes management plan")
            else:
                recommendations.append("Consider glucose monitoring")
        
        if any("cholesterol" in r.name.lower() for r in abnormal_results):
            recommendations.append("Consider heart-healthy diet modifications")
            recommendations.append("Discuss cholesterol management with your doctor")
        
        if any("blood" in r.name.lower() for r in abnormal_results):
            recommendations.append("Follow up with your healthcare provider")
            recommendations.append("Consider additional blood work if recommended")
        
        # Ensure we have at least basic recommendations
        if not recommendations:
            recommendations = [
                "Discuss these results with your healthcare provider",
                "Follow any treatment plans recommended by your doctor",
                "Continue monitoring your health regularly"
            ]
        
        return recommendations[:4]  # Limit to 4 recommendations