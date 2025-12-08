#!/usr/bin/env python3
"""
Example of how to integrate the ML model with the survey system
This is a template showing the expected data flow
"""

import json
import numpy as np

# Example survey data structure
EXAMPLE_SURVEY_DATA = {
    "phone_model": "iPhone 14 Pro",
    "gender": "Male",
    "reason": "Internet stabil",
    "call_frequency": "100-200 menit/hari",
    "wifi": "Rumah",
    "housing": "Rumah",
    "usage": ["Browsing", "Streaming"],
    "quota": "20GB",
    "budget": "Rp50.000-Rp100.000",
    "preference": "Kuota besar",
    "roaming": "Tidak"
}

# Available packages (from backend)
AVAILABLE_PACKAGES = [
    {"name": "Sphinx Stable 20GB", "kuota": "20GB", "harga": 40000, "category": "stable"},
    {"name": "Sphinx Stable 50GB", "kuota": "50GB", "harga": 75000, "category": "stable"},
    {"name": "Sphinx Stable 100GB", "kuota": "100GB", "harga": 120000, "category": "stable"},
    {"name": "Sphinx Hemat 5GB", "kuota": "5GB", "harga": 25000, "category": "hemat"},
    {"name": "Sphinx Hemat 10GB", "kuota": "10GB", "harga": 35000, "category": "hemat"},
    {"name": "Sphinx Hemat 20GB", "kuota": "20GB", "harga": 45000, "category": "hemat"},
    {"name": "Sphinx Hemat 30GB", "kuota": "30GB", "harga": 55000, "category": "hemat"},
    {"name": "Sphinx Unlimited", "kuota": "Unlimited", "harga": 250000, "category": "unlimited"},
    {"name": "Sphinx Call Pro", "kuota": "300 Menit", "harga": 50000, "category": "call"},
    {"name": "Sphinx Call Flex", "kuota": "150 Menit", "harga": 30000, "category": "call"},
    {"name": "Sphinx Call Lite", "kuota": "60 Menit", "harga": 15000, "category": "call"},
    {"name": "Sphinx Social 10GB", "kuota": "10GB", "harga": 20000, "category": "social"},
    {"name": "Sphinx Stream 50GB", "kuota": "50GB", "harga": 70000, "category": "stream"},
    {"name": "Sphinx Stream 100GB", "kuota": "100GB", "harga": 120000, "category": "stream"},
    {"name": "Sphinx Work Connect 30GB", "kuota": "30GB", "harga": 55000, "category": "work"},
    {"name": "Sphinx Gamer Pro 40GB", "kuota": "40GB", "harga": 65000, "category": "gaming"},
    {"name": "Sphinx Gamer Max 80GB", "kuota": "80GB", "harga": 110000, "category": "gaming"},
    {"name": "Sphinx IoT Home 20GB", "kuota": "20GB", "harga": 30000, "category": "iot"},
    {"name": "Sphinx IoT Fiber 30 Mbps", "kuota": "Fiber IoT", "harga": 150000, "category": "iot"},
    {"name": "Sphinx Global Lite", "kuota": "1GB", "harga": 75000, "category": "roaming"},
    {"name": "Sphinx Global Pass", "kuota": "3GB", "harga": 150000, "category": "roaming"},
    {"name": "Sphinx Roam Max", "kuota": "10GB", "harga": 350000, "category": "roaming"}
]

def preprocess_survey_data(survey_data):
    """
    Preprocess survey data for ML model
    This is a template - actual encoding depends on training data
    """
    processed = {}

    # Handle categorical encoding
    # Example mappings (these should match the training data encoding)

    # Phone model categories
    phone_categories = {
        'iPhone': 'Apple',
        'Samsung': 'Samsung',
        'Xiaomi': 'Xiaomi',
        'OPPO': 'OPPO',
        'Vivo': 'Vivo',
        'Realme': 'Realme',
        'Other': 'Other'
    }

    # Gender
    gender_map = {
        'Male': 'M',
        'Female': 'F',
        'Other': 'O'
    }

    # Budget ranges (convert to numeric)
    budget_map = {
        "< Rp25.000": 25000,
        "Rp25.000–Rp50.000": 37500,
        "Rp.50.000-Rp100.000": 75000,
        "Rp.100.000–Rp250.000": 175000,
        "> Rp250.000": 300000
    }

    # Usage patterns
    usage_map = {
        'Browsing': 1,
        'Streaming': 2,
        'Gaming': 3,
        'Social Media': 4,
        'Work': 5,
        'Conference': 6
    }

    # Apply transformations
    processed['phone_model'] = categorize_phone(survey_data['phone_model'])
    processed['gender'] = gender_map.get(survey_data['gender'], 'O')
    processed['reason'] = survey_data['reason'].lower()
    processed['call_frequency'] = extract_numeric_calls(survey_data['call_frequency'])
    processed['wifi'] = survey_data['wifi']
    processed['housing'] = survey_data['housing']
    processed['usage'] = ','.join(survey_data.get('usage', []))
    processed['quota'] = extract_numeric_quota(survey_data['quota'])
    processed['budget'] = budget_map.get(survey_data['budget'], 75000)
    processed['preference'] = survey_data['preference'].lower()
    processed['roaming'] = survey_data['roaming']

    return processed

