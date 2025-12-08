#!/usr/bin/env python3
"""
Script to analyze the Telco recommendation model
"""

import pickle
import os
import sys

def analyze_model():
    model_path = "model_telco_recommendation.pkl"

    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found at: {model_path}")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for f in os.listdir('.'):
            if f.endswith('.pkl'):
                print(f"  - {f}")
        return None

    try:
        # Load the model
        print(f"[INFO] Loading model from: {model_path}")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        print(f"\n[SUCCESS] Model loaded successfully!")
        print(f"[INFO] Model type: {type(model)}")
        print(f"[INFO] Model module: {type(model).__module__}")
        print(f"[INFO] Model class: {type(model).__name__}")

        # Check if it's a scikit-learn model
        if hasattr(model, '__class__'):
            print(f"[INFO] Full class path: {model.__class__.__module__}.{model.__class__.__name__}")

        # List all attributes
        print(f"\n[ATTRIBUTES] Model has {len(dir(model))} attributes")
        important_attrs = []
        for attr in dir(model):
            if not attr.startswith('_'):
                important_attrs.append(attr)
                if len(important_attrs) <= 20:  # Show first 20
                    value = getattr(model, attr)
                    print(f"  - {attr}: {type(value).__name__}")

        # Check for common scikit-learn attributes
        sklearn_attributes = [
            'feature_names_in_', 'n_features_in_', 'classes_', 'coef_',
            'feature_importances_', 'tree_', 'estimators_', 'named_steps',
            'steps', 'transformer', 'classifier', 'regressor'
        ]

        print(f"\n[SCIKIT-LEARN ATTRIBUTES]")
        found_attrs = []
        for attr in sklearn_attributes:
            if hasattr(model, attr):
                value = getattr(model, attr)
                found_attrs.append(attr)
                print(f"  FOUND - {attr}: {type(value)}")
                if hasattr(value, '__len__') and len(str(value)) < 200:
                    print(f"    Value: {value}")

        # Check for Pipeline
        if hasattr(model, 'named_steps') and model.named_steps:
            print(f"\n[PIPELINE STEPS]")
            for name, step in model.named_steps.items():
                print(f"  Step '{name}': {type(step).__name__}")
                if hasattr(step, 'categories_'):
                    print(f"    Categories: {step.categories_}")
                if hasattr(step, 'n_features_in_'):
                    print(f"    Features: {step.n_features_in_}")
                if hasattr(step, 'feature_names_in_'):
                    print(f"    Feature names: {step.feature_names_in_}")

        # Check for feature names
        if hasattr(model, 'feature_names_in_'):
            print(f"\n[FEATURE NAMES] ({len(model.feature_names_in_)} features)")
            for i, feature in enumerate(model.feature_names_in_):
                print(f"  {i+1}. {feature}")

        # Check for classes
        if hasattr(model, 'classes_'):
            print(f"\n[OUTPUT CLASSES] ({len(model.classes_)} classes)")
            for i, cls in enumerate(model.classes_):
                print(f"  Class {i}: {cls}")

        # Check methods
        predict_methods = ['predict', 'predict_proba', 'decision_function', 'transform', 'fit', 'score']
        print(f"\n[METHODS]")
        for method in predict_methods:
            if hasattr(model, method):
                print(f"  AVAILABLE - {method}")

        # Try to get model parameters
        if hasattr(model, 'get_params'):
            try:
                params = model.get_params(deep=False)
                print(f"\n[PARAMETERS] (shallow)")
                for key, value in params.items():
                    if not key.endswith('_'):
                        print(f"  {key}: {value}")
            except Exception as e:
                print(f"  Error getting params: {e}")

        # Try to inspect what the model was trained on
        print(f"\n[INSPECTION]")
        if hasattr(model, 'X_'):
            print(f"  Has X_ (training data): {type(model.X_)}")
        if hasattr(model, 'y_'):
            print(f"  Has y_ (training labels): {type(model.y_)}")
        if hasattr(model, '_estimator'):
            print(f"  Has _estimator: {type(model._estimator)}")

        return model

    except Exception as e:
        print(f"[ERROR] Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_model_structure(model):
    """Try to understand the model structure"""
    print(f"\n[STRUCTURE ANALYSIS]")

    # Check if it's a Pipeline
    if type(model).__name__ == 'Pipeline':
        print("Model is a scikit-learn Pipeline")
        if hasattr(model, 'steps'):
            print(f"  Steps: {len(model.steps)}")
            for i, (name, step) in enumerate(model.steps):
                print(f"    Step {i}: {name} -> {type(step).__name__}")

    # Check if it's wrapped
    if hasattr(model, 'estimator'):
        print(f"  Has nested estimator: {type(model.estimator)}")

    # Try to understand the expected input
    if hasattr(model, 'feature_names_in_'):
        print(f"\n[EXPECTED INPUT FORMAT]")
        print(f"  Features required: {list(model.feature_names_in_)}")
        print(f"  Number of features: {len(model.feature_names_in_)}")

def main():
    print("=" * 60)
    print("TELCO MODEL ANALYSIS")
    print("=" * 60)

    model = analyze_model()

    if model:
        test_model_structure(model)

        print("\n" + "=" * 60)
        print("INTEGRATION GUIDELINES:")
        print("=" * 60)

        print("\n1. Model Input Format:")
        print("   - Collect all survey fields:")
        survey_fields = [
            "phone_model", "gender", "reason", "call_frequency",
            "wifi", "housing", "usage", "quota", "budget",
            "preference", "roaming"
        ]
        for field in survey_fields:
            print(f"     - {field}")

        print("\n2. Integration with current backend:")
        print("   - Current backend uses rule-based scoring")
        print("   - Option 1: Replace with ML model predictions")
        print("   - Option 2: Combine both (hybrid approach)")
        print("   - Option 3: Use ML model as fallback")

        print("\n3. Implementation steps:")
        print("   a) Load model on server start")
        print("   b) Transform survey data to match model format")
        print("   c) Call model.predict() for recommendations")
        print("   d) Format output to match frontend expectations")

        print("\n4. Preprocessing considerations:")
        print("   - May need categorical encoding")
        print("   - May need feature scaling")
        print("   - Check if model includes preprocessing pipeline")

if __name__ == "__main__":
    main()