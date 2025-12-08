#!/usr/bin/env python3
"""
Test if the system is using ML model for recommendations
"""

import requests
import json
import time

def test_ml_recommendations():
    """Test if ML model is being used for recommendations"""

    print("🧪 Testing ML Model Usage for Recommendations")
    print("=" * 50)

    base_url = "http://localhost:8000"

    # Test 1: Check server health
    print("\n1️⃣ Checking Server Health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server is healthy")
            print(f"   ML Model Available: {health.get('ml_model_available', False)}")
            print(f"   Model Type: {health.get('model_type', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running: python backend/recommendation_server_fixed.py")
        return False

    # Test 2: Test with high-end phone and high budget (should trigger ML)
    print("\n2️⃣ Testing with High-end Phone + High Budget...")
    test_data_high = {
        "phone_model": "iPhone (13/14/15 Pro Max)",
        "gender": "Laki-laki",
        "reason": "Mencari internet yang stabil",
        "call_frequency": "Jarang",
        "wifi": "Ya dirumah",
        "housing": "Rumah pribadi",
        "usage": ["Gaming online", "Streaming video (YouTube, Netflix, dll.)"],
        "quota": "50–100 GB",
        "budget": "> Rp250.000",
        "preference": "Kuota besar",
        "roaming": "Sering"
    }

    response = requests.post(
        f"{base_url}/api/recommend",
        json=test_data_high,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Recommendations received")
        print(f"   ML Model Used: {result['metadata']['ml_model_used']}")
        print(f"   Recommendation Source: {result['metadata']['recommendation_source']}")
        print(f"   Number of Recommendations: {len(result['recommendations'])}")

        if result['recommendations']:
            top_rec = result['recommendations'][0]
            print(f"   Top Recommendation: {top_rec['name']}")
            print(f"   Match Percentage: {top_rec['match_percentage']}%")
            if 'model_confidence' in top_rec:
                print(f"   ML Confidence: {top_rec['model_confidence']*100:.1f}%")
    else:
        print(f"❌ Recommendation request failed: {response.status_code}")
        return False

    # Test 3: Test with budget phone and low budget
    print("\n3️⃣ Testing with Budget Phone + Low Budget...")
    test_data_low = {
        "phone_model": "Xiaomi Redmi Note Series",
        "gender": "Perempuan",
        "reason": "Mencari internet yang murah",
        "call_frequency": "Tidak pernah",
        "wifi": "Tidak",
        "housing": "Kost/kontrakan",
        "usage": ["Browsing & media sosial"],
        "quota": "< 10 GB",
        "budget": "< Rp25.000",
        "preference": "Hemat/entry-level",
        "roaming": "Tidak"
    }

    response = requests.post(
        f"{base_url}/api/recommend",
        json=test_data_low,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Recommendations received")
        print(f"   ML Model Used: {result['metadata']['ml_model_used']}")
        print(f"   Recommendation Source: {result['metadata']['recommendation_source']}")

        if result['recommendations']:
            top_rec = result['recommendations'][0]
            print(f"   Top Recommendation: {top_rec['name']}")
            print(f"   Match Percentage: {top_rec['match_percentage']}%")
    else:
        print(f"❌ Recommendation request failed: {response.status_code}")
        return False

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    # Check if ML is being used
    ml_used_high = result['metadata']['ml_model_used'] if 'metadata' in result else False

    if ml_used_high:
        print("✅ ML Model IS being used for recommendations!")
        print("   The system successfully integrates ML predictions")
        print("   You should see 'ML Model' badges in the frontend")
    else:
        print("⚠️  ML Model is NOT being used")
        print("   The system is using rule-based recommendations")
        print("   This could be due to:")
        print("   - ML model loading issues")
        print("   - Compatibility problems")
        print("   - Intentional fallback to rule-based system")

    print("\n🔍 How to verify in the frontend:")
    print("1. Take the survey on home-before.html")
    print("2. Look for green 'ML Model' badge (if ML is used)")
    print("3. Look for orange 'Rule-based Algorithm' badge (if fallback)")
    print("4. Check for confidence scores on ML recommendations")

    return ml_used_high

if __name__ == "__main__":
    print("Starting ML Model Usage Test...")
    print("Make sure the fixed server is running:")
    print("python backend/recommendation_server_fixed.py")
    print()

    time.sleep(2)  # Give user time to read

    success = test_ml_recommendations()

    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed. Check server logs for details.")