def categorize_phone(phone_model):
    """Categorize phone model"""
    phone_lower = phone_model.lower()
    if 'iphone' in phone_lower:
        return 'Apple'
    elif 'galaxy' in phone_lower or 'samsung' in phone_lower:
        return 'Samsung'
    elif 'xiaomi' in phone_lower or 'redmi' in phone_lower:
        return 'Xiaomi'
    elif 'oppo' in phone_lower:
        return 'OPPO'
    elif 'vivo' in phone_lower:
        return 'Vivo'
    elif 'realme' in phone_lower:
        return 'Realme'
    else:
        return 'Other'

def extract_numeric_calls(call_freq):
    """Extract numeric value from call frequency"""
    if '100-200' in call_freq:
        return 150
    elif '50-100' in call_freq:
        return 75
    elif '< 50' in call_freq:
        return 25
    elif '> 200' in call_freq:
        return 250
    else:
        return 100

def extract_numeric_quota(quota_str):
    """Extract numeric quota value"""
    if 'GB' in quota_str:
        try:
            return int(quota_str.split('GB')[0])
        except:
            return 20
    elif 'Unlimited' in quota_str:
        return 999
    else:
        return 20

class MockMLModel:
    """Mock ML model for demonstration - replace with actual loaded model"""

    def __init__(self):
        # This would be loaded from pickle file
        # self.model = pickle.load(open('model_telco_recommendation.pkl', 'rb'))
        self.feature_names = [
            'phone_model', 'gender', 'reason', 'call_frequency', 'wifi',
            'housing', 'usage', 'quota', 'budget', 'preference', 'roaming'
        ]
        # Mock class labels (packages)
        self.classes_ = [pkg['name'] for pkg in AVAILABLE_PACKAGES[:5]]

    def predict(self, X):
        """Mock prediction - returns recommended package"""
        # In real implementation, this would use the loaded model
        # For demo, return based on budget
        budget = int(X[0][8])  # budget is at index 8

        if budget < 30000:
            return ['Sphinx Call Lite']
        elif budget < 50000:
            return ['Sphinx Hemat 10GB']
        elif budget < 100000:
            return ['Sphinx Stable 20GB']
        elif budget < 200000:
            return ['Sphinx Stream 50GB']
        else:
            return ['Sphinx Unlimited']

    def predict_proba(self, X):
        """Mock probability prediction"""
        prediction = self.predict(X)[0]
        probs = np.zeros(len(self.classes_))

        # Find index of predicted class
        if prediction in self.classes_:
            idx = self.classes_.index(prediction)
            probs[idx] = 0.8  # High confidence for predicted class

            # Distribute remaining probability
            remaining = 0.2
            for i in range(len(probs)):
                if i != idx:
                    probs[i] = remaining / (len(probs) - 1)

        return [probs]

def get_ml_recommendations(survey_data):
    """
    Get recommendations using ML model
    Template for actual implementation
    """
    # Preprocess the data
    processed_data = preprocess_survey_data(survey_data)

    # Create feature array in correct order
    feature_order = [
        'phone_model', 'gender', 'reason', 'call_frequency', 'wifi',
        'housing', 'usage', 'quota', 'budget', 'preference', 'roaming'
    ]

    features = []
    for feature in feature_order:
        features.append(processed_data.get(feature, 0))

    X = np.array([features])

    # Load model (in real implementation)
    model = MockMLModel()

    # Get predictions
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    # Format results
    results = []
    for i, (pkg, prob) in enumerate(zip(model.classes_, probabilities)):
        # Find package details
        pkg_details = next((p for p in AVAILABLE_PACKAGES if p['name'] == pkg), None)
        if pkg_details:
            results.append({
                'name': pkg,
                'probability': float(prob),
                'details': pkg_details
            })

    # Sort by probability
    results.sort(key=lambda x: x['probability'], reverse=True)

    return results

def main():
    """Demonstrate ML integration"""
    print("=" * 60)
    print("TELCO ML MODEL INTEGRATION EXAMPLE")
    print("=" * 60)

    print("\n1. INPUT SURVEY DATA:")
    print(json.dumps(EXAMPLE_SURVEY_DATA, indent=2))

    print("\n2. PREPROCESSED DATA:")
    processed = preprocess_survey_data(EXAMPLE_SURVEY_DATA)
    for key, value in processed.items():
        print(f"  {key}: {value}")

    print("\n3. ML RECOMMENDATIONS:")
    recommendations = get_ml_recommendations(EXAMPLE_SURVEY_DATA)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n  Recommendation #{i}:")
        print(f"    Package: {rec['name']}")
        print(f"    Confidence: {rec['probability']:.2%}")
        if rec['details']:
            print(f"    Price: Rp{rec['details']['harga']:,}")
            print(f"    Category: {rec['details']['category']}")

    print("\n4. INTEGRATION NOTES:")
    print("  - Replace MockMLModel with actual loaded model")
    print("  - Ensure categorical encoding matches training data")
    print("  - Handle edge cases and missing values")
    print("  - Consider using a Pipeline for preprocessing")
    print("  - Cache the model in memory for performance")

if __name__ == "__main__":
    main()