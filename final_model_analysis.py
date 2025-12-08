#!/usr/bin/env python3
"""
Final comprehensive analysis of the Telco recommendation model
"""

import pickle
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def analyze_model():
    model_path = "model_telco_recommendation.pkl"

    print("=" * 60)
    print("FINAL TELCO MODEL ANALYSIS")
    print("=" * 60)

    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found: {model_path}")
        return

    try:
        # Load the model
        print(f"[INFO] Loading model from {model_path}...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        print(f"[SUCCESS] Model loaded successfully!")
        print(f"\n[MODEL OVERVIEW]")
        print(f"  Type: {type(model).__name__}")
        print(f"  Module: {type(model).__module__}")

        # Check if it's a Pipeline
        if hasattr(model, 'named_steps'):
            print(f"\n[PIPELINE STRUCTURE]")
            print(f"  Steps: {len(model.named_steps)}")
            for name, step in model.named_steps.items():
                print(f"    - {name}: {type(step).__name__}")

                # If this is the classifier
                if hasattr(step, 'classes_'):
                    print(f"      Classes: {list(step.classes_)}")
                if hasattr(step, 'feature_names_in_'):
                    print(f"      Features: {list(step.feature_names_in_)}")

        else:
            # Direct model
            print(f"\n[MODEL DETAILS]")
            if hasattr(model, 'n_estimators'):
                print(f"  Type: Random Forest")
                print(f"  Trees: {model.n_estimators}")
            elif hasattr(model, 'tree_'):
                print(f"  Type: Decision Tree")
                if hasattr(model.tree_, 'node_count'):
                    print(f"  Nodes: {model.tree_.node_count}")
                if hasattr(model.tree_, 'max_depth'):
                    print(f"  Max Depth: {model.tree_.max_depth}")

            # Get classes
            if hasattr(model, 'classes_'):
                print(f"\n[OUTPUT CLASSES] ({len(model.classes_)} classes)")
                for i, cls in enumerate(model.classes_):
                    print(f"  Class {i}: {cls}")

            # Get feature names
            if hasattr(model, 'feature_names_in_'):
                print(f"\n[INPUT FEATURES] ({len(model.feature_names_in_)} features)")
                for i, feature in enumerate(model.feature_names_in_):
                    print(f"  {i+1:2d}. {feature}")

            # Feature importances
            if hasattr(model, 'feature_importances_'):
                print(f"\n[FEATURE IMPORTANCES]")
                importances = model.feature_importances_
                if hasattr(model, 'feature_names_in_'):
                    # Pair features with importances
                    feature_imp = list(zip(model.feature_names_in_, importances))
                    feature_imp.sort(key=lambda x: x[1], reverse=True)
                    for feature, imp in feature_imp:
                        print(f"  {feature:20s}: {imp:.4f}")
                else:
                    for i, imp in enumerate(importances):
                        print(f"  Feature {i}: {imp:.4f}")

        # Test with sample data
        print(f"\n[SAMPLE PREDICTION TEST]")

        # Expected features from survey
        survey_features = [
            'phone_model', 'gender', 'reason', 'call_frequency', 'wifi',
            'housing', 'usage', 'quota', 'budget', 'preference', 'roaming'
        ]

        # Create sample data
        sample_data = {}
        sample_values = [
            ('phone_model', 'iPhone 14 Pro'),
            ('gender', 'Male'),
            ('reason', 'Internet stabil'),
            ('call_frequency', '100-200 menit/hari'),
            ('wifi', 'Rumah'),
            ('housing', 'Rumah'),
            ('usage', 'Browsing, Streaming'),
            ('quota', '20GB'),
            ('budget', 'Rp50.000-Rp100.000'),
            ('preference', 'Kuota besar'),
            ('roaming', 'Tidak')
        ]

        for key, value in sample_values:
            sample_data[key] = value

        print(f"  Sample input:")
        for key, value in sample_values:
            print(f"    {key}: {value}")

        # Try to make a prediction
        try:
            # Prepare input based on model expectations
            if hasattr(model, 'feature_names_in_'):
                # Use the model's expected feature order
                input_array = []
                for feature in model.feature_names_in_:
                    input_array.append(sample_data.get(feature, ''))

                # Convert to numpy array
                input_array = np.array([input_array])

                print(f"\n  Input shape: {input_array.shape}")
                print(f"  Input features order: {list(model.feature_names_in_)}")

                # Make prediction
                prediction = model.predict(input_array)[0]
                print(f"\n  Prediction: {prediction}")

                # Get probabilities if available
                if hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(input_array)[0]
                    print(f"\n  Class Probabilities:")
                    for i, (cls, prob) in enumerate(zip(model.classes_, probabilities)):
                        print(f"    {cls}: {prob:.4f}")

        except Exception as e:
            print(f"  [ERROR] Prediction failed: {str(e)}")
            print(f"  Note: This might be due to categorical encoding requirements")

        print(f"\n" + "=" * 60)
        print("INTEGRATION RECOMMENDATIONS")
        print("=" * 60)

        print(f"\n1. MODEL REQUIREMENTS:")
        print(f"   - Input features: {survey_features}")
        print(f"   - Output: Package recommendation")
        if hasattr(model, 'classes_'):
            print(f"   - Possible outputs: {list(model.classes_)}")

        print(f"\n2. PREPROCESSING NEEDED:")
        print(f"   - Categorical encoding for text features")
        print(f"   - Feature ordering must match model.feature_names_in_")
        print(f"   - Consider using a Pipeline with preprocessing steps")

        print(f"\n3. INTEGRATION STEPS:")
        print(f"   Step 1: Create a mapping from survey responses to encoded values")
        print(f"   Step 2: Load the model on server startup")
        print(f"   Step 3: Transform incoming survey data")
        print(f"   Step 4: Make prediction using model.predict()")
        print(f"   Step 5: Map prediction back to package name")

        print(f"\n4. COMPATIBILITY WITH CURRENT BACKEND:")
        print(f"   - Current backend uses rule-based scoring")
        print(f"   - Can be modified to use ML model instead")
        print(f"   - Location: backend/recommendation_server.py")
        print(f"   - Modify: RecommendationEngine.get_recommendations() method")

        return model

    except Exception as e:
        print(f"[ERROR] Failed to analyze model: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    model = analyze_model()