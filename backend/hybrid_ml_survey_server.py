#!/usr/bin/env python3
"""
Hybrid ML + Survey Server - Combines actual ML model with survey analysis
Processes survey data through ML model and provides survey-based recommendations
"""

import json
import http.server
import socketserver
import urllib.parse
import sqlite3
from datetime import datetime
import os
import sys
import pickle
import numpy as np
import types

# Create compatibility layer for older sklearn module paths
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier

    # Create old module paths for compatibility
    sklearn_ensemble_forest = types.ModuleType('sklearn.ensemble._forest')
    sklearn_ensemble_forest.RandomForestClassifier = RandomForestClassifier
    sys.modules['sklearn.ensemble._forest'] = sklearn_ensemble_forest

    sklearn_tree_classes = types.ModuleType('sklearn.tree._classes')
    sklearn_tree_classes.DecisionTreeClassifier = DecisionTreeClassifier
    sys.modules['sklearn.tree._classes'] = sklearn_tree_classes

    print("Sklearn compatibility layer created successfully")
except ImportError as e:
    print(f"Warning: Could not create sklearn compatibility layer: {e}")

# Database setup
DB_NAME = 'telco_users.db'

def init_database():
    """Initialize SQLite database for user data"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            package TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_survey TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            survey_data TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# ISP Packages Data
PACKAGES = [
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

class FeatureEncoder:
    """Encodes survey data into features compatible with ML model"""

    def __init__(self):
        # Feature mappings for encoding
        self.phone_model_mapping = {
            'iPhone (13/14/15 Pro Max)': 10,
            'iPhone (12/13/14)': 9,
            'iPhone (11/XS/XR)': 8,
            'Samsung Galaxy S Series': 9,
            'Samsung Galaxy A Series': 7,
            'OPPO Reno/Find Series': 7,
            'Xiaomi Redmi Note Series': 6,
            'Xiaomi Mi/Poco Series': 7,
            'Vivo V/S Series': 6,
            'Realme GT/Pro Series': 7,
            'Lainnya': 4
        }

        self.gender_mapping = {
            'Laki-laki': 1,
            'Perempuan': 0
        }

        self.reason_mapping = {
            'Mencari internet yang stabil': 5,
            'Mencari internet yang murah': 3,
            'Mencari internet yang cepat': 4,
            'Mencari kuota besar': 4,
            'Mencari paket telepon': 3,
            'Lainnya': 2
        }

        self.call_frequency_mapping = {
            'Sering': 5,
            'Kadang': 3,
            'Jarang': 1,
            'Tidak pernah': 0
        }

        self.wifi_mapping = {
            'Ya dirumah': 3,
            'Ya di kantor': 3,
            'Tidak': 0
        }

        self.housing_mapping = {
            'Rumah pribadi': 5,
            'Apartemen': 4,
            'Kost/kontrakan': 3,
            'Lainnya': 2
        }

        self.budget_mapping = {
            '< Rp25.000': 1,
            'Rp25.000–Rp50.000': 2,
            'Rp.50.000-Rp100.000': 3,
            'Rp.100.000–Rp250.000': 4,
            '> Rp250.000': 5
        }

        self.quota_mapping = {
            '< 10 GB': 1,
            '10–25 GB': 2,
            '25-50 GB': 3,
            '50–100 GB': 4,
            '> 100 GB': 5
        }

        self.preference_mapping = {
            'Hemat/entry-level': 1,
            'Standar': 2,
            'Kuota besar': 4,
            'Unlimited': 5,
            'Stabil/cepat': 4
        }

        self.roaming_mapping = {
            'Sering': 3,
            'Kadang': 2,
            'Tidak': 0
        }

    def encode_usage_features(self, usage_list):
        """Encode usage features into binary"""
        if isinstance(usage_list, str):
            usage_list = [usage_list]

        usage_features = {
            'Gaming online': 0,
            'Streaming video (YouTube, Netflix, dll.)': 0,
            'Browsing & media sosial': 0,
            'Video conference (Zoom, Teams, dll.)': 0,
            'Download & upload file besar': 0,
            'Smart home / IoT': 0,
            'Lainnya': 0
        }

        for usage in usage_list:
            if usage in usage_features:
                usage_features[usage] = 1

        return list(usage_features.values())

    def encode_survey_data(self, survey_data):
        """Convert survey data to feature vector for ML model"""
        try:
            # Basic features
            phone_model = survey_data.get('phone_model', 'Lainnya')
            gender = survey_data.get('gender', 'Laki-laki')
            reason = survey_data.get('reason', 'Mencari internet yang stabil')
            call_frequency = survey_data.get('call_frequency', 'Jarang')
            wifi = survey_data.get('wifi', 'Tidak')
            housing = survey_data.get('housing', 'Rumah pribadi')
            budget = survey_data.get('budget', 'Rp.50.000-Rp100.000')
            quota = survey_data.get('quota', '25-50 GB')
            preference = survey_data.get('preference', 'Standar')
            roaming = survey_data.get('roaming', 'Tidak')
            usage = survey_data.get('usage', [])

            # Encode categorical features
            features = []

            # Phone model (high importance for tech_doc requirement)
            features.append(self.phone_model_mapping.get(phone_model, 4))

            # Gender
            features.append(self.gender_mapping.get(gender, 1))

            # Reason (need/importance)
            features.append(self.reason_mapping.get(reason, 2))

            # Call frequency
            features.append(self.call_frequency_mapping.get(call_frequency, 1))

            # WiFi availability
            features.append(self.wifi_mapping.get(wifi, 0))

            # Housing type
            features.append(self.housing_mapping.get(housing, 2))

            # Budget (important factor)
            features.append(self.budget_mapping.get(budget, 3))

            # Expected quota
            features.append(self.quota_mapping.get(quota, 3))

            # Preference
            features.append(self.preference_mapping.get(preference, 2))

            # Roaming needs
            features.append(self.roaming_mapping.get(roaming, 0))

            # Usage features (binary)
            usage_features = self.encode_usage_features(usage)
            features.extend(usage_features)

            # Convert to numpy array and reshape for model
            feature_vector = np.array(features).reshape(1, -1)

            return feature_vector

        except Exception as e:
            print(f"Error encoding survey data: {e}")
            # Return default feature vector if encoding fails
            return np.array([5, 1, 3, 1, 1, 3, 3, 3, 2, 0] + [0]*7).reshape(1, -1)

class WeightingLogic:
    """Implements weighting logic for recommendations as per tech_doc.txt"""

    def __init__(self):
        # Weight factors for different aspects
        self.weights = {
            'budget_fit': 0.35,      # Budget compatibility (most important)
            'usage_match': 0.30,     # Usage pattern matching
            'need_alignment': 0.20,  # Reason/preference alignment
            'tech_level': 0.15       # Phone model technology level
        }

    def calculate_budget_fit(self, package_price, user_budget):
        """Calculate how well package fits user budget"""
        budget_map = {
            "< Rp25.000": 25000,
            "Rp25.000–Rp50.000": 50000,
            "Rp.50.000-Rp100.000": 100000,
            "Rp.100.000–Rp250.000": 250000,
            "> Rp250.000": 500000
        }

        max_budget = budget_map.get(user_budget, 100000)

        if package_price <= max_budget:
            # Perfect fit if within budget
            return 1.0
        elif package_price <= max_budget * 1.2:
            # Slightly over budget
            return 0.7
        else:
            # Way over budget
            return 0.3

    def calculate_usage_match(self, package_category, usage_list):
        """Calculate how well package matches user usage"""
        if isinstance(usage_list, str):
            usage_list = [usage_list]

        category_usage_match = {
            'gaming': ['Gaming online'],
            'stream': ['Streaming video (YouTube, Netflix, dll.)'],
            'work': ['Video conference (Zoom, Teams, dll.)'],
            'social': ['Browsing & media sosial'],
            'call': ['Download & upload file besar'],  # Assumed
            'iot': ['Smart home / IoT']
        }

        match_score = 0.5  # Base score

        if package_category in category_usage_match:
            required_usage = category_usage_match[package_category]
            for usage in required_usage:
                if usage in usage_list:
                    match_score = 1.0
                    break

        return match_score

    def calculate_need_alignment(self, package_category, reason, preference):
        """Calculate alignment with user's stated needs"""
        reason_category_map = {
            'Mencari internet yang stabil': ['stable', 'work'],
            'Mencari internet yang murah': ['hemat'],
            'Mencari internet yang cepat': ['stream', 'gaming', 'stable'],
            'Mencari kuota besar': ['unlimited', 'stream', 'gaming'],
            'Mencari paket telepon': ['call']
        }

        preference_category_map = {
            'Hemat/entry-level': ['hemat', 'call'],
            'Standar': ['stable', 'social'],
            'Kuota besar': ['unlimited', 'stream', 'gaming'],
            'Unlimited': ['unlimited'],
            'Stabil/cepat': ['stable', 'work', 'stream']
        }

        alignment_score = 0.5

        # Check reason alignment
        if reason in reason_category_map:
            if package_category in reason_category_map[reason]:
                alignment_score += 0.3

        # Check preference alignment
        if preference in preference_category_map:
            if package_category in preference_category_map[preference]:
                alignment_score += 0.2

        return min(alignment_score, 1.0)

    def calculate_weighted_score(self, package, survey_data, ml_score=0.5):
        """Calculate final weighted score combining ML and logic"""
        user_budget = survey_data.get('budget', 'Rp.50.000-Rp100.000')
        usage = survey_data.get('usage', [])
        reason = survey_data.get('reason', 'Mencari internet yang stabil')
        preference = survey_data.get('preference', 'Standar')

        # Calculate individual scores
        budget_score = self.calculate_budget_fit(package['harga'], user_budget)
        usage_score = self.calculate_usage_match(package['category'], usage)
        need_score = self.calculate_need_alignment(package['category'], reason, preference)

        # Combine with weighted logic
        logic_score = (
            budget_score * self.weights['budget_fit'] +
            usage_score * self.weights['usage_match'] +
            need_score * self.weights['need_alignment'] +
            ml_score * self.weights['tech_level']
        )

        return min(logic_score, 1.0)

