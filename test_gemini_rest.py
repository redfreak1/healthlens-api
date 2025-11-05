#!/usr/bin/env python3
"""Test the REST-based Gemini service"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.gemini_service import GeminiService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_gemini_rest():
    """Test the REST-based Gemini service"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment")
        return False
    
    # Initialize service
    logger.info("Initializing Gemini REST service...")
    service = GeminiService()
    
    # Test data - matching expected format
    test_data = {
        "lab_results": [
            {
                "test_name": "Total Cholesterol",
                "value": 220,
                "unit": "mg/dL",
                "normal_range": "<200"
            },
            {
                "test_name": "HDL Cholesterol",
                "value": 45,
                "unit": "mg/dL", 
                "normal_range": ">40"
            },
            {
                "test_name": "LDL Cholesterol",
                "value": 150,
                "unit": "mg/dL",
                "normal_range": "<100"
            },
            {
                "test_name": "Triglycerides",
                "value": 200,
                "unit": "mg/dL",
                "normal_range": "<150"
            },
            {
                "test_name": "Blood Glucose",
                "value": 110,
                "unit": "mg/dL",
                "normal_range": "70-100"
            }
        ],
        "demographics": {
            "age": 45,
            "gender": "male"
        },
        "vitals": {
            "blood_pressure": "140/90",
            "heart_rate": 75,
            "weight": 85,
            "bmi": 27.5
        }
    }
    
    try:
        logger.info("Testing content generation...")
        result = await service.generate_health_insights(test_data, "simple")
        
        if result and isinstance(result, dict) and len(str(result)) > 50:
            logger.info("✅ Gemini REST API test successful!")
            logger.info(f"Response keys: {list(result.keys())}")
            if 'summary' in result:
                logger.info(f"Summary length: {len(result['summary'])} characters")
                logger.info(f"Summary preview: {result['summary'][:200]}...")
            return True
        else:
            logger.error("❌ Response invalid or too short")
            logger.error(f"Response: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_rest())
    sys.exit(0 if success else 1)