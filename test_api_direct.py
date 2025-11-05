#!/usr/bin/env python3
"""Test the FastAPI server endpoints directly"""

import asyncio
import sys
import os
import logging
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from api.ai import generate_ai_content
from models.schemas import AIGenerationRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_api_directly():
    """Test the API endpoint directly without HTTP"""
    
    load_dotenv()
    
    # Test data - matching AIGenerationRequest schema
    test_request = {
        "persona": "balanced",  # Must be one of the PersonaType enum values
        "lab_results": [
            {
                "name": "Total Cholesterol",
                "value": 220.0,
                "unit": "mg/dL",
                "reference_range": {"min": 0, "max": 200},
                "category": "lipid",
                "status": "high"
            },
            {
                "name": "HDL Cholesterol", 
                "value": 45.0,
                "unit": "mg/dL",
                "reference_range": {"min": 40, "max": 100},
                "category": "lipid",
                "status": "normal"
            }
        ],
        "template_type": "standard",
        "user_context": {
            "age": 45,
            "gender": "male"
        }
    }
    
    try:
        logger.info("Testing API endpoint directly...")
        
        # Create request object
        request_obj = AIGenerationRequest(**test_request)
        
        # Call the endpoint function directly
        result = await generate_ai_content(request_obj)
        
        logger.info("✅ API endpoint test successful!")
        logger.info(f"Response type: {type(result)}")
        logger.info(f"Response: {result}")
        
        # If it's a response object, extract the content
        if hasattr(result, 'content'):
            content = result.content
            logger.info(f"Content type: {type(content)}")
            logger.info(f"Content: {content}")
        elif hasattr(result, '__dict__'):
            logger.info(f"Response dict: {result.__dict__}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_directly())
    sys.exit(0 if success else 1)