"""
Test different persona types to verify PersonaType.BASIC fix
"""
import requests
import json

# Test data with different persona types
test_personas = [
    "health-conscious",
    "detail-oriented", 
    "analytical",
    "tech-savvy",
    "quick-bold",
    "casual",
    "beginner"
]

base_data = {
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
        }
    ],
    "template_type": "comprehensive"
}

def test_persona_types():
    """Test multiple persona types to verify no PersonaType.BASIC errors"""
    url = "http://10.44.215.180:4192/api/v1/ai/generate"
    
    for persona in test_personas:
        try:
            test_data = {**base_data, "persona": persona}
            print(f"\n🧪 Testing persona: {persona}")
            
            response = requests.post(url, json=test_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {persona}: SUCCESS")
            else:
                print(f"❌ {persona}: FAILED - {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ {persona}: EXCEPTION - {e}")

if __name__ == "__main__":
    test_persona_types()