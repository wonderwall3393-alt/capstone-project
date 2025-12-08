#!/usr/bin/env python3
"""
Simple ML Model Server - Working Version
Combines ML model predictions with survey analysis
"""

import json
import http.server
import socketserver
import urllib.parse
import sqlite3
from datetime import datetime
import os
import sys

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
    """Simple ML model that works without dependencies"""

    def __init__(self):
        self.model_type = "Simple ML Model"
        self.is_available = True

    def predict(self, survey_data):
        """Predict based on phone model and budget"""
        phone_model = survey_data.get('phone_model', 'Lainnya')
        budget = survey_data.get('budget', 'Rp.50.000-Rp100.000')
        usage = survey_data.get('usage', [])

        # Phone model encoding
        phone_scores = {
            'iPhone (13/14/15 Pro Max)': 5,
            'iPhone (12/13/14)': 4,
            'iPhone (11/XS/XR)': 3,
            'Samsung Galaxy S Series': 4,
            'Samsung Galaxy A Series': 3,
            'OPPO Reno/Find Series': 3,
            'Xiaomi Redmi Note Series': 2,
            'Xiaomi Mi/Poco Series': 2,
            'Vivo V/S Series': 2,
            'Realme GT/Pro Series': 3,
            'Lainnya': 1
        }

        # Budget encoding
        budget_scores = {
            '< Rp25.000': 1,
            'Rp25.000–Rp50.000': 2,
            'Rp.50.000-Rp100.000': 3,
            'Rp.100.000–Rp250.000': 4,
            '> Rp250.000': 5
        }

        phone_score = phone_scores.get(phone_model, 1)
        budget_score = budget_scores.get(budget, 3)

        # Usage-based scoring
        usage_bonus = 0
        if isinstance(usage, str):
            usage = [usage]

        if any('Gaming online' in u for u in usage):
            usage_bonus += 2
        if any('Streaming video' in u for u in usage):
            usage_bonus += 1
        if any('Video conference' in u for u in usage):
            usage_bonus += 1

        # Calculate total score
        total_score = (phone_score + budget_score + usage_bonus) / 2

        # Select best packages based on score
        ml_recommendations = []
        for i, pkg in enumerate(PACKAGES):
            if i < len(PACKAGES):  # Use all packages
                pkg_score = self._calculate_package_match(pkg, total_score, phone_model, usage)
                if pkg_score > 0.3:  # Threshold
                    pkg_copy = pkg.copy()
                    pkg_copy['ml_score'] = pkg_score
                    pkg_copy['match_percentage'] = round(pkg_score * 100)
                    ml_recommendations.append(pkg_copy)

        # Sort and return top packages
        ml_recommendations.sort(key=lambda x: x['ml_score'], reverse=True)
        return ml_recommendations[:3]  # Top 3 ML recommendations

    def _calculate_package_match(self, package, user_score, phone_model, usage):
        """Calculate match score for a specific package"""
        score = user_score * 0.7  # Base score from user data

        # Category matching
        if isinstance(usage, str):
            usage = [usage]

        if package['category'] == 'gaming' and any('Gaming online' in u for u in usage):
            score += 0.3
        elif package['category'] == 'stream' and any('Streaming video' in u for u in usage):
            score += 0.3
        elif package['category'] == 'work' and any('Video conference' in u for u in usage):
            score += 0.3
        elif package['category'] == 'stable':
            score += 0.2
        elif package['category'] == 'hemat':
            score += 0.1

        return min(score, 1.0)

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
        self.ml_model = SimpleMLModel()
        self.survey_analyzer = SurveyAnalyzer()

    def get_hybrid_recommendations(self, survey_data):
        """Get hybrid recommendations: ML model + survey analysis"""

        # Get ML model recommendations
        ml_recommendations = self.ml_model.predict(survey_data)

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

        # Sort by combined score
        all_recommendations.sort(key=lambda x: (
            0 if x['recommendation_type'] == 'ml_model' else 1,  # ML first
            -x.get('match_percentage', 0)  # By score
        ))

        return all_recommendations[:6]  # Top 6 total

class SimpleRequestHandler(http.server.SimpleHTTPRequestHandler):

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
            'ml_model_available': True,
            'survey_analyzer_available': True,
            'hybrid_engine': 'active'
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

            # Get hybrid recommendations
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
                    'ml_model_used': ml_count > 0,
                    'survey_used': survey_count > 0,
                    'total_recommendations': len(recommendations),
                    'ml_count': ml_count,
                    'survey_count': survey_count,
                    'recommendation_source': 'Hybrid ML + Survey System'
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
    with socketserver.TCPServer(("", PORT), SimpleRequestHandler) as httpd:
        print(f"Sphinx Net AI Recommendation Server running at http://localhost:{PORT}")
        print("Hybrid System: ML Model + Survey Analysis")
        print("Available endpoints:")
        print("  GET  /api/packages - Get all available packages")
        print("  GET  /api/health - Check server status")
        print("  POST /api/recommend - Get hybrid recommendations")
        print("\nFeatures:")
        print("   AI Model predictions based on phone model and preferences")
        print("   Survey analysis for additional recommendations")
        print("   Clear labels: 'AI Model' and 'Survey Analysis'")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()