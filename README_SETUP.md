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