"""
Test client for FastAPI endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_model_info():
    """Test model info endpoint"""
    print("\n2. Testing Model Info Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_single_prediction():
    """Test single prediction"""
    print("\n3. Testing Single Prediction")
    print("-" * 60)
    
    test_cases = [
        "The road has many potholes and needs repair",
        "Street light is not working at night",
        "Garbage not collected for many days",
        "सड़क पर बहुत गड्ढे हैं",
        "தெரு விளக்கு வேலை செய்யவில்லை",
        "কাজ করছে না রাস্তার আলো"
    ]
    
    for text in test_cases:
        print(f"\nText: {text}")
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"text": text}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Category: {result['category']}")
            print(f"Confidence: {result['confidence']:.2f}%")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n4. Testing Batch Prediction")
    print("-" * 60)
    
    texts = [
        "Road is full of potholes",
        "Street light broken",
        "Garbage overflowing",
        "सड़क खराब है",
        "कचरा नहीं उठाया गया"
    ]
    
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json={"texts": texts}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total predictions: {result['total']}")
        for pred in result['predictions']:
            print(f"\nText: {pred['text']}")
            print(f"  → {pred['category']} ({pred['confidence']:.2f}%)")

def test_categories():
    """Test categories endpoint"""
    print("\n5. Testing Categories Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/categories")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_languages():
    """Test languages endpoint"""
    print("\n6. Testing Languages Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/languages")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total languages: {result['total']}")
    for lang in result['languages']:
        print(f"  {lang['code']}: {lang['name']} ({lang['native']})")

if __name__ == "__main__":
    print("="*60)
    print("FASTAPI ENDPOINT TESTS")
    print("="*60)
    
    try:
        test_health()
        test_model_info()
        test_single_prediction()
        test_batch_prediction()
        test_categories()
        test_languages()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: python api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
