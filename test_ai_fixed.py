"""
Test the fixed Gemini AI integration with correct LabResult schema
"""
import requests
import json

# Test data with proper LabResult structure
test_data = {
    "user_context": {
        "age": 35,
        "gender": "male",
        "vitals": {
            "blood_pressure": "120/80",
            "heart_rate": 72,
            "temperature": "98.6°F"
        }
    },
    "lab_results": [
        {
            "name": "Total Cholesterol",
            "value": 195.0,
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 200},
            "category": "lipid",
            "status": "normal"
        },
        {
            "name": "Blood Glucose",
            "value": 90.0,
            "unit": "mg/dL", 
            "reference_range": {"min": 70, "max": 100},
            "category": "metabolic",
            "status": "normal"
        },
        {
            "name": "HDL Cholesterol",
            "value": 55.0,
            "unit": "mg/dL",
            "reference_range": {"min": 40, "max": 999},
            "category": "lipid", 
            "status": "normal"
        }
    ],
    "persona": "health-conscious",
    "template_type": "comprehensive"
}

def test_ai_generation():
    """Test the AI generation endpoint"""
    url = "http://10.44.215.180:4192/api/v1/ai/generate"
    
    try:
        print("🧪 Testing AI generation with fixed LabResult schema...")
        print(f"📡 POST {url}")
        print(f"📝 Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI generation successful!")
            print(f"📄 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ AI generation failed!")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")

if __name__ == "__main__":
    test_ai_generation()