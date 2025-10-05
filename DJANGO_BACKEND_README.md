# 🚀 Oursfolio Portfolio - Django Backend with Swagger & Celery

Complete Django REST API backend with Authentication, 2FA, Google OAuth, Swagger Documentation, and Celery task queue.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Celery Tasks](#celery-tasks)
- [Project Structure](#project-structure)

---

## ✨ Features

### Authentication & Security
- ✅ User Registration & Login
- ✅ JWT Token Authentication
- ✅ Two-Factor Authentication (2FA) with QR codes
- ✅ Google OAuth 2.0 Integration
- ✅ Password Reset & Change
- ✅ Account Locking (after 3 failed attempts)
- ✅ Login History Tracking
- ✅ Rate Limiting

### API Documentation
- ✅ **Swagger UI** at `/swagger/`
- ✅ **ReDoc** at `/redoc/`
- ✅ OpenAPI 3.0 Schema

### Background Tasks
- ✅ **Celery** for asynchronous tasks
- ✅ **Celery Beat** for periodic tasks
- ✅ Redis as message broker
- ✅ Email notifications
- ✅ Automated cleanup tasks

---

## 🛠️ Tech Stack

### Core
- **Django 4.2+** - Web framework
- **Django REST Framework** - API framework
- **SQLite** - Database (can be changed to PostgreSQL)

### Authentication
- **djangorestframework-simplejwt** - JWT tokens
- **pyotp** - 2FA implementation
- **qrcode** - QR code generation
- **social-auth-app-django** - OAuth integration

### Documentation
- **drf-yasg** - Swagger/OpenAPI documentation

### Background Tasks
- **Celery 5.3+** - Task queue
- **Redis 5.0+** - Message broker
- **django-celery-beat** - Periodic tasks
- **django-celery-results** - Task result backend

### Additional
- **django-cors-headers** - CORS support
- **python-dotenv** - Environment variables
- **Pillow** - Image processing
- **whitenoise** - Static files serving

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Redis Server
- Git

### 1. Clone Repository
```bash
cd "C:\Users\Administrator\Desktop\Final Midterm"
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Install Redis (Windows)
Download and install Redis from: https://github.com/microsoftarchive/redis/releases
Or use WSL/Docker:
```powershell
# Using WSL
wsl sudo service redis-server start

# Using Docker
docker run -d -p 6379:6379 redis:latest
```

---

## ⚙️ Configuration

### 1. Create Environment File
```powershell
Copy-Item .env.example .env
```

### 2. Update `.env` File
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

CELERY_BROKER_URL=redis://localhost:6379/0

GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

### 3. Generate SECRET_KEY
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🏃 Running the Application

### 1. Apply Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Superuser
```powershell
python manage.py createsuperuser
```

### 3. Collect Static Files
```powershell
python manage.py collectstatic --noinput
```

### 4. Run Development Server
```powershell
python manage.py runserver
```

The server will start at: **http://localhost:8000**

### 5. Run Celery Worker (in a new terminal)
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm"
.\venv\Scripts\Activate.ps1
celery -A backend worker --loglevel=info --pool=solo
```

### 6. Run Celery Beat (in another terminal)
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm"
.\venv\Scripts\Activate.ps1
celery -A backend beat --loglevel=info
```

---

## 📚 API Documentation

### Access Swagger UI
Open your browser and go to:
```
http://localhost:8000/swagger/
```

### Access ReDoc
```
http://localhost:8000/redoc/
```

### Authentication Endpoints

#### 1. Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### 2. Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "two_factor_enabled": false
  },
  "requires_2fa": false
}
```

#### 3. Setup 2FA
```http
GET /api/auth/2fa/setup/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KG...",
  "provisioning_uri": "otpauth://totp/..."
}
```

#### 4. Verify 2FA
```http
POST /api/auth/2fa/verify/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "token": "123456"
}
```

#### 5. Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer {access_token}
```

#### 6. Change Password
```http
POST /api/auth/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewPass123!",
  "new_password2": "NewPass123!"
}
```

#### 7. Logout
```http
POST /api/auth/logout/
Authorization: Bearer {access_token}
```

---

## 🔄 Celery Tasks

### Available Tasks

#### 1. Send Welcome Email
Automatically triggered after user registration.
```python
from authentication.tasks import send_welcome_email
send_welcome_email.delay(user_id=1)
```

#### 2. Log Login Attempt
Logs login attempts asynchronously.
```python
from authentication.tasks import log_login_attempt
log_login_attempt.delay(user_id=1, success=True, ip_address='127.0.0.1')
```

#### 3. Cleanup Expired Sessions
Runs daily at 2 AM to unlock expired account locks.
```python
from authentication.tasks import cleanup_expired_sessions
cleanup_expired_sessions.delay()
```

#### 4. Send Security Alert
Sends security alerts to users.
```python
from authentication.tasks import send_security_alert
send_security_alert.delay(user_id=1, alert_type='Unusual Login', details='Login from new location')
```

### Monitor Celery Tasks
```powershell
# Check active tasks
celery -A backend inspect active

# Check scheduled tasks
celery -A backend inspect scheduled

# Check registered tasks
celery -A backend inspect registered
```

---

## 📁 Project Structure

```
Final Midterm/
├── backend/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Main settings
│   ├── urls.py                # Main URL configuration
│   ├── celery.py              # Celery configuration
│   └── wsgi.py
│
├── authentication/             # Authentication app
│   ├── models.py              # User model with 2FA
│   ├── serializers.py         # API serializers
│   ├── views.py               # API views
│   ├── urls.py                # Auth URLs
│   ├── tasks.py               # Celery tasks
│   └── admin.py
│
├── portfolio/                  # Portfolio app
│   ├── models.py              # Project model
│   ├── tasks.py               # Portfolio tasks
│   └── urls.py
│
├── frontend/                   # Frontend files
│   ├── landing.html
│   ├── auth-callback.html
│   └── ...
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing the API

### Using cURL

#### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Pass123!\",\"password2\":\"Pass123!\"}"
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Pass123!\"}"
```

### Using Python Requests
```python
import requests

# Register
response = requests.post('http://localhost:8000/api/auth/register/', json={
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'Pass123!',
    'password2': 'Pass123!'
})
print(response.json())

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'email': 'test@example.com',
    'password': 'Pass123!'
})
tokens = response.json()
print(tokens)

