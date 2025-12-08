#!/usr/bin/env python3
"""
Telco Recommendation Backend Server
Using native Python HTTP server without frameworks
Integrates with ML model for enhanced recommendations
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

try:
    from ml_integration import MLModelIntegrator
    ML_AVAILABLE = True
except ImportError:
    print("⚠️  ML integration module not available, using rule-based system")
    ML_AVAILABLE = False

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
        if ML_AVAILABLE:
            try:
                model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model_telco_recommendation.pkl')
                self.ml_integrator = MLModelIntegrator(model_path)
                if self.ml_integrator.is_available():
                    print("✅ ML model integrated successfully")
                else:
                    print("⚠️  ML model not available, using rule-based fallback")
            except Exception as e:
                print(f"⚠️  Error initializing ML model: {e}")
                self.ml_integrator = None

    def calculate_usage_match(self, survey_data, package):
        """Calculate usage match score (0-1)"""
        usage = survey_data.get('usage', [])
        if isinstance(usage, str):
            usage = [usage]

        match = 0
        if any('Browsing' in u and 'social' in u.lower() for u in usage):
            if package['category'] in ['social', 'hemat', 'stable']:
                match = 1
        if any('Streaming' in u for u in usage):
            if package['category'] == 'stream' or 'Stream' in package['name']:
                match = 1
        if any('conference' in u for u in usage):
            if package['category'] in ['work', 'stable']:
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

    def calculate_need_match(self, survey_data, package):
        """Calculate need match score (0-1)"""
        reason = survey_data.get('reason', '')

        if "stabil" in reason.lower() and package['category'] == "stable":
            return 1
        if "murah" in reason.lower() and package['category'] == "hemat":
            return 1
        if "unlimited" in reason.lower() and package['category'] == "unlimited":
            return 1

        return 0

    def calculate_preference_match(self, survey_data, package):
        """Calculate preference match score (0-1)"""
        pref = survey_data.get('preference', '')

        if "Unlimited" in pref and package['category'] == "unlimited":
            return 1
        if "Kuota besar" in pref and any(size in package['kuota'] for size in ['50GB', '100GB', '80GB']):
            return 1
        if "Hemat" in pref and package['category'] == "hemat":
            return 1
        if "bundling" in pref and package['category'] == "call":
            return 1

        return 0.5

    def calculate_phone_model_score(self, survey_data, package):
        """Calculate phone model relevance score (0-1)"""
        phone = survey_data.get('phone_model', '').lower()

        # High-end phones typically need higher data plans
        if any(high_end in phone for high_end in ['pro max', 'galaxy s', 'find', 'gt']):
            if package['harga'] >= 70000:  # Higher-tier packages
                return 1
            return 0.3
        elif any(mid_range in phone for mid_end in ['galaxy a', 'reno', 'redmi note']):
            if package['category'] in ['stable', 'stream']:
                return 1
            return 0.5
        else:  # Budget phones
            if package['category'] in ['hemat', 'social']:
                return 1
            return 0.3

    def get_recommendations(self, survey_data):
        """Get top 6 recommendations based on survey data using ML model + fallback"""

        # Try ML model first if available
        if self.ml_integrator and self.ml_integrator.is_available():
            try:
                ml_recommendations = self.ml_integrator.get_top_recommendations(survey_data, top_k=6)
                if ml_recommendations:
                    print(f"✅ Using ML model recommendations: {len(ml_recommendations)} packages")
                    # Add ML-specific metadata
                    for rec in ml_recommendations:
                        rec['recommendation_type'] = 'ml_model'
                        rec['model_confidence'] = rec.get('ml_confidence', 0.0)
                    return ml_recommendations
            except Exception as e:
                print(f"⚠️  ML model prediction failed: {e}")
                print("🔄 Falling back to rule-based system")

        # Fallback to rule-based weighted scoring
        print("🔄 Using rule-based recommendation system")
        scores = []

        for package in PACKAGES:
            score = 0

            # Calculate individual scores
            usage_score = self.calculate_usage_match(survey_data, package)
            budget_score = self.calculate_budget_fit(survey_data, package)
            need_score = self.calculate_need_match(survey_data, package)
            pref_score = self.calculate_preference_match(survey_data, package)
            phone_score = self.calculate_phone_model_score(survey_data, package)

            # Weighted total score
            total_score = (
                usage_score * self.weights['usage'] +
                budget_score * self.weights['budget'] +
                need_score * self.weights['need'] +
                pref_score * self.weights['preference'] +
                phone_score * self.weights['phone_model']
            )

            scores.append({
                **package,
                'score': total_score,
                'match_percentage': round(total_score * 100),
                'recommendation_type': 'rule_based',
                'model_confidence': 0.0
            })

        # Sort by score and get top 6
        recommendations = sorted(scores, key=lambda x: x['score'], reverse=True)
        return [pkg for pkg in recommendations if pkg['score'] > 0][:6]

class TelcoRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.recommendation_engine = RecommendationEngine()
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        self.send_cors_headers()
        if self.path == '/api/packages':
            self.send_packages()
        elif self.path.startswith('/api/user/'):
            self.get_user_data()
        elif self.path == '/api/health':
            self.health_check()
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        self.send_cors_headers()
        if self.path == '/api/recommend':
            self.handle_recommendation()
        elif self.path == '/api/auth/login':
            self.handle_login()
        elif self.path == '/api/auth/register':
            self.handle_register()
        else:
            self.send_error(404)

    def send_cors_headers(self):
        """Send CORS headers for all responses"""
        self.send_cors_headers()
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def health_check(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_cors_headers()
        self.end_headers()

        health_data = {
            'status': 'healthy',
            'ml_model_available': self.recommendation_engine.ml_integrator.is_available() if self.recommendation_engine.ml_integrator else False,
            'recommendation_engine': 'active',
            'database': 'connected'
        }

        response = json.dumps(health_data)
        self.wfile.write(response.encode())

    def send_packages(self):
        """Send all available packages"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_cors_headers()
        self.end_headers()

        response = json.dumps(PACKAGES)
        self.wfile.write(response.encode())

    def handle_recommendation(self):
        """Handle survey recommendation request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            survey_data = json.loads(post_data.decode('utf-8'))

            # Get recommendations
            recommendations = self.recommendation_engine.get_recommendations(survey_data)

            # Check if ML model was used
            ml_used = any(rec.get('recommendation_type') == 'ml_model' for rec in recommendations) if recommendations else False

            # Store survey response in database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO survey_responses (survey_data, recommendations)
                VALUES (?, ?)
            ''', (json.dumps(survey_data), json.dumps(recommendations)))
            conn.commit()
            conn.close()

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
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
            self.send_cors_headers()
            self.end_headers()
            error_response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(error_response.encode())

    def handle_login(self):
        """Handle user login"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            login_data = json.loads(post_data.decode('utf-8'))
            email = login_data.get('email')
            password = login_data.get('password')

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_data = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'phone': user[4],
                    'package': user[5]
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                response = json.dumps({'success': True, 'user': user_data})
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'success': False, 'error': 'Invalid credentials'})

            self.wfile.write(response.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            error_response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(error_response.encode())

    def handle_register(self):
        """Handle user registration"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            register_data = json.loads(post_data.decode('utf-8'))
            name = register_data.get('name')
            email = register_data.get('email')
            password = register_data.get('password')

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                self.send_response(409)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'success': False, 'error': 'User already exists'})
                self.wfile.write(response.encode())
                conn.close()
                return

            # Create new user
            cursor.execute('''
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            ''', (name, email, password))

            user_id = cursor.lastrowid
            conn.commit()
            conn.close()

            user_data = {
                'id': user_id,
                'name': name,
                'email': email,
                'package': None
            }

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            response = json.dumps({'success': True, 'user': user_data})
            self.wfile.write(response.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            error_response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(error_response.encode())

def run_server():
    """Initialize and run the server"""
    # Initialize database
    init_database()

    # Create and run server
    PORT = 8000
    with socketserver.TCPServer(("", PORT), TelcoRequestHandler) as httpd:
        print(f"Sphinx Net Recommendation Server running at http://localhost:{PORT}")
        print("Available endpoints:")
        print("  GET  /api/packages - Get all available packages")
        print("  POST /api/recommend - Get recommendations based on survey")
        print("  POST /api/auth/login - User login")
        print("  POST /api/auth/register - User registration")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()