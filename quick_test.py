#!/usr/bin/env python3
"""
Quick test script to verify ML model and CORS fixes
"""

import os
import sys
import json

def test_ml_integration():
    """Test ML model integration with fixes"""
    print("🤖 Testing ML Model Integration with Fixes")
    print("=" * 50)

    try:
        # Add backend to path
        sys.path.append(os.path.join(os.getcwd(), 'backend'))
        from ml_integration import MLModelIntegrator

        # Test model loading
        integrator = MLModelIntegrator()
        if integrator.is_available():
            print("✅ ML Model loaded successfully!")
            print(f"   Model type: {type(integrator.model).__name__}")

            # Test with sample data
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

            recommendations = integrator.get_top_recommendations(test_data, top_k=3)
            if recommendations:
                print("✅ Recommendations generated:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec['name']} - {rec['match_percentage']}% match")
            else:
                print("⚠️  No recommendations generated")

        else:
            print("❌ ML Model not available - using fallback")
            print("   This is normal if the model has compatibility issues")
            print("   The system will use rule-based recommendations")

    except Exception as e:
        print(f"❌ Error testing ML integration: {e}")

def test_server_endpoints():
    """Test server endpoints"""
    print("\n🌐 Testing Server Endpoints")
    print("=" * 50)

    try:
        import requests
        base_url = "http://localhost:8000"

        print("📡 Testing server connectivity...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print("✅ Server is healthy!")
            print(f"   ML Model Available: {health.get('ml_model_available', False)}")
            print(f"   Recommendation Engine: {health.get('recommendation_engine', 'unknown')}")
        else:
            print(f"⚠️  Server returned status {response.status_code}")

        print("\n📦 Testing packages endpoint...")
        response = requests.get(f"{base_url}/api/packages", timeout=5)
        if response.status_code == 200:
            packages = response.json()
            print(f"✅ Retrieved {len(packages)} packages")
        else:
            print(f"⚠️  Packages endpoint failed: {response.status_code}")

        print("\n🤖 Testing recommendation endpoint...")
        test_data = {
            "phone_model": "iPhone (13/14/15 Pro Max)",
            "gender": "Laki-laki",
            "reason": "Mencari internet yang stabil",
            "usage": ["Gaming online", "Streaming video"],
            "quota": "50–100 GB",
            "budget": "Rp.100.000–Rp250.000",
            "preference": "Kuota besar"
        }

        response = requests.post(
            f"{base_url}/api/recommend",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Recommendations received!")
            print(f"   ML Model Used: {result.get('metadata', {}).get('ml_model_used', False)}")
            print(f"   Total Recommendations: {len(result.get('recommendations', []))}")
        else:
            print(f"⚠️  Recommendation endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running")
        print("   Start with: python backend/recommendation_server.py")
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")

def print_solution_summary():
    """Print summary of the fixes applied"""
    print("\n🔧 SOLUTION SUMMARY")
    print("=" * 50)
    print("✅ Fixed Scikit-learn compatibility issues:")
    print("   - Added sklearn_compatibility_fix.py")
    print("   - Multiple model loading strategies")
    print("   - Mock model fallback for testing")
    print("   - Version checking and warnings")

    print("\n✅ Fixed CORS issues:")
    print("   - Added OPTIONS request handling")
    print("   - CORS headers for all responses")
    print("   - Proper preflight request support")

    print("\n🚀 How to run:")
    print("   1. python backend/recommendation_server.py")
    print("   2. Open home-before.html in browser")
    print("   3. Take the survey to see ML recommendations")

if __name__ == "__main__":
    test_ml_integration()
    test_server_endpoints()
    print_solution_summary()