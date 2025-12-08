#!/usr/bin/env python3
"""
Test the Hybrid Recommendation System
Verifies that ML recommendations come first, followed by survey-based recommendations
"""

import requests
import json
import time

def test_hybrid_recommendations():
    """Test the hybrid recommendation system"""

    print("🧪 Testing Hybrid Recommendation System")
    print("=" * 60)

    base_url = "http://localhost:8000"

    # Test 1: Check server health
    print("\n1️⃣ Checking Server Health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server Status: {health['status']}")
            print(f"   ML Model Available: {health.get('ml_model_available', False)}")
            print(f"   Model Type: {health.get('model_type', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Start the server with: python backend/recommendation_server_fixed.py")
        return False

    # Test 2: High-end user - should get ML recommendations first
    print("\n2️⃣ Testing High-end Phone + High Budget (ML Priority)...")
    premium_user_data = {
        "phone_model": "iPhone (13/14/15 Pro Max)",
        "gender": "Laki-laki",
        "reason": "Mencari internet yang stabil",
        "call_frequency": "Jarang",
        "wifi": "Ya dirumah",
        "housing": "Rumah pribadi",
        "usage": ["Gaming online", "Streaming video (YouTube, Netflix, dll.)", "Video conference"],
        "quota": "50–100 GB",
        "budget": "> Rp250.000",
        "preference": "Kuota besar",
        "roaming": "Sering"
    }

    response = requests.post(
        f"{base_url}/api/recommend",
        json=premium_user_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        analyze_hybrid_result(result, "Premium User")
    else:
        print(f"❌ Premium user test failed: {response.status_code}")

    # Test 3: Budget user - should get ML + survey recommendations
    print("\n3️⃣ Testing Budget Phone + Low Budget (Hybrid)...")
    budget_user_data = {
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
        json=budget_user_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        analyze_hybrid_result(result, "Budget User")
    else:
        print(f"❌ Budget user test failed: {response.status_code}")

    # Test 4: Business user - should get ML + survey
    print("\n4️⃣ Testing Business User (Comprehensive)...")
    business_user_data = {
        "phone_model": "Samsung Galaxy S Series",
        "gender": "Laki-laki",
        "reason": "Mencari internet yang stabil",
        "call_frequency": "Sering",
        "wifi": "Ya di kantor",
        "housing": "Apartemen",
        "usage": ["Video conference (Zoom, Teams, dll.)", "Gaming online", "Smart home / IoT"],
        "quota": "25-50 GB",
        "budget": "Rp.100.000–Rp250.000",
        "preference": "Kuota besar",
        "roaming": "Kadang"
    }

    response = requests.post(
        f"{base_url}/api/recommend",
        json=business_user_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        analyze_hybrid_result(result, "Business User")
    else:
        print(f"❌ Business user test failed: {response.status_code}")

    print("\n" + "=" * 60)
    print("🎯 HYBRID SYSTEM ANALYSIS COMPLETE")
    print("=" * 60)
    print("\n📊 What to expect in the frontend:")
    print("1. 📋 ML recommendations appear first with green badges")
    print("2. 📈 Survey-based recommendations follow with blue badges")
    print("3. 🔍 Priority ranking (#1, #2) for top ML recommendations")
    print("4. 📊 Confidence scores for ML recommendations")
    print("5. 💡 Analysis tooltips for survey-based recommendations")

def analyze_hybrid_result(result, user_type):
    """Analyze the hybrid recommendation result"""
    recommendations = result.get('recommendations', [])
    metadata = result.get('metadata', {})

    print(f"📊 {user_type} Analysis:")
    print(f"   Total Recommendations: {len(recommendations)}")
    print(f"   ML Model Used: {metadata.get('ml_model_used', False)}")

    # Count recommendation types
    ml_count = sum(1 for r in recommendations if r.get('recommendation_type') == 'ml_model')
    survey_count = sum(1 for r in recommendations if r.get('recommendation_type') == 'survey_based')

    print(f"   ML Recommendations: {ml_count}")
    print(f"   Survey-Based: {survey_count}")

    # Check ordering (ML should come first)
    if ml_count > 0 and survey_count > 0:
        ml_positions = [i for i, r in enumerate(recommendations) if r.get('recommendation_type') == 'ml_model']
        survey_positions = [i for i, r in enumerate(recommendations) if r.get('recommendation_type') == 'survey_based']

        if max(ml_positions) < min(survey_positions):
            print("   ✅ Correct ordering: ML recommendations first, then survey-based")
        else:
            print("   ⚠️  Ordering issue: ML and survey recommendations are mixed")

    # Show top recommendations
    print(f"   Top 3 Recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        rec_type = rec.get('recommendation_type', 'unknown')
        confidence = rec.get('model_confidence', 0)
        match = rec.get('match_percentage', 0)

        type_icon = "🤖" if rec_type == 'ml_model' else "📋"
        confidence_text = f" (Confidence: {confidence*100:.1f}%)" if confidence > 0 else ""

        print(f"     {i}. {type_icon} {rec['name']} - {match}% match{confidence_text}")

if __name__ == "__main__":
    print("🚀 Starting Hybrid Recommendation System Test...")
    print("Make sure the server is running:")
    print("python backend/recommendation_server_fixed.py")
    print()

    time.sleep(2)

    test_hybrid_recommendations()

    print("\n💡 Next steps:")
    print("1. Open home-before.html in your browser")
    print("2. Take the survey with different user profiles")
    print("3. Observe the hybrid recommendation system in action!")
    print("4. Check for green ML badges and blue survey badges")