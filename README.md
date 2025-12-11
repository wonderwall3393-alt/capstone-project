# capstoneProject-Telco
capstone project - Telco

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

# Sphinx Net - Telco Recommendation Platform

## Project Overview

Sphinx Net is a comprehensive telco recommendation platform that provides personalized ISP recommendations based on user surveys, using AI-powered matching algorithms. The system is built using native HTML, CSS, JavaScript, and Python without any frameworks, as specified in the technical requirements.

## Features

### ✅ Implemented Features

1. **Dynamic Landing Page**
   - Guest mode (default view)
   - Logged-in mode (user avatar, dropdown menu)
   - Real-time UI state management

2. **Interactive Survey System**
   - 11 comprehensive questions including phone model
   - Step-by-step navigation
   - Real-time validation
   - Progress tracking

3. **AI-Powered Recommendations**
   - Weighted scoring algorithm
   - Phone model relevance scoring
   - Budget-based filtering
   - Usage pattern matching

4. **User Authentication**
   - Registration system
   - Login/Logout functionality
   - Session management (localStorage)
   - Profile management

5. **Data Visualization**
   - Native CSS pie chart for data usage
   - No external charting libraries
   - Responsive design

6. **Backend API**
   - RESTful endpoints
   - SQLite database
   - Survey data processing
   - User management

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.x (no frameworks)
- **Database**: SQLite
- **Visualization**: Native CSS (conic-gradient)
- **Icons**: Font Awesome
- **Animation**: CSS3, AOS library

## Project Structure

```
capstoneProject-Telco/
├── backend/
│   └── recommendation_server.py    # Python backend server
├── assets/
│   ├── images/
│   └── fonts/
├── style/
│   ├── style.css                   # Main styles
│   ├── login-style.css             # Login page styles
│   ├── signin-style.css            # Sign up page styles
│   └── responsive.css              # Responsive styles
├── script/
│   ├── script.js                   # Main JavaScript
│   └── animation.js                # Animation scripts
├── home-before.html                # Main landing page
├── login.html                      # Login page
├── signin.html                     # Sign up page
└── README_SETUP.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 1. Start the Backend Server

```bash
# Navigate to project directory
cd D:\nhd\ASAH\capstoneProject-Telco

# Start the Python backend server
python backend/recommendation_server.py
```

The server will start on `http://localhost:8000` with the following endpoints:
- `GET /api/packages` - Get all available packages
- `POST /api/recommend` - Get recommendations based on survey
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration

### 2. Open the Frontend

Open `home-before.html` in your web browser:

```bash
# Option 1: Double-click the file
# Option 2: Use a local server (recommended for development)
python -m http.server 3000
# Then visit http://localhost:3000
```

### 3. Test the Application

#### Demo Mode (without backend)

Use these credentials for quick testing:
- **Email**: demo@sphinx.net
- **Password**: demo123

#### Full Mode (with backend)

1. **Register a new user**:
   - Visit `signin.html`
   - Fill in the registration form
   - Create an account

2. **Login**:
   - Visit `login.html`
   - Use your credentials
   - Access the main application

3. **Take the Survey**:
   - Click "Survey Pengguna" on the main page
   - Answer all questions including your phone model
   - Get personalized recommendations

4. **View Profile**:
   - Click on your avatar in the header
   - View your profile with data usage visualization

## API Documentation

### Survey Question Format

```javascript
{
    "phone_model": "iPhone (13/14/15 Pro Max)",
    "gender": "Laki-laki",
    "reason": "Mencari internet yang stabil",
    "call_frequency": "Sering",
    "wifi": "Ya dirumah",
    "housing": "Rumah pribadi",
    "usage": ["Browsing & media sosial", "Streaming video"],
    "quota": "25-50 GB",
    "budget": "Rp50.000–Rp100.000",
    "preference": "Kuota besar",
    "roaming": "Tidak"
}
```

### Response Format

```javascript
{
    "success": true,
    "recommendations": [
        {
            "name": "Sphinx Stable 50GB",
            "kuota": "50GB",
            "harga": 75000,
            "category": "stable",
            "score": 0.85,
            "match_percentage": 85
        }
    ]
}
```

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password`: Encrypted password
- `phone`: Phone number
- `package`: Current package
- `created_at`: Registration timestamp
- `last_survey`: Last survey data (JSON)

### Survey Responses Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `survey_data`: Survey responses (JSON)
- `recommendations`: Generated recommendations (JSON)
- `created_at`: Response timestamp

## Deployment Notes

### For Production

1. **Security**: Implement proper password hashing
2. **CORS**: Configure CORS headers for production domains
3. **HTTPS**: Use SSL certificates
4. **Database**: Consider PostgreSQL/MySQL for scalability
5. **Session Management**: Use secure cookies instead of localStorage

### Environment Variables

```python
# In recommendation_server.py
DB_NAME = 'telco_users.db'
PORT = 8000
HOST = '0.0.0.0'  # For production
```

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Troubleshooting

### Common Issues

1. **Backend Not Responding**
   - Ensure Python server is running
   - Check port 8000 is not blocked
   - Verify firewall settings

2. **CORS Errors**
   - Server should be running before opening frontend
   - Use local development server for frontend

3. **Database Issues**
   - Delete `telco_users.db` to reset
   - Ensure write permissions in project directory

4. **Survey Not Submitting**
   - Check all questions are answered
   - Verify network connection to backend

### Development Tips

1. Use browser developer tools to monitor API calls
2. Check console for JavaScript errors
3. Use Chrome DevTools Network tab to debug requests
4. Clear localStorage to reset login state

## Future Enhancements

- Real-time data usage tracking
- Package comparison tools
- Customer support integration
- Mobile app development
- Advanced AI/ML model integration
- Payment gateway integration
- Multi-language support

## License

© 2025 Sphinx Net. All Rights Reserved.

---

For technical support or questions, please refer to the code comments or contact the development team.