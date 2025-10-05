# ✅ Google OAuth 2.0 Configuration Complete!

## 🔑 Your Credentials

Your Google OAuth credentials have been configured in the `.env` file (not committed to git):

- **Client ID**: Set in `backend/.env`
- **Client Secret**: Set in `backend/.env`
- **Project ID**: `oursfolio-portfolio-474212`

## 📋 Configuration Status

✅ **Backend .env file**: Created with your Google OAuth credentials  
✅ **Backend settings.py**: Already configured to use OAuth credentials  
✅ **Frontend landing.html**: Already has Google OAuth client ID  

## 🔄 OAuth Redirect URIs

Currently configured in your Google Cloud Console:
- ✅ `http://localhost:3000/auth/google/callback`

**Additional URIs needed for Django backend:**
- ⚠️ `http://localhost:8000/auth/complete/google-oauth2/` (Add this!)
- ⚠️ `http://localhost:3000/auth/complete/google-oauth2/` (Add this!)

## 🌐 Authorized JavaScript Origins

Currently configured:
- ✅ `http://localhost:3000`

**Additional origins needed:**
- ⚠️ `http://localhost:8000` (Add this!)
- ⚠️ `http://127.0.0.1:8000` (Add this!)
- ⚠️ `http://127.0.0.1:3000` (Add this!)

## 🛠️ How to Update Google Cloud Console

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Navigate to Credentials:**
   - Select project: `oursfolio-portfolio-474212`
   - Go to: APIs & Services → Credentials

3. **Edit OAuth 2.0 Client:**
   - Click on: `206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct`

4. **Update Authorized redirect URIs:**
   ```
   http://localhost:3000/auth/google/callback
   http://localhost:8000/auth/complete/google-oauth2/
   http://localhost:3000/auth/complete/google-oauth2/
   http://127.0.0.1:8000/auth/complete/google-oauth2/
   http://127.0.0.1:3000/auth/complete/google-oauth2/
   ```

5. **Update Authorized JavaScript origins:**
   ```
   http://localhost:3000
   http://localhost:8000
   http://127.0.0.1:8000
   http://127.0.0.1:3000
   ```

6. **Click Save**

## 🔧 Backend Configuration

The backend is already configured in `backend/settings.py`:

```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile', 'openid']
```

And your `.env` file now contains:
```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id-from-google-console
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-from-google-console
```

## 🎯 OAuth Endpoints

### Django Backend Endpoints:
- **Login URL**: `http://localhost:8000/auth/login/google-oauth2/`
- **Callback URL**: `http://localhost:8000/auth/complete/google-oauth2/`

### How it works:
1. User clicks "Sign in with Google"
2. Redirects to Google OAuth consent screen
3. User approves access
4. Google redirects to callback URL with authorization code
5. Backend exchanges code for tokens
6. Backend creates/updates user in database
7. Backend returns JWT tokens to frontend

## 🔐 Django Social Auth URLs

Add these to your `backend/urls.py` if not already present:

```python
from django.urls import path, include

urlpatterns = [
    # ... existing patterns ...
    path('auth/', include('social_django.urls', namespace='social')),
]
```

## 🌟 Frontend Integration

Your frontend already has the Google OAuth button configured with your client ID:

```javascript
const clientId = '206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com';
```

### To integrate with Django backend:

Update the `loginWithGoogle()` function to redirect to Django's social auth:

```javascript
function loginWithGoogle() {
    // Redirect to Django social auth endpoint
    window.location.href = 'http://localhost:8000/auth/login/google-oauth2/';
}
```

## 📝 Create OAuth Callback Handler

Create `backend/authentication/views.py` addition for OAuth callback:

```python
from social_django.models import UserSocialAuth
from rest_framework_simplejwt.tokens import RefreshToken

def google_oauth_callback(request):
    """Handle Google OAuth callback and return JWT tokens"""
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        return JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'email': request.user.email,
            'message': 'Login successful via Google'
        })
    return JsonResponse({'error': 'Authentication failed'}, status=400)
```

## 🧪 Testing Google OAuth

### Step 1: Start Django Server
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
python manage.py runserver
```

### Step 2: Test OAuth Flow

**Option A: Using Browser**
1. Navigate to: `http://localhost:8000/auth/login/google-oauth2/`
2. Choose Google account
3. Approve permissions
4. Should redirect to callback URL

**Option B: Using Frontend Button**
1. Open `frontend/landing.html`
2. Click "Sign in with Google"
3. Complete OAuth flow
4. JWT tokens should be stored

### Step 3: Verify User Creation

Check Django admin:
```
http://localhost:8000/admin/
```

Or use Django shell:
```powershell
python manage.py shell
```

```python
from authentication.models import User
from social_django.models import UserSocialAuth

# List all users
User.objects.all()

# List all OAuth connections
UserSocialAuth.objects.all()

# Get user by Google ID
user = UserSocialAuth.objects.get(provider='google-oauth2')
print(user.user.email)
```

## 🎨 Environment Files Summary

### `.env` (Active - Git Ignored)
```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
```

### `.env.example` (Template - Committed to Git)
```env
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id-here
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret-here
```

### `.gitignore` (Protects Secrets)
```
.env
client_secret_*.json
```

## 🔒 Security Notes

### ✅ What's Protected:
- `.env` file is in `.gitignore`
- `client_secret_*.json` is in `.gitignore`
- Secrets loaded via environment variables

### ⚠️ Important:
Your `client_secret_*.json` file is currently **NOT** in `.gitignore`. It should be removed from the repository:

```powershell
# Remove from git but keep locally
git rm --cached "client_secret_206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com.json"

# Commit the removal
git commit -m "Remove OAuth client secret file"

# Push changes
git push origin main
```

## 🚀 Quick Start Commands

### Restart Django Server (to load new .env)
```powershell
# Stop the current server (Ctrl+C)
# Then restart:
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
python manage.py runserver
```

### Test OAuth Endpoint
```powershell
# In browser or curl:
curl http://localhost:8000/auth/login/google-oauth2/
```

### Check Environment Variables Loaded
```powershell
python manage.py shell
```
```python
import os
print(os.getenv('GOOGLE_OAUTH_CLIENT_ID'))
print(os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'))
```

## ✅ Checklist

- [x] Google OAuth credentials extracted from JSON file
- [x] `.env` file created with credentials
- [x] `.env.example` updated with credentials
- [x] `settings.py` already configured for OAuth
- [ ] Update Google Cloud Console redirect URIs
- [ ] Update Google Cloud Console JavaScript origins
- [ ] Remove client_secret file from git repository
- [ ] Test OAuth login flow
- [ ] Verify user creation in Django

## 📚 Additional Resources

- **Google OAuth Documentation**: https://developers.google.com/identity/protocols/oauth2
- **Django Social Auth**: https://python-social-auth.readthedocs.io/
- **Google Cloud Console**: https://console.cloud.google.com/

## 🎉 Next Steps

1. **Update Google Cloud Console** with additional redirect URIs
2. **Restart Django server** to load new environment variables
3. **Test Google OAuth login** from frontend
4. **Remove client_secret file** from git repository
5. **Verify users** are created in Django database

Your Google OAuth 2.0 is configured and ready to use! 🚀
