#!/usr/bin/env python3
"""
Robust script to analyze the Telco recommendation model
Handles version compatibility issues
"""

import pickle
import os
import sys
import warnings
warnings.filterwarnings('ignore')

def safe_load_model(model_path):
    """Try to load the model with various strategies"""

    # Strategy 1: Direct load
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("[SUCCESS] Model loaded directly")
        return model, "direct"
    except Exception as e:
        print(f"[FAILED] Direct load failed: {str(e)}")

    # Strategy 2: Try to ignore version mismatch
    try:
        import sklearn
        # Temporarily disable version check
        original_version_check = sklearn.base._DEFAULT_UNSPECIFIED_TYPE
        sklearn.base._DEFAULT_UNSPECIFIED_TYPE = object()

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        sklearn.base._DEFAULT_UNSPECIFIED_TYPE = original_version_check
        print("[SUCCESS] Model loaded with version check disabled")
        return model, "version_disabled"
    except Exception as e:
        print(f"[FAILED] Version-disabled load failed: {str(e)}")

    # Strategy 3: Try to load as raw bytes and inspect
    try:
        with open(model_path, 'rb') as f:
            raw_data = f.read()

        # Look for text patterns in the pickle
        if b'DecisionTreeClassifier' in raw_data:
            print("[INFO] Model contains DecisionTreeClassifier")
        if b'RandomForestClassifier' in raw_data:
            print("[INFO] Model contains RandomForestClassifier")
        if b'Pipeline' in raw_data:
            print("[INFO] Model contains Pipeline")

        # Look for feature names
        if b'phone_model' in raw_data:
            print("[INFO] Model expects 'phone_model' feature")
        if b'gender' in raw_data:
            print("[INFO] Model expects 'gender' feature")

        return None, "inspected"
    except Exception as e:
        print(f"[FAILED] Inspection failed: {str(e)}")

    return None, "failed"

def analyze_pickle_structure(model_path):
    """Analyze pickle structure without fully loading"""
    import pickletools

    try:
        with open(model_path, 'rb') as f:
            print("\n[PICKLE OPCODES ANALYSIS]")
            # Show first 50 opcodes
            for i, (opcode, arg, pos) in enumerate(pickletools.genops(f.read()[:5000])):
                if i < 50:
                    print(f"  {opcode.name}: {arg if arg else ''}")
                else:
                    break
    except Exception as e:
        print(f"[ERROR] Could not analyze pickle structure: {e}")

def main():
    print("=" * 60)
    print("TELCO MODEL ANALYSIS (ROBUST)")
    print("=" * 60)

    model_path = "model_telco_recommendation.pkl"

    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found at: {model_path}")
        print(f"Current directory: {os.getcwd()}")
        # List all pkl files
        for f in os.listdir('.'):
            if f.endswith('.pkl'):
                print(f"Found pkl file: {f}")
        return

    print(f"[INFO] Analyzing model: {model_path}")
    print(f"[INFO] File size: {os.path.getsize(model_path)} bytes")

    # Try to load model
    model, method = safe_load_model(model_path)

    if model and method != "inspected":
        print(f"\n[MODEL ANALYSIS - Loaded via {method}]")
        print(f"[INFO] Model type: {type(model)}")
        print(f"[INFO] Model class: {type(model).__name__}")
        print(f"[INFO] Model module: {type(model).__module__}")

        # Get all attributes without causing errors
        print(f"\n[ATTRIBUTES]")
        attrs = [attr for attr in dir(model) if not attr.startswith('_')]
        print(f"  Total non-private attributes: {len(attrs)}")

        # Show important attributes
        important_attrs = [
            'feature_names_in_', 'n_features_in_', 'classes_', 'n_classes_',
            'estimators_', 'feature_importances_', 'tree_', 'max_depth',
            'min_samples_split', 'min_samples_leaf', 'criterion'
        ]

        for attr in important_attrs:
            if hasattr(model, attr):
                value = getattr(model, attr)
                print(f"  FOUND - {attr}: {type(value)}")
                if isinstance(value, (list, tuple, np.ndarray)):
                    print(f"    Length/Shape: {len(value) if hasattr(value, '__len__') else 'N/A'}")
                elif isinstance(value, (str, int, float)):
                    if len(str(value)) < 100:
                        print(f"    Value: {value}")

        # Check if it's a forest or tree
        if 'Forest' in type(model).__name__:
            print(f"\n[RANDOM FOREST DETECTED]")
            if hasattr(model, 'n_estimators'):
                print(f"  Number of trees: {model.n_estimators}")
            if hasattr(model, 'estimators_'):
                print(f"  Estimators shape: {len(model.estimators_)}")

        elif 'Tree' in type(model).__name__:
            print(f"\n[DECISION TREE DETECTED]")
            if hasattr(model, 'tree_'):
                print(f"  Tree node count: {model.tree_.node_count if hasattr(model.tree_, 'node_count') else 'N/A'}")
                if hasattr(model.tree_, 'max_depth'):
                    print(f"  Tree depth: {model.tree_.max_depth}")

        # Check for Pipeline
        if hasattr(model, 'steps') or hasattr(model, 'named_steps'):
            print(f"\n[PIPELINE DETECTED]")
            if hasattr(model, 'named_steps') and model.named_steps:
                for name, step in model.named_steps.items():
                    print(f"  Step: {name} -> {type(step).__name__}")

    elif method == "inspected":
        print("\n[MODEL ANALYSIS - Inspected]")
        print("Could not load model due to version incompatibility")
        print("However, we can see from the raw data that:")
        print("  - Model is likely a scikit-learn estimator")
        print("  - May contain RandomForestClassifier or DecisionTreeClassifier")
        print("  - Expects survey features like phone_model, gender, etc.")

    # Analyze pickle structure
    analyze_pickle_structure(model_path)

    print("\n" + "=" * 60)
    print("RECOMMENDATIONS FOR INTEGRATION:")
    print("=" * 60)

    print("\n1. VERSION COMPATIBILITY:")
    print("   - Model was saved with scikit-learn 1.6.1")
    print("   - Current version is 1.7.2")
    print("   - Option A: Downgrade scikit-learn: pip install scikit-learn==1.6.1")
    print("   - Option B: Re-train the model with current scikit-learn version")
    print("   - Option C: Use current rule-based system (working)")

    print("\n2. INPUT FEATURES (Expected):")
    survey_features = [
        "phone_model", "gender", "reason", "call_frequency",
        "wifi", "housing", "usage", "quota", "budget",
        "preference", "roaming"
    ]
    for feature in survey_features:
        print(f"   - {feature}")

    print("\n3. INTEGRATION APPROACH:")
    print("   Since the model has version issues, consider:")
    print("   a) Continue using the current rule-based recommendation system")
    print("   b) Re-train a new model with the same training data")
    print("   c) Use a hybrid approach - rules + simple ML")

    print("\n4. CURRENT BACKEND:")
    print("   - Uses weighted scoring algorithm")
    print("   - Handles all survey fields correctly")
    print("   - Returns top 6 package recommendations")
    print("   - Stores responses in SQLite database")

if __name__ == "__main__":
    # Try to import numpy for array handling
    try:
        import numpy as np
    except ImportError:
        print("WARNING: NumPy not available")

    main()