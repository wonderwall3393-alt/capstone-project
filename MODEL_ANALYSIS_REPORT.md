# Telco Recommendation Model Analysis Report

## Overview
- **Model File**: `model_telco_recommendation.pkl` (9.7 MB)
- **Model Type**: scikit-learn RandomForestClassifier (detected in pickle analysis)
- **Version Issue**: Model saved with sklearn 1.6.1, has module path compatibility issues

## Model Structure (Based on Pickle Inspection)

### 1. Model Architecture
- **Type**: RandomForestClassifier
- **Base Estimator**: DecisionTreeClassifier
- **Parameters Detected**:
  - criterion: 'gini'
  - splitter: 'best'
  - max_depth: None (unlimited)
  - min_samples_split: 2
  - min_samples_leaf: 1

### 2. Expected Input Features
The model expects the following 11 survey features:
1. `phone_model` - User's phone model
2. `gender` - User's gender
3. `reason` - Reason for choosing package
4. `call_frequency` - Daily call usage
5. `wifi` - WiFi availability
6. `housing` - Housing type
7. `usage` - Usage patterns (browsing, streaming, etc.)
8. `quota` - Current quota preference
9. `budget` - Budget range
10. `preference` - Package preferences
11. `roaming` - Roaming needs

### 3. Output Format
- **Type**: Categorical classification
- **Output**: Telco package recommendation
- **Probabilities**: Likely available via `predict_proba()`

## Integration Challenges

### 1. Version Compatibility
- Model was pickled with specific sklearn version
- Module path: `sklearn.ensemble._forest.RandomForestClassifier`
- Current issue: `RandomForestClassifier` module not found

### 2. Preprocessing Requirements
- Categorical encoding needed for text features
- Feature ordering must match training data
- Missing value handling may be required

## Current Backend Implementation

The current `backend/recommendation_server.py` uses:
- **Rule-based scoring system** (working)
- **Weighted factors**:
  - Usage: 30%
  - Budget: 25%
  - Need: 20%
  - Preference: 15%
  - Phone Model: 10%

## Integration Options

### Option 1: Fix Model Loading (Recommended)
```python
# Try alternative import paths
from sklearn.ensemble import RandomForestClassifier
import sys

# Add compatibility for older sklearn versions
if not hasattr(sklearn.ensemble, '_forest'):
    sklearn.ensemble._forest = sklearn.ensemble._forest
```

### Option 2: Re-train Model
1. Collect the original training data
2. Re-train with current sklearn version
3. Save with proper module paths

### Option 3: Hybrid Approach
1. Use current rule-based system (working)
2. Add ML model as secondary validation
3. Combine scores for final recommendation

## Implementation Steps for ML Integration

### 1. Data Preprocessing
```python
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Create encoders for categorical variables
encoders = {}
categorical_features = ['phone_model', 'gender', 'reason', 'call_frequency',
                       'wifi', 'housing', 'usage', 'quota', 'budget',
                       'preference', 'roaming']

# Fit encoders on training data (need to collect from original training set)
```

### 2. Prediction Pipeline
```python
def predict_package(survey_data):
    # Transform survey data to model format
    features = []
    for feature in model.feature_names_in_:
        value = survey_data.get(feature, '')
        # Apply encoding
        if feature in encoders:
            value = encoders[feature].transform([value])[0]
        features.append(value)

    # Make prediction
    features_array = np.array([features])
    prediction = model.predict(features_array)[0]
    probabilities = model.predict_proba(features_array)[0]

    return prediction, probabilities
```

### 3. Backend Integration
Modify `backend/recommendation_server.py`:
```python
class MLRecommendationEngine:
    def __init__(self):
        # Load model on initialization
        with open('model_telco_recommendation.pkl', 'rb') as f:
            self.model = pickle.load(f)

    def get_recommendations(self, survey_data):
        # Transform and predict
        packages = self.transform_survey_data(survey_data)
        predictions = self.model.predict(packages)
        probabilities = self.model.predict_proba(packages)

        # Format results
        return self.format_recommendations(predictions, probabilities)
```

## Package Mapping

The model likely outputs package names from this list:
- Sphinx Stable 20GB/50GB/100GB
- Sphinx Hemat 5GB/10GB/20GB/30GB
- Sphinx Unlimited
- Sphinx Call Pro/Flex/Lite
- Sphinx Social 10GB
- Sphinx Stream 50GB/100GB
- Sphinx Work Connect 30GB
- Sphinx Gamer Pro/Max
- Sphinx IoT Home/Fiber
- Sphinx Global Lite/Pass/Roam Max

## Recommendation

Given the current challenges:
1. **Short-term**: Continue using the working rule-based system
2. **Medium-term**: Re-train the model with current sklearn version
3. **Long-term**: Create a hybrid system combining rules and ML

The rule-based system is already well-implemented and provides good results based on survey responses. Consider enhancing it with additional business rules rather than struggling with the ML model compatibility issues.