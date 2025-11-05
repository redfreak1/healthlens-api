"""
Check available Gemini models and test with correct model name
"""
import os
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyC_sVs2CvzS3dJkIBe2QqNaq6r0csYrjrE"
genai.configure(api_key=API_KEY)

def list_available_models():
    """List all available Gemini models"""
    try:
        print("🔍 Checking available Gemini models...")
        models = genai.list_models()
        
        print("Available models:")
        for model in models:
            print(f"  - {model.name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"    Supported methods: {model.supported_generation_methods}")
        
        return models
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return []

def test_with_correct_model():
    """Test with the correct model name"""
    try:
        # Try different model names based on what's available
        model_names = [
            'models/gemini-2.5-flash',
            'models/gemini-flash-latest',
            'models/gemini-2.5-pro',
            'models/gemini-pro-latest',
            'models/gemini-2.0-flash',
            'gemini-2.5-flash',
            'gemini-flash-latest'
        ]
        
        for model_name in model_names:
            try:
                print(f"\n🧪 Testing model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content("Hello, can you confirm you're working? Just say 'Gemini API is working!'")
                
                print(f"✅ SUCCESS with model: {model_name}")
                print(f"Response: {response.text}")
                return model_name
                
            except Exception as e:
                print(f"❌ Failed with {model_name}: {e}")
                continue
        
        print("❌ No working model found")
        return None
        
    except Exception as e:
        print(f"❌ Error in model testing: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Testing Gemini API with new key...")
    print(f"API Key (first 10 chars): {API_KEY[:10]}...")
    print()
    
    # List available models
    models = list_available_models()
    print()
    
    # Test with correct model
    working_model = test_with_correct_model()
    
    if working_model:
        print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        print("✅ Gemini API is now ready for HealthLens integration!")
    else:
        print("\n❌ No working models found. Please check API configuration.")