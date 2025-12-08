#!/usr/bin/env python3
"""
Test script for ML model integration
Verifies that the ML model is working correctly with survey data
"""

import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.ml_integration import MLModelIntegrator

def test_ml_model():
    """Test the ML model with sample survey data"""
    print("🧪 Testing ML Model Integration")
    print("=" * 50)

    # Initialize ML integrator
    model_path = "model_telco_recommendation.pkl"
    integrator = MLModelIntegrator(model_path)

    if not integrator.is_available():
        print("❌ ML model is not available")
        print("Falling back to rule-based system will be used")
        return False

    print("✅ ML model loaded successfully")

    # Test with sample survey data
    test_surveys = [
        {
            "name": "Gaming User with High-end Phone",
            "data": {
                "phone_model": "iPhone (13/14/15 Pro Max)",
                "gender": "Laki-laki",
                "reason": "Mencari internet yang stabil",
                "call_frequency": "Jarang",
                "wifi": "Ya dirumah",
                "housing": "Rumah pribadi",
                "usage": ["Gaming online", "Streaming video (YouTube, Netflix, dll.)"],
                "quota": "50–100 GB",
                "budget": "Rp.100.000–Rp250.000",
                "preference": "Kuota besar",
                "roaming": "Tidak"
            }
        },
        {
            "name": "Budget User with Mid-range Phone",
            "data": {
                "phone_model": "Xiaomi Redmi Note Series",
                "gender": "Perempuan",
                "reason": "Mencari internet yang murah",
                "call_frequency": "Sering",
                "wifi": "Tidak",
                "housing": "Kost/kontrakan",
                "usage": ["Browsing & media sosial"],
                "quota": "< 10 GB",
                "budget": "< Rp25.000",
                "preference": "Hemat/entry-level",
                "roaming": "Tidak"
            }
        },
        {
            "name": "Business User with Samsung Galaxy",
            "data": {
                "phone_model": "Samsung Galaxy S Series",
                "gender": "Laki-laki",
                "reason": "Mencari internet yang stabil",
                "call_frequency": "Sering",
                "wifi": "Ya di kantor",
                "housing": "Apartemen",
                "usage": ["Video conference (Zoom, Teams, dll.)", "Browsing & media sosial"],
                "quota": "25-50 GB",
                "budget": "Rp.100.000–Rp250.000",
                "preference": "Unlimited",
                "roaming": "Kadang"
            }
        }
    ]

    # Test each survey
    for i, test_case in enumerate(test_surveys, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 40)

        try:
            # Preprocess survey data
            features = integrator.preprocess_survey_data(test_case['data'])
            if features is not None:
                print(f"✅ Survey data preprocessed successfully")
                print(f"   Feature vector shape: {features.shape}")

                # Get recommendations
                recommendations = integrator.get_top_recommendations(test_case['data'], top_k=3)

                if recommendations:
                    print(f"✅ Generated {len(recommendations)} recommendations:")
                    for j, rec in enumerate(recommendations, 1):
                        print(f"   {j}. {rec['name']} - {rec['kuota']} - Rp {rec['harga']:,}")
                        print(f"      Confidence: {rec['ml_confidence']*100:.1f}%")
                else:
                    print("⚠️  No recommendations generated")
            else:
                print("❌ Failed to preprocess survey data")

        except Exception as e:
            print(f"❌ Error processing test case: {e}")

    print("\n" + "=" * 50)
    print("🎯 ML Model Integration Test Complete")
    return True

def test_server_integration():
    """Test the full server integration"""
    print("\n🌐 Testing Server Integration")
    print("=" * 50)

    try:
        import requests
        import json

        # Test server endpoints
        base_url = "http://localhost:8000"

        # Test packages endpoint
        print("📦 Testing /api/packages endpoint...")
        response = requests.get(f"{base_url}/api/packages", timeout=5)
        if response.status_code == 200:
            packages = response.json()
            print(f"✅ Retrieved {len(packages)} packages")
        else:
            print(f"⚠️  Server returned status {response.status_code}")

        # Test recommendation endpoint
        print("\n🤖 Testing /api/recommend endpoint...")
        test_data = {
            "phone_model": "iPhone (13/14/15 Pro Max)",
            "gender": "Laki-laki",
            "reason": "Mencari internet yang stabil",
            "call_frequency": "Jarang",
            "wifi": "Ya dirumah",
            "housing": "Rumah pribadi",
            "usage": ["Gaming online", "Streaming video (YouTube, Netflix, dll.)"],
            "quota": "50–100 GB",
            "budget": "Rp.100.000–Rp250.000",
            "preference": "Kuota besar",
            "roaming": "Tidak"
        }

        response = requests.post(
            f"{base_url}/api/recommend",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ Recommendations received: {len(result['recommendations'])} packages")
                print(f"   ML Model Used: {result['metadata']['ml_model_used']}")
                print(f"   Recommendation Source: {result['metadata']['recommendation_source']}")
            else:
                print(f"❌ API returned error: {result.get('error')}")
        else:
            print(f"⚠️  Server returned status {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python backend/recommendation_server.py")
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    # Test ML model integration
    ml_success = test_ml_model()

    # Test server integration (if server is running)
    test_server_integration()

    print(f"\n🏁 Testing complete!")
    print(f"ML Model Status: {'✅ Working' if ml_success else '❌ Not Available'}")
    print("\nTo start the full application:")
    print("   python start_app.py")
    print("\nOr start manually:")
    print("   python backend/recommendation_server.py")
    print("   Then open home-before.html in browser")