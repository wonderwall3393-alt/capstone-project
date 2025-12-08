#!/usr/bin/env python3
"""
Sphinx Net Application Startup Script
Automatically starts the backend server and opens the frontend in browser
"""

import subprocess
import webbrowser
import time
import os
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)

def start_backend():
    """Start the backend server"""
    print("🚀 Starting Sphinx Net Backend Server...")
    backend_path = os.path.join("backend", "recommendation_server.py")

    if not os.path.exists(backend_path):
        print(f"❌ Error: Backend file not found at {backend_path}")
        return None

    try:
        # Start backend server
        process = subprocess.Popen([sys.executable, backend_path])
        print("✅ Backend server starting on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def open_frontend():
    """Open frontend in browser"""
    print("🌐 Opening frontend in browser...")

    frontend_files = ["home-before.html", "index.html", "login.html"]

    for file in frontend_files:
        if os.path.exists(file):
            file_path = os.path.abspath(file)
            file_url = f"file:///{file_path.replace(os.sep, '/')}"

            try:
                webbrowser.open(file_url)
                print(f"✅ Frontend opened: {file_url}")
                return True
            except Exception as e:
                print(f"❌ Error opening browser: {e}")
                return False

    print("❌ No frontend file found")
    return False

def main():
    """Main application startup"""
    print("=" * 60)
    print("🌟 SPHINX NET - Telco Recommendation Platform")
    print("=" * 60)

    # Check Python version
    check_python_version()

    # Check if we're in the right directory
    if not os.path.exists("home-before.html"):
        print("❌ Error: Please run this script from the project root directory")
        print("   (directory containing home-before.html)")
        sys.exit(1)

    # Start backend
    backend_process = start_backend()
    if backend_process is None:
        print("❌ Failed to start backend server")
        sys.exit(1)

    # Wait a moment for server to start
    print("⏳ Waiting for server to initialize...")
    time.sleep(2)

    # Open frontend
    frontend_opened = open_frontend()

    print("\n" + "=" * 60)
    print("🎉 APPLICATION READY!")
    print("=" * 60)
    print("📍 Backend API: http://localhost:8000")
    print("📍 Frontend: Check your browser")
    print("\n📝 Demo Credentials:")
    print("   Email: demo@sphinx.net")
    print("   Password: demo123")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        # Keep the script running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    main()