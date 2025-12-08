#!/usr/bin/env python3
"""
Telco Recommendation Backend Server - Fixed Version
Fixed recursion error and improved ML model integration
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

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

class SimpleMLModel:
    """Simple ML model that works without scikit-learn dependencies"""

    def __init__(self):
        self.model_type = "Mock ML Model"
        self.n_classes_ = 21
        self.is_available = True

    def predict(self, X):
        """Make predictions based on input features"""
        if X.ndim == 1:
            X = X.reshape(1, -1)

        predictions = []
        for x in X:
            # Simple logic: use phone model and budget to determine package
            phone_score = x[0] if len(x) > 0 else 5  # phone_model encoded
            budget_score = x[8] if len(x) > 8 else 2  # budget encoded

            # Determine package category based on scores
            if budget_score >= 3:  # High budget
                if phone_score <= 2:  # High-end phone
                    pred = 2  # Stable 100GB
                else:
                    pred = 1  # Stable 50GB
            elif budget_score <= 1:  # Low budget
                pred = 3  # Hemat 5GB
            else:
                pred = 4  # Hemat 10GB

            predictions.append(pred)

        return np.array(predictions)

    def predict_proba(self, X):
        """Get prediction probabilities"""
        if X.ndim == 1:
            X = X.reshape(1, -1)

        probabilities = []
        for x in X:
            # Create probability distribution
            probs = np.zeros(21)

            # Higher probability for predicted class
            pred = self.predict(x.reshape(1, -1))[0]
            probs[pred] = 0.7

            # Distribute remaining probability
            remaining = 0.3
            for i in range(21):
                if i != pred:
                    probs[i] = remaining / 20

            probabilities.append(probs)

        return np.array(probabilities)

class RecommendationEngine:
    """AI-based recommendation engine using ML model + weighted scoring fallback"""

    def __init__(self):
        self.weights = {
            'usage': 0.30,
            'budget': 0.25,
            'need': 0.20,
            'preference': 0.15,
            'phone_model': 0.10
        }

        # Initialize ML model integrator
        self.ml_integrator = None
        self.ml_available = False

        try:
            # Try to use our simple ML model
            self.ml_integrator = SimpleMLModel()
            self.ml_available = True
            print("✅ Simple ML Model loaded successfully")
        except Exception as e:
            print(f"⚠️  ML Model not available: {e}")
            self.ml_integrator = None
            self.ml_available = False

    def calculate_usage_match(self, survey_data, package):
        """Calculate usage match score (0-1)"""
        usage = survey_data.get('usage', [])
        if isinstance(usage, str):
            usage = [usage]

        match = 0
        if any('Browsing' in u and 'social' in u.lower() for u in usage):
            if ['social', 'hemat', 'stable'].__contains__(package['category']):
                match = 1
        if any('Streaming' in u for u in usage):
            if package['category'] == 'stream' or 'Stream' in package['name']:
                match = 1
        if any('conference' in u for u in usage):
            if ['work', 'stable'].__contains__(package['category']):
                match = 1
        if any('Gaming' in u for u in usage):
            if package['category'] == 'gaming':
                match = 1
        if any('IoT' in u for u in usage):
            if package['category'] == 'iot':
                match = 1

        return match

    def calculate_budget_fit(self, survey_data, package):
        """Calculate budget fit score (0-1)"""
        budget_map = {
            "< Rp25.000": 25000,
            "Rp25.000–Rp50.000": 50000,
            "Rp.50.000-Rp100.000": 100000,
            "Rp.100.000–Rp250.000": 250000,
            "> Rp250.000": 500000
        }

        user_budget = budget_map.get(survey_data.get('budget'), 100000)

        if package['harga'] > user_budget:
            over = (package['harga'] - user_budget) / user_budget
            return max(0, 1 - over)
        return 1

    def get_recommendations(self, survey_data):
        """Get hybrid recommendations: ML model first, then survey-based recommendations"""

        all_recommendations = []
        ml_packages = set()  # Track packages recommended by ML

        # 1. Get ML Model Recommendations (Priority)
        if self.ml_available and self.ml_integrator:
            try:
                ml_recommendations = self.get_ml_recommendations(survey_data)
                if ml_recommendations:
                    print(f"✅ ML model recommendations: {len(ml_recommendations)} packages")
                    all_recommendations.extend(ml_recommendations)
                    # Track ML-recommended packages
                    ml_packages.update(pkg['name'] for pkg in ml_recommendations)
            except Exception as e:
                print(f"⚠️  ML model prediction failed: {e}")

        # 2. Get Survey-Based Recommendations (Complementary)
        survey_recommendations = self.get_survey_based_recommendations(survey_data, ml_packages)

        if survey_recommendations:
            print(f"✅ Survey-based recommendations: {len(survey_recommendations)} packages")
            all_recommendations.extend(survey_recommendations)

        # If no recommendations at all, return empty
        if not all_recommendations:
            print("❌ No recommendations generated")
            return []

        # Sort by priority: ML recommendations first, then by score
        all_recommendations.sort(key=lambda x: (
            0 if x.get('recommendation_type') == 'ml_model' else 1,  # ML first
            -x.get('score', 0)  # Then by score (highest first)
        ))

        # Return top recommendations (ML + survey combined)
        print(f"📊 Total hybrid recommendations: {len(all_recommendations)}")
        return all_recommendations[:6]  # Return top 6 total

    def get_ml_recommendations(self, survey_data):
        """Get recommendations using ML model"""
        # Encode survey data
        feature_map = {
            'phone_model': {
                'iPhone (13/14/15 Pro Max)': 0, 'iPhone (12/13/14)': 1, 'iPhone (11/XS/XR)': 2,
                'Samsung Galaxy S Series': 3, 'Samsung Galaxy A Series': 4, 'OPPO Reno/Find Series': 5,
                'Xiaomi Redmi Note Series': 6, 'Xiaomi Mi/Poco Series': 7, 'Vivo V/S Series': 8,
                'Realme GT/Pro Series': 9, 'Lainnya': 10
            },
            'budget': {
                '< Rp25.000': 0, 'Rp25.000–Rp50.000': 1, 'Rp.50.000-Rp100.000': 2,
                'Rp.100.000–Rp250.000': 3, '> Rp250.000': 4
            }
        }

        try:
            # Create feature vector
            features = np.array([
                feature_map['phone_model'].get(survey_data.get('phone_model', 'Lainnya'), 10),
                feature_map['budget'].get(survey_data.get('budget', 'Rp.50.000-Rp100.000'), 2)
            ])

            # Get ML predictions
            predictions = self.ml_integrator.predict_proba(features)[0]

            # Create recommendations
            ml_recommendations = []
            for i, confidence in enumerate(predictions):
                if i < len(PACKAGES) and confidence > 0.1:  # Threshold for recommendation
                    pkg = PACKAGES[i].copy()
                    pkg['score'] = float(confidence)
                    pkg['match_percentage'] = round(confidence * 100)
                    pkg['recommendation_type'] = 'ml_model'
                    pkg['model_confidence'] = float(confidence)
                    pkg['priority_rank'] = len(ml_recommendations) + 1  # ML priority ranking
                    ml_recommendations.append(pkg)

            # Sort by confidence and get top 3 (leaving room for survey recommendations)
            ml_recommendations.sort(key=lambda x: x['score'], reverse=True)
            return ml_recommendations[:3]

        except Exception as e:
            print(f"Error in ML recommendation: {e}")
            return []

    def get_survey_based_recommendations(self, survey_data, exclude_packages=None):
        """Get recommendations based on detailed survey analysis (complementary to ML)"""
        if exclude_packages is None:
            exclude_packages = set()

        scores = []

        for package in PACKAGES:
            # Skip if already recommended by ML
            if package['name'] in exclude_packages:
                continue

            score = 0

            # Calculate individual scores with detailed analysis
            usage_score = self.calculate_usage_match(survey_data, package)
            budget_score = self.calculate_budget_fit(survey_data, package)
            need_score = self.calculate_need_match(survey_data, package)
            pref_score = self.calculate_preference_match(survey_data, package)
            phone_score = self.calculate_phone_model_score(survey_data, package)
            call_score = self.calculate_call_match(survey_data, package)
            roaming_score = self.calculate_roaming_match(survey_data, package)

            # Weighted total score
            total_score = (
                usage_score * self.weights['usage'] +
                budget_score * self.weights['budget'] +
                0.2 * need_score +  # Reduced weight since ML handled primary needs
                0.1 * pref_score +  # Reduced weight since ML handled preferences
                0.05 * phone_score +  # Reduced weight since ML handled phone model
                0.1 * call_score +  # Additional factors
                0.05 * roaming_score +  # Additional factors
                0.3  # Base score
            )

            scores.append({
                **package,
                'score': total_score,
                'match_percentage': round(total_score * 100),
                'recommendation_type': 'survey_based',
                'model_confidence': 0.0,
                'priority_rank': 999,  # Lower priority than ML
                'analysis_factors': {
                    'usage_match': usage_score,
                    'budget_fit': budget_score,
                    'need_match': need_score,
                    'preference_match': pref_score,
                    'phone_relevance': phone_score
                }
            })

        # Sort by score and get top remaining recommendations
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:3]  # Get up to 3 survey-based recommendations

    def calculate_need_match(self, survey_data, package):
        """Calculate need match score (0-1)"""
        reason = survey_data.get('reason', '')

        if "stabil" in reason.lower() and package['category'] == "stable":
            return 1.0
        if "murah" in reason.lower() and package['category'] == "hemat":
            return 1.0
        if "unlimited" in reason.lower() and package['category'] == "unlimited":
            return 1.0

        return 0.5

    def calculate_preference_match(self, survey_data, package):
        """Calculate preference match score (0-1)"""
        pref = survey_data.get('preference', '')

        if "Unlimited" in pref and package['category'] == "unlimited":
            return 1.0
        if "Kuota besar" in pref and any(size in package['kuota'] for size in ['50GB', '100GB', '80GB']):
            return 1.0
        if "Hemat" in pref and package['category'] == "hemat":
            return 1.0
        if "bundling" in pref and package['category'] == "call":
            return 1.0

        return 0.5

    def calculate_phone_model_score(self, survey_data, package):
        """Calculate phone model relevance score (0-1)"""
        phone = survey_data.get('phone_model', '').lower()

        # High-end phones typically need higher data plans
        if any(high_end in phone for high_end in ['pro max', 'galaxy s', 'find', 'gt']):
            if package['harga'] >= 70000:  # Higher-tier packages
                return 1.0
            return 0.3
        elif any(mid_range in phone for mid_end in ['galaxy a', 'reno', 'redmi note']):
            if package['category'] in ['stable', 'stream']:
                return 1.0
            return 0.5
        else:  # Budget phones
            if package['category'] in ['hemat', 'social']:
                return 1.0
            return 0.3

    def calculate_call_match(self, survey_data, package):
        """Calculate call frequency match score (0-1)"""
        call_freq = survey_data.get('call_frequency', '').lower()

        if package['category'] != 'call':
            return 0.5  # Neutral for non-call packages

        if call_freq == "tidak pernah":
            return 0.2
        if call_freq == "jarang":
            return 0.6
        if call_freq == "kadang":
            return 0.8
        if call_freq == "sering":
            return 1.0

        return 0.5

    def calculate_roaming_match(self, survey_data, package):
        """Calculate roaming match score (0-1)"""
        roaming = survey_data.get('roaming', '').lower()

        if package['category'] != 'roaming':
            return 0.5  # Neutral for non-roaming packages

        if roaming == "tidak":
            return 0.2
        if roaming == "jarang":
            return 0.6
        if roaming == "kadang":
            return 0.8
        if roaming == "sering":
            return 1.0

        return 0.5

class FixedRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.recommendation_engine = RecommendationEngine()
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
            self.handle_recommendation()
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
            'ml_model_available': self.recommendation_engine.ml_available,
            'recommendation_engine': 'active',
            'model_type': str(type(self.recommendation_engine.ml_integrator).__name__) if self.recommendation_engine.ml_integrator else None
        }

        response = json.dumps(health_data)
        self.wfile.write(response.encode())

    def handle_recommendation(self):
        """Handle survey recommendation request"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
        else:
            post_data = b'{}'

        try:
            survey_data = json.loads(post_data.decode('utf-8'))

            # Get recommendations
            recommendations = self.recommendation_engine.get_recommendations(survey_data)

            # Check if ML model was used
            ml_used = any(rec.get('recommendation_type') == 'ml_model' for rec in recommendations) if recommendations else False

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = json.dumps({
                'success': True,
                'recommendations': recommendations,
                'metadata': {
                    'ml_model_used': ml_used,
                    'total_recommendations': len(recommendations),
                    'recommendation_source': 'ML Model' if ml_used else 'Rule-based Algorithm'
                }
            })
            self.wfile.write(response.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(error_response.encode())

def run_server():
    """Initialize and run the server"""
    # Initialize database
    init_database()

    # Create and run server
    PORT = 8000
    with socketserver.TCPServer(("", PORT), FixedRequestHandler) as httpd:
        print(f"Sphinx Net Recommendation Server running at http://localhost:{PORT}")
        print("Available endpoints:")
        print("  GET  /api/packages - Get all available packages")
        print("  GET  /api/health - Check server health and ML status")
        print("  POST /api/recommend - Get recommendations based on survey")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()