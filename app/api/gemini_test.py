"""
Gemini API test endpoints for validating AI integration
"""

from fastapi import APIRouter, HTTPException
from app.services.gemini_service import get_gemini_service
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini", tags=["gemini"])

@router.get("/test-connection")
async def test_gemini_connection():
    """Test Gemini API connection"""
    try:
        gemini_service = get_gemini_service()
        result = await gemini_service.test_connection()
        return result
    except Exception as e:
        logger.error(f"Gemini connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini API connection failed: {str(e)}")

@router.post("/generate-health-insights")
async def generate_health_insights(request: Dict[str, Any]):
    """Generate health insights using Gemini API"""
    try:
        gemini_service = get_gemini_service()
        
        # Extract data from request
        user_data = request.get('user_data', {})
        persona_type = request.get('persona_type', 'simple')
        
        # Generate insights
        insights = await gemini_service.generate_health_insights(user_data, persona_type)
        
        return {
            "status": "success",
            "insights": insights,
            "persona_type": persona_type
        }
        
    except Exception as e:
        logger.error(f"Health insights generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate health insights: {str(e)}")

@router.post("/test-sample-data")
async def test_with_sample_data():
    """Test Gemini API with sample health data"""
    try:
        gemini_service = get_gemini_service()
        
        # Sample user data for testing
        sample_data = {
            'demographics': {
                'age': 45,
                'gender': 'female'
            },
            'lab_results': [
                {
                    'test_name': 'Total Cholesterol',
                    'value': 240,
                    'unit': 'mg/dL',
                    'normal_range': '< 200 mg/dL',
                    'status': 'high'
                },
                {
                    'test_name': 'Blood Glucose',
                    'value': 105,
                    'unit': 'mg/dL',
                    'normal_range': '70-100 mg/dL',
                    'status': 'high'
                },
                {
                    'test_name': 'HDL Cholesterol',
                    'value': 55,
                    'unit': 'mg/dL',
                    'normal_range': '> 50 mg/dL',
                    'status': 'normal'
                }
            ],
            'vitals': {
                'blood_pressure': '130/85 mmHg',
                'heart_rate': 72,
                'weight': 68,
                'bmi': 24.5
            }
        }
        
        # Test with different persona types
        results = {}
        for persona in ['simple', 'detailed']:
            insights = await gemini_service.generate_health_insights(sample_data, persona)
            results[persona] = insights
        
        return {
            "status": "success",
            "message": "Sample data test completed",
            "sample_data": sample_data,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Sample data test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Sample data test failed: {str(e)}")