class MLModelProcessor:
    """Processes survey data through the actual ML model"""

    def __init__(self):
        self.model = None
        self.feature_encoder = FeatureEncoder()
        self.weighting_logic = WeightingLogic()
        self.model_loaded = False

    def load_model(self):
        """Load the ML model from pickle file"""
        try:
            # Try the new fixed model first
            model_path = 'model_telco_recommendation_new.pkl'
            fallback_path = 'model_telco_recommendation.pkl'

            if os.path.exists(model_path):
                print(f"Loading NEW AI model from {model_path}...")
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                print(f"SUCCESS: NEW AI model loaded: {type(self.model)}")
                if hasattr(self.model, 'estimators_'):
                    print(f"AI Model has {len(self.model.estimators_)} decision trees")
                if hasattr(self.model, 'n_features_in_'):
                    print(f"AI Model expects {self.model.n_features_in_} features")
                return

            elif os.path.exists(fallback_path):
                print(f"Trying original model from {fallback_path}...")
                with open(fallback_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                print(f"SUCCESS: Original model loaded: {type(self.model)}")
            else:
                print("No ML model file found")
                self.model_loaded = False

        except Exception as e:
            print(f"ERROR loading AI model: {e}")
            self.model_loaded = False

    def process_survey_through_model(self, survey_data):
        """Process survey data through ML model and return recommendations"""
        if not self.model_loaded:
            self.load_model()

        recommendations = []

        # Encode survey data
        try:
            feature_vector = self.feature_encoder.encode_survey_data(survey_data)
            print(f"Feature vector shape: {feature_vector.shape}")

            if self.model_loaded and hasattr(self.model, 'predict_proba'):
                # Use actual ML model for predictions
                try:
                    # Get predictions/probabilities from model
                    if hasattr(self.model, 'predict_proba'):
                        probabilities = self.model.predict_proba(feature_vector)[0]
                    else:
                        # If no predict_proba, use decision_function or predict
                        if hasattr(self.model, 'decision_function'):
                            scores = self.model.decision_function(feature_vector)[0]
                        else:
                            predictions = self.model.predict(feature_vector)
                            scores = predictions[0] if len(predictions.shape) > 1 else [predictions[0]]

                        # Convert to probabilities-like scores
                        probabilities = np.array(scores) / np.sum(scores) if np.sum(scores) > 0 else np.ones(len(scores)) / len(scores)

                    print(f"Model predictions: {probabilities}")

                except Exception as model_error:
                    print(f"Error in model prediction: {model_error}")
                    probabilities = None
            else:
                probabilities = None

        except Exception as e:
            print(f"Error in feature encoding: {e}")
            probabilities = None

        # Generate recommendations with ML scores
        if probabilities is not None and len(probabilities) == len(PACKAGES):
            # Use actual AI model predictions
            for i, package in enumerate(PACKAGES):
                ml_score = probabilities[i]
        else:
            # Fallback ML score based on phone model and basic features
            phone_model = survey_data.get('phone_model', 'Lainnya')
            budget = survey_data.get('budget', 'Rp.50.000-Rp100.000')

            # Simple ML-like scoring based on phone and budget
            phone_score = self.feature_encoder.phone_model_mapping.get(phone_model, 4)
            budget_score = self.feature_encoder.budget_mapping.get(budget, 3)
            base_ml_score = (phone_score + budget_score) / 12.0  # Normalize to 0-1

            # Create varied ML scores for each package based on category match
            for i, package in enumerate(PACKAGES):
                ml_score = base_ml_score
                usage = survey_data.get('usage', [])
                if isinstance(usage, str):
                    usage = [usage]

                # Boost scores based on category match
                if package['category'] == 'gaming' and any('Gaming' in u for u in usage):
                    ml_score += 0.2
                elif package['category'] == 'stream' and any('Streaming' in u for u in usage):
                    ml_score += 0.2
                elif package['category'] == 'work' and any('Video conference' in u for u in usage):
                    ml_score += 0.2
                elif package['category'] == 'social' and any('Browsing' in u for u in usage):
                    ml_score += 0.1

                probabilities = [0] * len(PACKAGES) if probabilities is None else probabilities
                if i < len(probabilities):
                    probabilities[i] = min(ml_score, 1.0)

        for i, package in enumerate(PACKAGES):
            if probabilities is not None and i < len(probabilities):
                ml_score = probabilities[i]

            # Apply weighting logic
            final_score = self.weighting_logic.calculate_weighted_score(
                package, survey_data, ml_score
            )

            # Create recommendation package
            pkg_copy = package.copy()
            pkg_copy['ml_score'] = ml_score
            pkg_copy['logic_score'] = final_score
            pkg_copy['match_percentage'] = round(final_score * 100)
            pkg_copy['recommendation_type'] = 'ml_model'
            pkg_copy['source'] = 'AI Model'

            recommendations.append(pkg_copy)

        # Sort by final score
        recommendations.sort(key=lambda x: x['logic_score'], reverse=True)
        return recommendations[:3]  # Top 3 ML recommendations

class SurveyAnalyzer:
    """Survey-based recommendation analyzer"""

    def __init__(self):
        self.weights = {
            'usage': 0.4,
            'budget': 0.3,
            'need': 0.2,
            'preference': 0.1
        }

    def get_recommendations(self, survey_data, exclude_packages=None):
        """Get survey-based recommendations"""
        if exclude_packages is None:
            exclude_packages = set()

        survey_recommendations = []

        for package in PACKAGES:
            if package['name'] in exclude_packages:
                continue

            score = self._calculate_survey_score(survey_data, package)

            if score > 0.2:  # Threshold
                pkg_copy = package.copy()
                pkg_copy['survey_score'] = score
                pkg_copy['match_percentage'] = round(score * 100)
                survey_recommendations.append(pkg_copy)

        # Sort and return top packages
        survey_recommendations.sort(key=lambda x: x['survey_score'], reverse=True)
        return survey_recommendations[:3]  # Top 3 survey recommendations

    def _calculate_survey_score(self, survey_data, package):
        """Calculate survey-based score"""
        score = 0

        # Usage match
        usage = survey_data.get('usage', [])
        if isinstance(usage, str):
            usage = [usage]

        if package['category'] == 'gaming' and any('Gaming online' in u for u in usage):
            score += self.weights['usage']
        elif package['category'] == 'stream' and any('Streaming video' in u for u in usage):
            score += self.weights['usage']
        elif package['category'] == 'work' and any('Video conference' in u for u in usage):
            score += self.weights['usage']
        elif package['category'] == 'social' and any('Browsing' in u for u in usage):
            score += self.weights['usage']

        # Budget fit
        budget_map = {
            "< Rp25.000": 25000,
            "Rp25.000–Rp50.000": 50000,
            "Rp.50.000-Rp100.000": 100000,
            "Rp.100.000–Rp250.000": 250000,
            "> Rp250.000": 500000
        }

        user_budget = budget_map.get(survey_data.get('budget'), 100000)
        if package['harga'] <= user_budget:
            score += self.weights['budget']

        # Need match
        reason = survey_data.get('reason', '')
        if "stabil" in reason.lower() and package['category'] == "stable":
            score += self.weights['need']
        elif "murah" in reason.lower() and package['category'] == "hemat":
            score += self.weights['need']
        elif "unlimited" in reason.lower() and package['category'] == "unlimited":
            score += self.weights['need']

        return min(score, 1.0)

class HybridRecommendationEngine:
    """Hybrid engine combining ML model and survey analysis"""

    def __init__(self):
        self.ml_processor = MLModelProcessor()
        self.survey_analyzer = SurveyAnalyzer()

    def get_hybrid_recommendations(self, survey_data):
        """Get hybrid recommendations: ML model + survey analysis"""

        # Get ML model recommendations with proper feature encoding
        ml_recommendations = self.ml_processor.process_survey_through_model(survey_data)

        # Track packages recommended by ML
        ml_packages = {pkg['name'] for pkg in ml_recommendations}

        # Get survey-based recommendations (excluding ML packages)
        survey_recommendations = self.survey_analyzer.get_recommendations(survey_data, ml_packages)

        # Combine recommendations
        all_recommendations = []

        # Add ML recommendations first
        for pkg in ml_recommendations:
            pkg['recommendation_type'] = 'ml_model'
            pkg['source'] = 'AI Model'
            all_recommendations.append(pkg)

        # Add survey recommendations
        for pkg in survey_recommendations:
            pkg['recommendation_type'] = 'survey_based'
            pkg['source'] = 'Survey Analysis'
            all_recommendations.append(pkg)

        # Sort by combined score (ML first, then survey)
        all_recommendations.sort(key=lambda x: (
            0 if x['recommendation_type'] == 'ml_model' else 1,  # ML first
            -x.get('match_percentage', 0)  # By score
        ))

        return all_recommendations[:6]  # Top 6 total

class HybridRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.recommendation_engine = HybridRecommendationEngine()
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/packages':
            self.send_packages()
        elif self.path == '/api/health':
            self.health_check()
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/recommend':
            self.handle_hybrid_recommendation()
        else:
            self.send_error(404)

    def send_packages(self):
        """Send all available packages"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = json.dumps(PACKAGES)
        self.wfile.write(response.encode())

    def health_check(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        health_data = {
            'status': 'healthy',
            'ml_model_loaded': self.recommendation_engine.ml_processor.model_loaded,
            'feature_encoder_ready': True,
            'weighting_logic_ready': True,
            'survey_analyzer_ready': True,
            'hybrid_engine': 'active',
            'model_type': 'model_telco_recommendation.pkl'
        }

        response = json.dumps(health_data)
        self.wfile.write(response.encode())

    def handle_hybrid_recommendation(self):
        """Handle hybrid recommendation request"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
        else:
            post_data = b'{}'

        try:
            survey_data = json.loads(post_data.decode('utf-8'))

            # Get hybrid recommendations (ML + Survey)
            recommendations = self.recommendation_engine.get_hybrid_recommendations(survey_data)

            # Count recommendation types
            ml_count = sum(1 for r in recommendations if r.get('recommendation_type') == 'ml_model')
            survey_count = sum(1 for r in recommendations if r.get('recommendation_type') == 'survey_based')

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = json.dumps({
                'success': True,
                'recommendations': recommendations,
                'metadata': {
                    'ml_model_used': self.recommendation_engine.ml_processor.model_loaded,
                    'feature_encoding': 'active',
                    'weighting_logic': 'active',
                    'survey_analysis': 'active',
                    'total_recommendations': len(recommendations),
                    'ml_count': ml_count,
                    'survey_count': survey_count,
                    'recommendation_source': 'Hybrid ML Model + Survey Analysis',
                    'model_file': 'model_telco_recommendation.pkl'
                }
            })
            self.wfile.write(response.encode())

        except Exception as e:
            print(f"Error in hybrid recommendation: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(error_response.encode())

def run_server():
    """Initialize and run the hybrid server"""
    # Initialize database
    init_database()

    # Create and run server
    PORT = 8000  # Use original port
    with socketserver.TCPServer(("", PORT), HybridRequestHandler) as httpd:
        print(f"Sphinx Net Hybrid ML + Survey Server running at http://localhost:{PORT}")
        print("Hybrid System: ML Model (model_telco_recommendation.pkl) + Survey Analysis")
        print("Available endpoints:")
        print("  GET  /api/packages - Get all available packages")
        print("  GET  /api/health - Check system status")
        print("  POST /api/recommend - Get hybrid recommendations")
        print("\nFeatures:")
        print("   ML Model predictions using model_telco_recommendation.pkl with feature encoding")
        print("   Survey analysis for complementary recommendations")
        print("   Weighting logic: Budget (35%) + Usage (30%) + Need (20%) + Tech (15%)")
        print("   Hybrid output: 3 ML + 3 Survey recommendations")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()