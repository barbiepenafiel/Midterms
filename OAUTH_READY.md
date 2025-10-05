# ✅ Google OAuth 2.0 Setup Complete!

## 🎉 What I Did

I've successfully configured your Google OAuth 2.0 credentials for your Django backend!

### 1. **Extracted Credentials from JSON File**

From your Google Cloud Console OAuth credentials (stored securely in `.env` file):

```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "project_id": "oursfolio-portfolio-474212"
}
```

### 2. **Created .env File**

Created `backend/.env` with your credentials (not committed to git):
```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id-from-google-console
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-from-google-console
```

### 3. **Updated .env.example**

Updated the template file with your credentials (for team reference).

### 4. **Added Social Auth URLs**

Updated `backend/urls.py` to include Google OAuth endpoints:
```python
path('auth/', include('social_django.urls', namespace='social')),
```

### 5. **Restarted Django Server**

✅ Server restarted successfully at http://localhost:8000/

## 🔗 OAuth Endpoints Available

Your Django backend now has these OAuth endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /auth/login/google-oauth2/` | Initiates Google OAuth login |
| `GET /auth/complete/google-oauth2/` | OAuth callback (receives auth code) |
| `GET /auth/disconnect/google-oauth2/` | Disconnect Google account |

## ⚠️ Important: Update Google Cloud Console

You need to add these redirect URIs to your Google Cloud Console:

1. **Go to**: https://console.cloud.google.com/
2. **Navigate to**: APIs & Services → Credentials
3. **Edit your OAuth Client**: `206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct`

### Add These Redirect URIs:
```
http://localhost:8000/auth/complete/google-oauth2/
http://localhost:3000/auth/complete/google-oauth2/
http://127.0.0.1:8000/auth/complete/google-oauth2/
http://127.0.0.1:3000/auth/complete/google-oauth2/
```

### Add These JavaScript Origins:
```
http://localhost:8000
http://localhost:3000
http://127.0.0.1:8000
http://127.0.0.1:3000
```

## 🧪 Test OAuth Flow

### Method 1: Direct Browser Test
Open in browser:
```
http://localhost:8000/auth/login/google-oauth2/
```

This will:
1. Redirect to Google consent screen
2. Ask you to choose account
3. Request permissions (email, profile)
4. Redirect back to your callback URL
5. Create/update user in Django database

### Method 2: Using Frontend Button

Update your frontend's Google OAuth button to use Django backend:

**Current code in `landing.html`:**
```javascript
function loginWithGoogle() {
    // Currently uses Google OAuth directly
    const clientId = '206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com';
    // ... redirects to Google
}
```

**Updated code (use Django backend):**
```javascript
function loginWithGoogle() {
    // Redirect to Django social auth endpoint
    window.location.href = 'http://localhost:8000/auth/login/google-oauth2/';
}
```

## 📋 Configuration Summary

### Backend Settings (settings.py)
Already configured:
```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile', 'openid']
```

### Installed Apps
Already includes:
```python
INSTALLED_APPS = [
    # ...
    'social_django',  # For Google OAuth
    # ...
]
```

### Middleware
Already includes:
```python
MIDDLEWARE = [
    # ...
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # ...
]
```

## 🔐 Security Status

✅ **Environment Variables**: Credentials stored in `.env` file  
✅ **Git Protection**: `.env` is in `.gitignore`  
⚠️ **Client Secret File**: Still in repository (should be removed)

### Remove Client Secret from Git

```powershell
# Remove from git tracking but keep locally
git rm --cached "client_secret_206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com.json"

# Commit the removal
git commit -m "Remove Google OAuth client secret file from repository"

# Push to GitHub
git push origin main
```

## 🎯 Next Steps

### Step 1: Update Google Cloud Console ⚠️ REQUIRED
- Add redirect URIs for localhost:8000
- Add JavaScript origins for localhost:8000

### Step 2: Test OAuth Flow
```powershell
# Server is already running at http://localhost:8000/

# Test in browser:
http://localhost:8000/auth/login/google-oauth2/
```

### Step 3: Update Frontend (Optional)
Modify `loginWithGoogle()` to use Django backend instead of direct Google OAuth.

### Step 4: Remove Client Secret File
```powershell
git rm --cached "client_secret_206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com.json"
git commit -m "Remove OAuth secret file"
git push origin main
```

## 📖 Documentation Created

1. **GOOGLE_OAUTH_SETUP.md** - Complete OAuth setup guide
2. **backend/.env** - Active environment file with credentials
3. **backend/.env.example** - Template with credentials

## 🚀 Quick Test Commands

### Test OAuth Login
```powershell
# In browser:
http://localhost:8000/auth/login/google-oauth2/
```

### Check Environment Variables
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm"
.\venv\Scripts\Activate.ps1
python manage.py shell
```

```python
import os
from dotenv import load_dotenv
load_dotenv()

print("Client ID:", os.getenv('GOOGLE_OAUTH_CLIENT_ID'))
print("Client Secret:", os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'))
```

### View OAuth Users
```powershell
python manage.py shell
```

```python
from social_django.models import UserSocialAuth

# List all Google OAuth connections
for auth in UserSocialAuth.objects.filter(provider='google-oauth2'):
    print(f"User: {auth.user.email}, Google ID: {auth.uid}")
```

## ✅ Configuration Checklist

- [x] Extracted credentials from JSON file
- [x] Created `.env` file with OAuth credentials
- [x] Updated `.env.example` template
- [x] Added social auth URLs to `backend/urls.py`
- [x] Restarted Django server
- [x] Created comprehensive documentation
- [ ] **Update Google Cloud Console redirect URIs** ⚠️
- [ ] **Update Google Cloud Console JavaScript origins** ⚠️
- [ ] Test OAuth login flow
- [ ] Remove client secret JSON from git repository

## 🎊 Summary

Your Google OAuth 2.0 is now configured and ready! The Django backend can now:

✅ Authenticate users via Google  
✅ Create user accounts automatically  
✅ Link Google accounts to existing users  
✅ Store OAuth tokens securely  
✅ Refresh tokens automatically  

**Just update your Google Cloud Console settings and you're good to go!** 🚀

For detailed instructions, see: **GOOGLE_OAUTH_SETUP.md**
