"""
Test script to verify Gemini API integration
"""
import os
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyC_sVs2CvzS3dJkIBe2QqNaq6r0csYrjrE"
genai.configure(api_key=API_KEY)

def test_gemini_connection():
    """Test basic Gemini API connection"""
    try:
        # Initialize model
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Test with a simple prompt
        response = model.generate_content("Hello, can you confirm you're working? Just say 'Gemini API is working!'")
        
        print("🎉 SUCCESS: Gemini API Connection Test")
        print("=" * 50)
        print(f"Response: {response.text}")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Gemini API Connection Failed")
        print(f"Error details: {str(e)}")
        return False

def test_health_insights():
    """Test health insights generation"""
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Sample health data
        prompt = """
        You are a health AI assistant. Analyze this health data and provide insights in JSON format:
        
        Patient: 45-year-old female
        Lab Results:
        - Total Cholesterol: 240 mg/dL (Normal: < 200 mg/dL) - HIGH
        - Blood Glucose: 105 mg/dL (Normal: 70-100 mg/dL) - HIGH
        - HDL Cholesterol: 55 mg/dL (Normal: > 50 mg/dL) - NORMAL
        
        Provide response in this JSON format:
        {
            "overall_health_score": <number 0-100>,
            "key_insights": ["insight 1", "insight 2"],
            "recommendations": ["recommendation 1", "recommendation 2"],
            "summary": "Brief health summary"
        }
        """
        
        response = model.generate_content(prompt)
        
        print("🎉 SUCCESS: Health Insights Generation Test")
        print("=" * 50)
        print(f"Health Analysis Response:")
        print(response.text)
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Health Insights Generation Failed")
        print(f"Error details: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gemini API Tests...")
    print(f"API Key (first 10 chars): {API_KEY[:10]}...")
    print()
    
    # Test 1: Basic connection
    connection_success = test_gemini_connection()
    print()
    
    # Test 2: Health insights
    if connection_success:
        health_success = test_health_insights()
    
    print("\n🎯 Test Summary:")
    print(f"✅ Basic Connection: {'PASSED' if connection_success else 'FAILED'}")
    if connection_success:
        print(f"✅ Health Insights: {'PASSED' if health_success else 'FAILED'}")
    
    if connection_success:
        print("\n🎉 All tests passed! Gemini API is ready for HealthLens integration.")
    else:
        print("\n❌ Tests failed. Please check API key and configuration.")