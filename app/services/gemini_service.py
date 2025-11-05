"""
Gemini API Service for AI content generation
Provides health insights using Google's Gemini API via REST
"""

import os
import json
import logging
import requests
import asyncio
from typing import Dict, Any, List, Optional

# Load environment variables early
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini AI API via REST"""
    
    def __init__(self):
        """Initialize Gemini service with API key and REST configuration"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        model_env = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        # Convert model name to REST API format (remove 'models/' prefix if present)
        self.model_name = model_env.replace('models/', '') if model_env.startswith('models/') else model_env
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Configure session with retries and proxy settings
        self.session = requests.Session()
        self.session.verify = False  # For corporate networks
        
        # Add proxy settings if available
        proxy_url = os.getenv('HTTP_PROXY') or os.getenv('HTTPS_PROXY')
        if proxy_url:
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            logger.info(f"Using proxy: {proxy_url}")
        
        # Disable SSL warnings for corporate networks
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Check if service is available
        self.gemini_available = bool(self.api_key)
        
        # Debug logging
        logger.info(f"🔧 Gemini REST Service Debug:")
        logger.info(f"  - API Key present: {bool(self.api_key)}")
        logger.info(f"  - API Key (first 10): {self.api_key[:10] if self.api_key else 'None'}...")
        logger.info(f"  - Model: {self.model_name}")
        logger.info(f"  - Base URL: {self.base_url}")
        logger.info(f"  - Service available: {self.gemini_available}")
        
        if not self.gemini_available:
            logger.warning("Gemini REST service not available - using mock responses")
            return
        
        # Test connection (optional - don't fail if it doesn't work)
        try:
            self._test_connection()
            logger.info("✅ Gemini REST service initialized successfully")
        except Exception as e:
            logger.warning(f"Gemini REST API test connection failed: {e}")
            logger.info("🔄 Service will still attempt to generate content when requested")
            # Don't set gemini_available to False here - let it try during actual requests
    
    def _test_connection(self):
        """Test the REST API connection"""
        url = f"{self.base_url}/{self.model_name}:generateContent"
        headers = {
            'Content-Type': 'application/json',
        }
        test_payload = {
            "contents": [{
                "parts": [{"text": "Hello"}]
            }],
            "generationConfig": {
                "maxOutputTokens": 10
            }
        }
        
        # Try with SSL verification first, then without if it fails
        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=test_payload,
                timeout=10,
                verify=True
            )
        except requests.exceptions.SSLError:
            logger.warning("SSL verification failed, trying without SSL verification (corporate network)")
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=test_payload,
                timeout=10,
                verify=False
            )
        
        if response.status_code == 403:
            error_msg = response.text
            if "leaked" in error_msg.lower() or "reported" in error_msg.lower():
                logger.error("🔑 API key has been reported as leaked - please generate a new key")
                raise Exception(f"API key leaked: {error_msg}")
            else:
                logger.error("🚫 API access forbidden - check permissions")
                raise Exception(f"API access forbidden: {error_msg}")
        elif response.status_code != 200:
            raise Exception(f"REST API test failed: {response.status_code} - {response.text}")
        
        logger.info("✅ Gemini REST API connection test successful")
    
    async def generate_health_insights(
        self, 
        user_data: Dict[str, Any], 
        persona_type: str = "simple"
    ) -> Dict[str, Any]:
        """
        Generate personalized health insights based on user data
        
        Args:
            user_data: User health information including lab results, demographics
            persona_type: Type of persona (simple, detailed, etc.)
            
        Returns:
            Dictionary containing AI-generated health insights
        """
        # If Gemini is not available, return mock insights
        if not self.gemini_available:
            logger.info("Using mock health insights (Gemini not available)")
            return self._get_mock_insights(user_data, persona_type)
        
        try:
            # Prepare prompt for health insights
            prompt = self._create_health_insights_prompt(user_data, persona_type)
            
            # Generate content using REST API
            response_text = self._generate_content_rest(prompt)
            
            # Parse response
            if response_text:
                insights = self._parse_health_insights(response_text)
                logger.info(f"Generated health insights using Gemini REST API (persona: {persona_type})")
                return insights
            else:
                logger.warning("Empty response from Gemini REST API")
                return self._get_mock_insights(user_data, persona_type)
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'connection' in error_msg or 'timeout' in error_msg or 'network' in error_msg:
                logger.error(f"Gemini REST API network error: {str(e)}")
                logger.warning("Falling back to mock responses due to network issue")
            else:
                logger.error(f"Error generating health insights with Gemini REST API: {str(e)}")
            return self._get_mock_insights(user_data, persona_type)
    
    def _generate_content_rest(self, prompt: str) -> str:
        """Generate content using Gemini REST API with retries"""
        url = f"{self.base_url}/{self.model_name}:generateContent"
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topP": 0.8,
                "topK": 40,
                "maxOutputTokens": 2048,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        # Try multiple times with different configurations
        attempts = [
            {"timeout": 15, "verify": False, "description": "Quick unverified"},
            {"timeout": 30, "verify": False, "description": "Extended unverified"},
            {"timeout": 45, "verify": True, "description": "Extended with SSL"}
        ]
        
        last_error = None
        for i, attempt in enumerate(attempts):
            try:
                logger.info(f"Attempting Gemini REST API call #{i+1}: {attempt['description']}")
                
                response = self.session.post(
                    f"{url}?key={self.api_key}",
                    headers=headers,
                    json=payload,
                    timeout=attempt['timeout'],
                    verify=attempt['verify']
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract text from response
                    if 'candidates' in result and len(result['candidates']) > 0:
                        candidate = result['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            parts = candidate['content']['parts']
                            if len(parts) > 0 and 'text' in parts[0]:
                                logger.info(f"✅ Gemini REST API success on attempt #{i+1}")
                                return parts[0]['text']
                    
                    raise Exception("No valid text content in response")
                    
                elif response.status_code == 403:
                    error_msg = response.text
                    if "leaked" in error_msg.lower() or "reported" in error_msg.lower():
                        logger.error("🔑 API key has been reported as leaked - stopping all attempts")
                        raise Exception(f"API key leaked: {error_msg}")
                    else:
                        raise Exception(f"API access forbidden: {error_msg}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt #{i+1} failed: {str(e)}")
                if i < len(attempts) - 1:
                    logger.info(f"Retrying with next configuration...")
                continue
        
        # All attempts failed
        raise Exception(f"All REST API attempts failed. Last error: {last_error}")
    
    def _create_health_insights_prompt(self, user_data: Dict[str, Any], persona_type: str) -> str:
        """Create a detailed prompt for health insights generation"""
        
        # Extract user information
        demographics = user_data.get('demographics', {})
        lab_results = user_data.get('lab_results', [])
        vitals = user_data.get('vitals', {})
        
        age = demographics.get('age', 'unknown')
        gender = demographics.get('gender', 'unknown')
        
        # Format lab results
        lab_summary = []
        for lab in lab_results:
            lab_summary.append(f"- {lab.get('test_name', 'Unknown test')}: {lab.get('value', 'N/A')} {lab.get('unit', '')} (Normal range: {lab.get('normal_range', 'N/A')})")
        
        lab_text = "\n".join(lab_summary) if lab_summary else "No lab results available"
        
        # Format vitals
        vitals_text = ""
        if vitals:
            vitals_text = f"""
            Blood Pressure: {vitals.get('blood_pressure', 'N/A')}
            Heart Rate: {vitals.get('heart_rate', 'N/A')} bpm
            Weight: {vitals.get('weight', 'N/A')} kg
            BMI: {vitals.get('bmi', 'N/A')}
            """
        
        # Persona-specific instructions
        persona_instructions = {
            "simple": "Provide simple, easy-to-understand health insights in plain language. Focus on key takeaways and basic recommendations.",
            "detailed": "Provide comprehensive health analysis with detailed explanations, medical context, and specific recommendations.",
            "clinical": "Provide clinical-grade analysis with medical terminology, risk assessments, and evidence-based recommendations."
        }
        
        persona_instruction = persona_instructions.get(persona_type, persona_instructions["simple"])
        
        prompt = f"""
        You are a health AI assistant providing personalized health insights. Analyze the following health data and provide insights ONLY in valid JSON format.

        Patient Information:
        - Age: {age}
        - Gender: {gender}

        Lab Results:
        {lab_text}

        Vitals:
        {vitals_text}

        Instructions: {persona_instruction}

        CRITICAL: Respond with ONLY valid JSON in the exact format below. Do not include any text before or after the JSON:

        {{
            "overall_health_score": <number between 0-100>,
            "key_insights": [
                "insight 1",
                "insight 2", 
                "insight 3"
            ],
            "recommendations": [
                "recommendation 1",
                "recommendation 2",
                "recommendation 3"
            ],
            "risk_factors": [
                "risk factor 1 if any",
                "risk factor 2 if any"
            ],
            "positive_indicators": [
                "positive indicator 1",
                "positive indicator 2"
            ],
            "summary": "Brief overall health summary",
            "next_steps": [
                "suggested next step 1",
                "suggested next step 2"
            ]
        }}

        IMPORTANT RULES:
        - Return ONLY valid JSON, no additional text
        - Base insights only on the provided data
        - If data is limited, acknowledge limitations in the insights
        - Provide general wellness advice when specific medical data is unavailable
        - Do not provide specific medical diagnoses
        - Encourage consultation with healthcare providers for medical concerns
        - Health score should reflect the lab results (higher for normal values, lower for abnormal)
        """
        
        return prompt
    
    def _parse_health_insights(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response and extract structured insights"""
        try:
            # Try to find JSON in the response using regex
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                insights = json.loads(json_str)
                logger.info("✅ Successfully parsed JSON from Gemini response")
                
                # Validate required fields
                required_fields = ['overall_health_score', 'key_insights', 'recommendations', 'summary']
                for field in required_fields:
                    if field not in insights:
                        insights[field] = self._get_default_value(field)
                
                return insights
            else:
                logger.warning("⚠️ No JSON found in response, creating structured response")
                return self._create_structured_response_from_text(response_text)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            logger.error(f"Response text: {response_text[:500]}...")
            return self._create_structured_response_from_text(response_text)
    
    def _create_structured_response_from_text(self, text: str) -> Dict[str, Any]:
        """Create structured response when JSON parsing fails"""
        import re
        
        # Extract health score if present
        health_score_match = re.search(r'Health Score:\s*(\d+)/100', text)
        health_score = int(health_score_match.group(1)) if health_score_match else 75
        
        # Extract insights from text
        lines = text.split('\n')
        insights = []
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:
                if any(keyword in line.lower() for keyword in ['high', 'low', 'elevated', 'abnormal', 'normal']):
                    insights.append(line)
                elif any(keyword in line.lower() for keyword in ['recommend', 'should', 'consider', 'suggest']):
                    recommendations.append(line)
        
        # Default values if extraction fails
        if not insights:
            insights = [
                "AI health analysis completed successfully",
                "Health data has been processed and reviewed",
                "Personalized insights generated based on available data"
            ]
        
        if not recommendations:
            recommendations = [
                "Schedule follow-up consultation with healthcare provider",
                "Maintain regular exercise routine and balanced nutrition",
                "Monitor key health indicators regularly"
            ]
        
        return {
            "overall_health_score": health_score,
            "key_insights": insights[:3],
            "recommendations": recommendations[:3],
            "risk_factors": [
                "Consult healthcare provider for detailed analysis"
            ],
            "positive_indicators": [
                "Active health monitoring",
                "Engagement with health data analysis"
            ],
            "summary": text[:300] + "..." if len(text) > 300 else text,
            "next_steps": [
                "Review results with healthcare provider",
                "Continue monitoring health metrics"
            ]
        }
    
    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing fields"""
        defaults = {
            'overall_health_score': 75,
            'key_insights': ["Personalized health insights generated"],
            'recommendations': ["Maintain healthy lifestyle habits"],
            'risk_factors': [],
            'positive_indicators': ["Active health monitoring"],
            'summary': "Health insights generated using AI analysis",
            'next_steps': ["Continue health monitoring"]
        }
        return defaults.get(field, "")
    
    def _get_mock_insights(self, user_data: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Generate mock insights when Gemini API is not available"""
        
        # Extract some data for context
        lab_results = user_data.get('lab_results', [])
        demographics = user_data.get('demographics', {})
        age = demographics.get('age', 'unknown')
        
        # Count abnormal results
        abnormal_count = sum(1 for lab in lab_results if lab.get('status', '').lower() != 'normal')
        total_tests = len(lab_results)
        
        # Calculate a basic health score
        if total_tests > 0:
            health_score = max(50, 100 - (abnormal_count * 15))
        else:
            health_score = 75
        
        # Generate persona-specific insights
        if persona_type == "detailed":
            insights = {
                "overall_health_score": health_score,
                "key_insights": [
                    f"Analyzed {total_tests} lab parameters with {abnormal_count} values outside normal range",
                    "Health assessment shows areas for improvement and monitoring",
                    "Personalized recommendations provided based on current health data",
                    "Regular monitoring recommended for optimal health maintenance"
                ],
                "recommendations": [
                    "Schedule follow-up consultation with healthcare provider",
                    "Maintain regular exercise routine (150 minutes moderate activity per week)",
                    "Follow balanced nutrition plan with emphasis on whole foods",
                    "Monitor key health indicators monthly",
                    "Stay hydrated and maintain adequate sleep (7-9 hours)"
                ],
                "risk_factors": [
                    f"Age-related health considerations (age: {age})" if age != 'unknown' else "Age considerations",
                    "Values outside normal range require monitoring" if abnormal_count > 0 else ""
                ],
                "positive_indicators": [
                    "Active health monitoring and engagement",
                    "Proactive approach to health management",
                    "Comprehensive health data collection"
                ],
                "summary": f"Comprehensive health analysis complete. Health score of {health_score}/100 indicates {'good overall health with room for optimization' if health_score >= 70 else 'areas requiring attention and improvement'}. Continue monitoring and follow healthcare provider recommendations.",
                "next_steps": [
                    "Review results with healthcare provider",
                    "Implement recommended lifestyle modifications",
                    "Schedule follow-up testing as advised",
                    "Continue regular health monitoring"
                ]
            }
        else:  # simple persona
            insights = {
                "overall_health_score": health_score,
                "key_insights": [
                    f"Your health score is {health_score} out of 100",
                    f"Reviewed {total_tests} test results" if total_tests > 0 else "Health assessment completed",
                    f"{abnormal_count} values need attention" if abnormal_count > 0 else "Most values look good"
                ],
                "recommendations": [
                    "Talk to your doctor about these results",
                    "Keep up with regular exercise",
                    "Eat healthy foods",
                    "Get enough sleep"
                ],
                "risk_factors": [],
                "positive_indicators": [
                    "You're tracking your health",
                    "Taking a proactive approach"
                ],
                "summary": f"Your health score is {health_score}/100. {'Keep up the good work!' if health_score >= 75 else 'There are some areas to focus on.'} Talk to your doctor about these results.",
                "next_steps": [
                    "Discuss with your healthcare provider",
                    "Follow their recommendations"
                ]
            }
        
        # Remove empty risk factors
        insights["risk_factors"] = [rf for rf in insights["risk_factors"] if rf.strip()]
        
        return insights
    
    def _get_fallback_insights(self) -> Dict[str, Any]:
        """Provide fallback insights when AI generation fails"""
        return {
            "overall_health_score": 75,
            "key_insights": [
                "Health data reviewed successfully",
                "General wellness recommendations provided",
                "Continued monitoring encouraged"
            ],
            "recommendations": [
                "Maintain regular exercise routine",
                "Follow balanced nutrition plan",
                "Schedule regular health checkups"
            ],
            "risk_factors": [],
            "positive_indicators": [
                "Active health data tracking",
                "Proactive health management"
            ],
            "summary": "General health insights provided. For personalized analysis, ensure complete health data is available.",
            "next_steps": [
                "Update health profile with latest data",
                "Consult healthcare provider for comprehensive assessment"
            ]
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Gemini API connection"""
        if not self.gemini_available:
            return {
                "status": "unavailable",
                "message": "Gemini API not available (using mock responses)",
                "model": "mock",
                "api_key_status": "not configured" if not self.api_key else "configured but library unavailable"
            }
        
        try:
            test_prompt = "Respond with 'Gemini API connection successful' if you can read this message."
            
            response = self.model.generate_content(
                test_prompt,
                safety_settings=self.safety_settings
            )
            
            if response.text:
                return {
                    "status": "success",
                    "message": "Gemini API connection working",
                    "model": self.model_name,
                    "response": response.text
                }
            else:
                return {
                    "status": "error",
                    "message": "Empty response from Gemini API"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Gemini API connection failed: {str(e)}",
                "fallback": "Using mock responses"
            }

# Global service instance
gemini_service = None

def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global gemini_service
    if gemini_service is None:
        gemini_service = GeminiService()
    return gemini_service