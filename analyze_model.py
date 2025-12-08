#!/usr/bin/env python3
"""
Script to analyze the Telco recommendation model
"""

import pickle
import os

# Try to import numpy, but don't fail if it's not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("WARNING: NumPy not installed - some features may be limited")

def analyze_model():
    model_path = "model_telco_recommendation.pkl"

    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found at: {model_path}")
        print(f"Current directory: {os.getcwd()}")
        return None

    try:
        # Load the model
        print(f"[INFO] Loading model from: {model_path}")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        print(f"\n[SUCCESS] Model loaded successfully!")
        print(f"[INFO] Model type: {type(model)}")

        # Check if it's a scikit-learn model
        if hasattr(model, '__class__'):
            print(f"🔧 Model class: {model.__class__.__module__}.{model.__class__.__name__}")

        # Check for common scikit-learn attributes
        sklearn_attributes = [
            'feature_names_in_', 'n_features_in_', 'classes_', 'coef_',
            'feature_importances_', 'tree_', 'estimators_', 'named_steps'
        ]

        print("\n📋 Model Attributes:")
        for attr in sklearn_attributes:
            if hasattr(model, attr):
                value = getattr(model, attr)
                print(f"  ✓ {attr}: {type(value)} - {value if len(str(value)) < 100 else str(type(value))}")

        # Check for Pipeline
        if hasattr(model, 'named_steps') and model.named_steps:
            print(f"\n🔄 Pipeline Steps:")
            for name, step in model.named_steps.items():
                print(f"  - {name}: {type(step).__name__}")
                if hasattr(step, 'categories_'):
                    print(f"    Categories: {step.categories_}")
                if hasattr(step, 'n_features_in_'):
                    print(f"    Features: {step.n_features_in_}")

        # Check for feature names
        if hasattr(model, 'feature_names_in_'):
            print(f"\n📝 Expected Features ({len(model.feature_names_in_)}):")
            for i, feature in enumerate(model.feature_names_in_):
                print(f"  {i+1}. {feature}")

        # Check for classes
        if hasattr(model, 'classes_'):
            print(f"\n🏷️  Output Classes ({len(model.classes_)}):")
            for i, cls in enumerate(model.classes_):
                print(f"  {i}. {cls}")

        # Check methods
        predict_methods = ['predict', 'predict_proba', 'decision_function', 'transform']
        print(f"\n⚙️  Available Methods:")
        for method in predict_methods:
            if hasattr(model, method):
                print(f"  ✓ {method}")

        # Try to get model parameters
        if hasattr(model, 'get_params'):
            try:
                params = model.get_params()
                print(f"\n📐 Model Parameters:")
                for key, value in params.items():
                    if not key.endswith('_') and len(str(value)) < 100:
                        print(f"  {key}: {value}")
            except:
                pass

        return model

    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_model_prediction(model):
    """Test model with sample data based on survey questions"""

    # Expected features based on survey questions
    expected_features = [
        'phone_model', 'gender', 'reason', 'call_frequency', 'wifi',
        'housing', 'usage', 'quota', 'budget', 'preference', 'roaming'
    ]

    print(f"\n🧪 Testing Model with Sample Data:")
    print(f"Expected features based on survey: {expected_features}")

    # Create sample test data
    test_data = {
        'phone_model': 'iPhone 14 Pro',
        'gender': 'Male',
        'reason': 'Internet stabil',
        'call_frequency': '100-200 menit/hari',
        'wifi': 'Rumah',
        'housing': 'Rumah',
        'usage': 'Browsing, Streaming',
        'quota': '20GB',
        'budget': 'Rp50.000-Rp100.000',
        'preference': 'Kuota besar',
        'roaming': 'Tidak'
    }

    print(f"\n📝 Sample survey data:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")

    # Try different input formats
    print(f"\n🔄 Testing different input formats:")

    # Test 1: Dictionary input
    try:
        if hasattr(model, 'predict'):
            result = model.predict([test_data])
            print(f"✅ Dictionary input successful: {result}")
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([test_data])
                print(f"📊 Probabilities: {proba}")
    except Exception as e:
        print(f"❌ Dictionary input failed: {str(e)}")

    # Test 2: Array input (if we know feature order)
    if hasattr(model, 'feature_names_in_'):
        try:
            # Convert dictionary to array in correct order
            array_input = [test_data.get(feature, '') for feature in model.feature_names_in_]
            result = model.predict([array_input])
            print(f"✅ Array input successful: {result}")
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([array_input])
                print(f"📊 Probabilities: {proba}")
        except Exception as e:
            print(f"❌ Array input failed: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 TELCO MODEL ANALYSIS")
    print("=" * 60)

    model = analyze_model()

    if model:
        test_model_prediction(model)

        print("\n" + "=" * 60)
        print("📝 INTEGRATION GUIDELINES:")
        print("=" * 60)

        print("\n1. Model Input Format:")
        print("   - The model expects features in a specific format")
        print("   - Based on the analysis, features should be:")
        print("     phone_model, gender, reason, call_frequency, wifi,")
        print("     housing, usage, quota, budget, preference, roaming")

        print("\n2. Preprocessing Requirements:")
        print("   - Categorical encoding may be needed")
        print("   - Features may need to be in a specific order")
        print("   - Check if the model has a pipeline with preprocessing")

        print("\n3. Integration Steps:")
        print("   a) Collect survey data from frontend")
        print("   b) Transform data to match model's expected format")
        print("   c) Use model.predict() for recommendations")
        print("   d) Use model.predict_proba() if confidence scores needed")

        print("\n4. Current Implementation:")
        print("   - The backend uses a rule-based scoring system")
        print("   - Consider replacing or combining with ML model predictions")
        print("   - Modify recommendation_server.py to integrate the model")