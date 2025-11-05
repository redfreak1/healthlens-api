#!/usr/bin/env python3
"""
Test the exact request format from the logs that was causing JSON parsing issues
"""

import os
import sys
import asyncio
import json
import logging
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.gemini_service import GeminiService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_exact_log_format():
    """Test with the exact data format from the logs"""
    
    load_dotenv()
    
    # Initialize service
    logger.info("Testing exact log format from production...")
    service = GeminiService()
    
    # Exact data from your logs
    test_data = {
        "persona": "intermediate",
        "lab_results": [
            {
                "name": "Glucose",
                "value": 95,
                "unit": "mg/dL",
                "reference_range": {"min": 70, "max": 99},
                "category": "Metabolic Panel",
                "status": "normal",
                "referenceRange": {"min": 70, "max": 99}  # Note: duplicate field in your data
            },
            {
                "name": "White Blood Cell Count",
                "value": 11.2,
                "unit": "K/uL",
                "reference_range": {"min": 4.5, "max": 11},
                "category": "Complete Blood Count",
                "status": "high",
                "referenceRange": {"min": 4.5, "max": 11}
            },
            {
                "name": "Red Blood Cell Count",
                "value": 4.8,
                "unit": "M/uL",
                "reference_range": {"min": 4.5, "max": 5.9},
                "category": "Complete Blood Count",
                "status": "normal",
                "referenceRange": {"min": 4.5, "max": 5.9}
            },
            {
                "name": "Hemoglobin",
                "value": 14.2,
                "unit": "g/dL",
                "reference_range": {"min": 13.5, "max": 17.5},
                "category": "Complete Blood Count",
                "status": "normal",
                "referenceRange": {"min": 13.5, "max": 17.5}
            },
            {
                "name": "Hematocrit",
                "value": 42.1,
                "unit": "%",
                "reference_range": {"min": 38.8, "max": 50},
                "category": "Complete Blood Count",
                "status": "normal",
                "referenceRange": {"min": 38.8, "max": 50}
            },
            {
                "name": "Platelet Count",
                "value": 210,
                "unit": "K/uL",
                "reference_range": {"min": 150, "max": 400},
                "category": "Complete Blood Count",
                "status": "normal",
                "referenceRange": {"min": 150, "max": 400}
            },
            {
                "name": "Sodium",
                "value": 148,
                "unit": "mmol/L",
                "reference_range": {"min": 136, "max": 145},
                "category": "Metabolic Panel",
                "status": "normal",
                "referenceRange": {"min": 136, "max": 145}
            },
            {
                "name": "Potassium",
                "value": 3.2,
                "unit": "mmol/L",
                "reference_range": {"min": 3.5, "max": 5.1},
                "category": "Metabolic Panel",
                "status": "low",
                "referenceRange": {"min": 3.5, "max": 5.1}
            },
            {
                "name": "Creatinine",
                "value": 1,
                "unit": "mg/dL",
                "reference_range": {"min": 0.7, "max": 1.3},
                "category": "Metabolic Panel",
                "status": "normal",
                "referenceRange": {"min": 0.7, "max": 1.3}
            },
            {
                "name": "Total Cholesterol",
                "value": 195,
                "unit": "mg/dL",
                "reference_range": {"min": 0, "max": 200},
                "category": "Lipid Panel",
                "status": "normal",
                "referenceRange": {"min": 0, "max": 200}
            }
        ],
        "template_type": "chat_response",
        "user_context": {
            "query": "Testing"
        }
    }
    
    try:
        logger.info("Testing with production-like data (10 lab results)...")
        
        # Count abnormal results
        abnormal_results = [r for r in test_data["lab_results"] if r["status"] != "normal"]
        logger.info(f"Lab results: {len(test_data['lab_results'])} total, {len(abnormal_results)} abnormal")
        
        # Call the generate_health_insights method directly
        result = await service.generate_health_insights(test_data, test_data["persona"])
        
        if result and isinstance(result, dict):
            logger.info("✅ JSON parsing and response generation successful!")
            logger.info(f"Response keys: {list(result.keys())}")
            
            # Check for required fields
            required_fields = ['overall_health_score', 'key_insights', 'recommendations', 'summary']
            missing_fields = [field for field in required_fields if field not in result]
            
            if not missing_fields:
                logger.info("✅ All required fields present")
                logger.info(f"Health Score: {result.get('overall_health_score', 'N/A')}")
                logger.info(f"Insights: {len(result.get('key_insights', []))} items")
                logger.info(f"Recommendations: {len(result.get('recommendations', []))} items")
                logger.info(f"Summary length: {len(result.get('summary', ''))} characters")
                
                # Show a sample of the content
                if 'summary' in result:
                    logger.info(f"Summary preview: {result['summary'][:200]}...")
                
                return True
            else:
                logger.error(f"❌ Missing required fields: {missing_fields}")
                return False
        else:
            logger.error("❌ Response is not a valid dictionary")
            logger.error(f"Response type: {type(result)}")
            logger.error(f"Response: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_exact_log_format())
    print("=" * 60)
    if success:
        print("🎉 Production data format test PASSED!")
        print("✅ JSON parsing issues should be resolved")
        print("✅ Ready for deployment with new API key")
    else:
        print("🚨 Production data format test FAILED")
        print("❌ Additional fixes may be needed")
    sys.exit(0 if success else 1)