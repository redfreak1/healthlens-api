#!/usr/bin/env python3
"""
Quick test script to verify new Gemini API key works
Run this after updating your API key in .env
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_api_key():
    """Test if the new API key works"""
    
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your-new-gemini-api-key-here':
        print("❌ Please update GEMINI_API_KEY in .env file")
        return False
    
    print(f"🔑 Testing API key: {api_key[:10]}...")
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": "Say 'API key test successful' if you can read this."}]
        }]
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=payload,
            timeout=10,
            verify=False  # For corporate networks
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ API key test successful!")
                print(f"🤖 Gemini response: {content}")
                return True
            else:
                print("❌ Unexpected response format")
                return False
                
        elif response.status_code == 403:
            error_msg = response.text
            if "leaked" in error_msg.lower():
                print("❌ API key is still reported as leaked")
                print("🔄 Please generate a completely new API key")
            else:
                print(f"❌ API access forbidden: {error_msg}")
            return False
            
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.SSLError:
        print("⚠️  SSL error - trying without verification (corporate network)")
        # Try again without SSL verification
        try:
            response = requests.post(
                f"{url}?key={api_key}",
                headers=headers,
                json=payload,
                timeout=10,
                verify=False
            )
            # Process response same as above
            if response.status_code == 200:
                print("✅ API key test successful (unverified SSL)!")
                return True
            else:
                print(f"❌ API call failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing new Gemini API key...")
    print("=" * 50)
    
    success = test_api_key()
    
    print("=" * 50)
    if success:
        print("🎉 Your new API key is working correctly!")
        print("✅ You can now deploy to GCP safely")
    else:
        print("🚨 API key test failed")
        print("📖 Please follow the instructions in API_KEY_SETUP.md")