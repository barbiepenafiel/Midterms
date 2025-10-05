# Quick Reference Commands

## Start Django Server
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm"
.\venv\Scripts\Activate.ps1
cd backend
python manage.py runserver
```

## Start Celery Worker
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
celery -A backend worker --loglevel=info --pool=solo
```

## Start Celery Beat (Scheduler)
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
celery -A backend beat --loglevel=info
```

## Run Database Migrations
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
python manage.py makemigrations
python manage.py migrate
```

## Create Superuser (Admin)
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
python manage.py createsuperuser
```

## Collect Static Files
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
python manage.py collectstatic --noinput
```

## Important URLs

| Service | URL |
|---------|-----|
| Django Server | http://localhost:8000/ |
| Swagger UI | http://localhost:8000/swagger/ |
| ReDoc | http://localhost:8000/redoc/ |
| Admin Panel | http://localhost:8000/admin/ |
| Frontend | frontend/landing.html |
| API Test Page | frontend/api-test.html |

## API Endpoints Quick Reference

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login
- POST `/api/auth/token/refresh/` - Refresh token
- POST `/api/auth/logout/` - Logout

### 2FA
- GET `/api/auth/2fa/setup/` - Get QR code
- POST `/api/auth/2fa/verify/` - Verify code
- POST `/api/auth/2fa/disable/` - Disable 2FA

### Profile
- GET `/api/auth/profile/` - Get profile
- PUT `/api/auth/profile/` - Update profile
- POST `/api/auth/change-password/` - Change password

## Test User Creation

Using curl:
```powershell
curl -X POST http://localhost:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123!","password2":"TestPass123!"}'
```

Using PowerShell:
```powershell
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "TestPass123!"
    password2 = "TestPass123!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## Clear Browser Data
```javascript
// In browser console
localStorage.clear();
sessionStorage.clear();
```

## Git Commands

### Push Changes
```powershell
git add .
git commit -m "Your message"
git push origin main
```

### Check Status
```powershell
git status
```

### View Logs
```powershell
git log --oneline
```

## Environment Variables (.env)

Create `.env` file in backend directory:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

## Common Issues

### Port Already in Use
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Redis Not Running
```powershell
# Install Redis for Windows or use Docker
docker run -d -p 6379:6379 redis
```

### Virtual Environment Issues
```powershell
# Deactivate
deactivate

# Reactivate
.\venv\Scripts\Activate.ps1
```

## Useful Django Commands

### Shell
```powershell
python manage.py shell
```

### Check Configuration
```powershell
python manage.py check
```

### Show URLs
```powershell
python manage.py show_urls
```

### Database Shell
```powershell
python manage.py dbshell
```

## Documentation Files

| File | Description |
|------|-------------|
| `INTEGRATION_COMPLETE.md` | Integration summary |
| `FRONTEND_INTEGRATION.md` | Detailed integration guide |
| `DJANGO_BACKEND_README.md` | Backend documentation |
| `SETUP_COMPLETE.md` | Quick setup summary |
| `frontend/api-test.html` | API testing tool |

---

**Keep this file handy for quick command reference!** 🚀
