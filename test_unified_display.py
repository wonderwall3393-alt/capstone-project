#!/usr/bin/env python3
"""
Test the Unified Recommendation Display
Verifies that ML and survey-based recommendations are shown together
"""

import requests
import json

def test_unified_display():
    """Test the unified recommendation display"""

    print("🧪 Testing Unified Recommendation Display")
    print("=" * 50)

    base_url = "http://localhost:8000"

    # Test with comprehensive user data
    test_data = {
        "phone_model": "Samsung Galaxy S Series",
        "gender": "Laki-laki",
        "reason": "Mencari internet yang stabil",
        "call_frequency": "Sering",
        "wifi": "Ya di kantor",
        "housing": "Apartemen",
        "usage": ["Gaming online", "Video conference (Zoom, Teams, dll.)", "Smart home / IoT"],
        "quota": "25-50 GB",
        "budget": "Rp.100.000–Rp250.000",
        "preference": "Kuota besar",
        "roaming": "Kadang"
    }

    try:
        response = requests.post(
            f"{base_url}/api/recommend",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('recommendations', [])

            print(f"✅ Response received successfully")
            print(f"   Total Recommendations: {len(recommendations)}")

            # Count and categorize recommendations
            ml_recs = [r for r in recommendations if r.get('recommendation_type') == 'ml_model']
            survey_recs = [r for r in recommendations if r.get('recommendation_type') == 'survey_based']

            print(f"\n📊 Recommendation Breakdown:")
            print(f"   ML Model: {len(ml_recs)} packages")
            print(f"   Survey Analysis: {len(survey_recs)} packages")

            print(f"\n🎯 Unified Display (All recommendations together):")

            for i, rec in enumerate(recommendations, 1):
                rec_type = rec.get('recommendation_type', 'unknown')
                is_ml = rec_type == 'ml_model'

                type_label = "🤖 ML Model" if is_ml else "📋 Survey Analysis"
                match_percent = rec.get('match_percentage', 0)
                confidence = rec.get('model_confidence', 0)

                print(f"   {i}. {type_label}")
                print(f"      Package: {rec.get('name', 'Unknown')}")
                print(f"      Match: {match_percent}%")
                if confidence > 0:
                    print(f"      Confidence: {confidence*100:.1f}%")
                print(f"      Price: Rp {rec.get('harga', 0):,}")
                print()

            print(f"✅ Unified display test completed!")
            print(f"\n🎨 What you'll see in the frontend:")
            print(f"   - All packages in the same grid layout")
            print(f"   - Green borders for ML Model recommendations")
            print(f"   - Blue borders for Survey Analysis recommendations")
            print(f"   - Clear labels: 'ML Model' or 'Survey Analysis'")
            print(f"   - Mixed order (ML prioritized, then survey-based)")
            print(f"   - Single unified header showing counts")

        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the server is running: python backend/recommendation_server_fixed.py")

if __name__ == "__main__":
    print("🚀 Testing Unified Recommendation Display...")
    print("Starting test...")
    print()

    test_unified_display()

    print("\n💡 Next Steps:")
    print("1. Open home-before.html in your browser")
    print("2. Take the survey")
    print("3. Observe the unified recommendation grid")
    print("4. Look for mixed ML (green) and Survey (blue) cards")