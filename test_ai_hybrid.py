#!/usr/bin/env python3
"""
Test the AI Model + Survey Hybrid System
"""

import requests
import json
import time

def test_ai_hybrid_system():
    """Test the hybrid AI + Survey recommendation system"""

    print("Testing AI Model + Survey Hybrid System")
    print("=" * 60)

    base_url = "http://localhost:8000"

    # Test server health
    print("\n1. Checking Server Health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server Status: {health['status']}")
            print(f"   AI Model Available: {health.get('ml_model_available', False)}")
            print(f"   Survey Analyzer Available: {health.get('survey_analyzer_available', False)}")
            print(f"   Hybrid Engine: {health.get('hybrid_engine', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Start the server with: python backend/simple_ml_server.py")
        return False

    # Test different user types
    test_cases = [
        {
            "name": "Premium Gamer",
            "data": {
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
                "roaming": "Kadang"
            }
        },
        {
            "name": "Budget User",
            "data": {
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
        },
        {
            "name": "Business Professional",
            "data": {
                "phone_model": "Samsung Galaxy S Series",
                "gender": "Laki-laki",
                "reason": "Mencari internet yang stabil",
                "call_frequency": "Sering",
                "wifi": "Ya di kantor",
                "housing": "Apartemen",
                "usage": ["Video conference (Zoom, Teams, dll.)", "Gaming online"],
                "quota": "25-50 GB",
                "budget": "Rp.100.000–Rp250.000",
                "preference": "Kuota besar",
                "roaming": "Sering"
            }
        }
    ]

    all_tests_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}...")

        try:
            response = requests.post(
                f"{base_url}/api/recommend",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    recommendations = result['recommendations']
                    metadata = result.get('metadata', {})

                    print(f"   ✅ Response received successfully")
                    print(f"   📊 Total Recommendations: {len(recommendations)}")
                    print(f"   🧠 AI Model: {metadata.get('ml_count', 0)} packages")
                    print(f"   📊 Survey Analysis: {metadata.get('survey_count', 0)} packages")

                    # Analyze recommendations
                    ai_recs = [r for r in recommendations if r.get('recommendation_type') == 'ml_model']
                    survey_recs = [r for r in recommendations if r.get('recommendation_type') == 'survey_based']

                    print(f"\n   🎯 Top Recommendations for {test_case['name']}:")
                    for j, rec in enumerate(recommendations[:3], 1):
                        rec_type = "🤖 AI" if rec.get('recommendation_type') == 'ml_model' else "📋 Survey"
                        match = rec.get('match_percentage', 0)

                        print(f"      {j}. {rec_type} - {rec.get('name', 'Unknown')}")
                        print(f"         Match: {match}%")
                        print(f"         Price: Rp {rec.get('harga', 0):,}")

                        if rec.get('ml_score'):
                            print(f"         ML Score: {rec.get('ml_score', 0)*100:.1f}")
                        if rec.get('survey_score'):
                            print(f"         Survey Score: {rec.get('survey_score', 0)*100:.1f}")

                else:
                    print(f"   ❌ Response failed: {result.get('error', 'Unknown error')}")
                    all_tests_passed = False

            else:
                print(f"   ❌ HTTP error: {response.status_code}")
                all_tests_passed = False

        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_tests_passed = False

    print("\n" + "=" * 60)
    print("🎯 AI + HYBRID SYSTEM TEST COMPLETE")
    print("=" * 60)

    if all_tests_passed:
        print("✅ All tests passed! 🎉")
        print("\n📱 What you'll see in the frontend:")
        print("   🧠 AI Model recommendations with green borders")
        print("   📋 Survey Analysis recommendations with blue borders")
        print("   🏷️  Clear labels: 'AI Model' and 'Survey Analysis'")
        print("   🎯 Unified display showing all recommendations together")
    else:
        print("❌ Some tests failed")

    print("\n🚀 To see it in action:")
    print("   1. Start server: python backend/simple_ml_server.py")
    print("   2. Open home-before.html in browser")
    print("   3. Take the survey with different phone models")
    print("   4. See the AI + Survey hybrid recommendations!")

    return all_tests_passed

if __name__ == "__main__":
    print("Starting AI Model + Survey Hybrid Test...")
    print("This test will verify the hybrid recommendation system")
    print()

    time.sleep(2)

    test_ai_hybrid_system()