# Get Profile
headers = {'Authorization': f'Bearer {tokens["access"]}'}
response = requests.get('http://localhost:8000/api/auth/profile/', headers=headers)
print(response.json())
```

---

## 🔒 Security Features

### Implemented
- ✅ JWT Token Authentication
- ✅ Password Hashing (PBKDF2)
- ✅ CORS Protection
- ✅ Rate Limiting
- ✅ CSRF Protection
- ✅ XSS Protection (Helmet)
- ✅ Account Locking (3 failed attempts)
- ✅ 2FA with TOTP
- ✅ Login History Tracking

### Best Practices
- Strong password validation
- Token expiration (7 days access, 30 days refresh)
- Secure session management
- IP address logging
- User agent tracking

---

## 📝 Admin Panel

Access Django Admin at: **http://localhost:8000/admin/**

Login with the superuser credentials you created.

From the admin panel, you can:
- Manage users
- View login history
- Check Celery periodic tasks
- Monitor task results

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure production database (PostgreSQL)
- [ ] Set up email backend (SMTP)
- [ ] Configure HTTPS
- [ ] Set allowed hosts
- [ ] Set up Redis in production
- [ ] Configure Celery workers with supervisor
- [ ] Set up static/media file serving (AWS S3, etc.)
- [ ] Enable security headers
- [ ] Set up monitoring (Sentry, etc.)

---

## 📞 Support

For issues or questions:
- Check the Swagger documentation
- Review the code comments
- Check Django logs
- Check Celery logs

---

## 📄 License

MIT License

---

**Built with ❤️ using Django, DRF, Swagger, and Celery**
