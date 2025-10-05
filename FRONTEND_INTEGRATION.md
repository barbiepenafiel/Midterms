# Frontend-Backend Integration Guide

## Overview
The frontend has been successfully connected to the Django REST API backend. All authentication operations now use real API endpoints instead of localStorage.

## What Changed

### 1. API Configuration
- **Base URL**: `http://localhost:8000/api`
- **Authentication**: JWT tokens (Bearer authentication)
- **Token Storage**: localStorage (access_token, refresh_token)

### 2. Token Management Functions

#### New Functions Added:
```javascript
getAccessToken()          // Retrieve JWT access token
getRefreshToken()         // Retrieve JWT refresh token
setTokens(access, refresh) // Store both tokens
clearTokens()             // Remove all tokens and user data
isAuthenticated()         // Check if user has valid token
refreshAccessToken()      // Refresh expired access token
fetchWithAuth(url, options) // Make authenticated API calls with auto-refresh
```

### 3. Updated Authentication Functions

#### Registration (`registerUser()`)
- **Endpoint**: POST `/api/auth/register/`
- **Payload**: `{ username, email, password, password2 }`
- **Success**: Shows success message, switches to login
- **Error Handling**: Displays server validation errors

#### Login (`proceedTo2FA()`)
- **Endpoint**: POST `/api/auth/login/`
- **Payload**: `{ email, password }`
- **Response Scenarios**:
  - **2FA Enabled**: Returns `{ requires_2fa: true, user_id, email }`
  - **2FA Disabled**: Returns `{ access, refresh, email }`
- **Token Storage**: Stores JWT tokens on successful login

#### 2FA Verification (`verify2FA()`)
- **Endpoint**: POST `/api/auth/2fa/verify/`
- **Payload**: `{ user_id, token }` (6-digit code)
- **Success**: Returns JWT tokens, completes login
- **Error Handling**: Displays verification errors

#### Logout (`logout()`)
- **Endpoint**: POST `/api/auth/logout/`
- **Headers**: `Authorization: Bearer {access_token}`
- **Action**: Clears all tokens, updates UI

#### Login State (`updateLoginButton()`)
- **Changed From**: `sessionStorage.getItem('isLoggedIn')`
- **Changed To**: `isAuthenticated()` (checks JWT token existence)
- **User Data**: Now reads from localStorage (`user_email`, `user_name`)

## API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login with email/password | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No (refresh token) |
| GET | `/api/auth/2fa/setup/` | Get QR code for 2FA | Yes |
| POST | `/api/auth/2fa/verify/` | Verify 2FA code | No (user_id) |
| POST | `/api/auth/2fa/disable/` | Disable 2FA | Yes |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT | `/api/auth/profile/` | Update user profile | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |
| POST | `/api/auth/logout/` | Logout | Yes |

### Request Examples

#### Register
```javascript
POST /api/auth/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecureP@ss123",
    "password2": "SecureP@ss123"
}

// Response
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "message": "User registered successfully"
}
```

#### Login (No 2FA)
```javascript
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecureP@ss123"
}

// Response
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "email": "john@example.com"
}
```

#### Login (With 2FA)
```javascript
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecureP@ss123"
}

// Response
{
    "requires_2fa": true,
    "user_id": 1,
    "email": "john@example.com",
    "message": "Please verify 2FA code"
}
```

#### 2FA Verification
```javascript
POST /api/auth/2fa/verify/
Content-Type: application/json

{
    "user_id": 1,
    "token": "123456"
}

// Response
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Login successful"
}
```

#### Authenticated Request Example
```javascript
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

// Response
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "profile_picture": null,
    "two_factor_enabled": true
}
```

## Data Flow

### Login Flow (Without 2FA)
1. User enters email/password → `proceedTo2FA()`
2. Frontend POSTs to `/api/auth/login/`
3. Backend validates credentials
4. Backend returns JWT tokens
5. Frontend stores tokens in localStorage
6. Frontend updates UI to show logged-in state

### Login Flow (With 2FA)
1. User enters email/password → `proceedTo2FA()`
2. Frontend POSTs to `/api/auth/login/`
3. Backend validates credentials, returns `requires_2fa: true`
4. Frontend shows 2FA verification step
5. User enters 6-digit code → `verify2FA()`
6. Frontend POSTs to `/api/auth/2fa/verify/`
7. Backend verifies code, returns JWT tokens
8. Frontend stores tokens, completes login

### Token Refresh Flow
1. Frontend makes API request with expired access token
2. Backend returns 401 Unauthorized
3. `fetchWithAuth()` automatically calls `/api/auth/token/refresh/`
4. Backend validates refresh token, returns new access token
5. Frontend updates stored access token
6. Frontend retries original request with new token

## Local Storage Keys

| Key | Purpose | Example Value |
|-----|---------|---------------|
| `access_token` | JWT access token (7-day lifetime) | `eyJ0eXAiOiJKV1Q...` |
| `refresh_token` | JWT refresh token (30-day lifetime) | `eyJ0eXAiOiJKV1Q...` |
| `user_email` | User's email address | `john@example.com` |
| `user_name` | User's display name | `johndoe` |
| `pending_user_id` | Temporary user ID during 2FA | `1` (cleared after 2FA) |
| `pending_user_email` | Temporary email during 2FA | `john@example.com` (cleared after 2FA) |

## Testing the Integration

### 1. Start Django Server
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm"
.\venv\Scripts\Activate.ps1
cd backend
python manage.py runserver
```

Server will be available at: http://localhost:8000/

### 2. Open Frontend
Open `frontend/landing.html` in your browser or serve it:
```powershell
cd frontend
python -m http.server 3000
```

Then visit: http://localhost:3000/landing.html

### 3. Test Registration
1. Click "Sign In / Register" button
2. Click "Don't have an account? Register"
3. Fill in:
   - Username: at least 6 characters
   - Email: valid email format
   - Password: 8+ chars with letters, numbers, special characters
4. Click "Create Account"
5. Should see success message
6. Check backend terminal for welcome email task

### 4. Test Login (Without 2FA)
1. Click "Sign In / Register"
2. Enter registered email and password
3. Click "Continue to 2FA Verification"
4. Should immediately see success screen (if 2FA not enabled)
5. User dropdown should appear in navigation

### 5. Test 2FA Setup
To enable 2FA for testing:
1. Use Swagger UI: http://localhost:8000/swagger/
2. Login to get access token
3. Call GET `/api/auth/2fa/setup/`
4. Scan QR code with Google Authenticator
5. Call POST `/api/auth/2fa/verify/` with code to enable

### 6. Test Login (With 2FA)
1. Click "Sign In / Register"
2. Enter email/password for user with 2FA enabled
3. Should see QR code step (or message to use existing app)
4. Enter 6-digit code from authenticator app
5. Click "Verify & Login"
6. Should see success screen

### 7. Test Logout
1. Click on user dropdown (top right)
2. Click "Logout"
3. Should see logout confirmation
4. User dropdown should disappear
5. "Sign In / Register" button should reappear

### 8. Test Token Refresh
1. Login successfully
2. Wait until access token expires (or manually delete it from localStorage)
3. Try to access a protected endpoint
4. Should automatically refresh token and retry request

## Error Handling

### Network Errors
```javascript
try {
    const response = await fetch(API_BASE_URL + '/auth/login/', {...});
} catch (error) {
    console.error('Login error:', error);
    showAuthError('Network error. Please check your connection and try again.');
}
```

### API Errors
```javascript
if (response.ok) {
    // Success
} else {
    const data = await response.json();
    let errorMessage = 'Operation failed. ';
    if (data.detail) errorMessage += data.detail;
    else if (data.error) errorMessage += data.error;
    showAuthError(errorMessage);
}
```

### Token Expiration
- Automatically handled by `fetchWithAuth()` function
- Attempts token refresh on 401 response
- Logs user out if refresh fails

## Security Considerations

### What's Implemented
✅ JWT authentication with short-lived tokens (7 days access, 30 days refresh)
✅ CORS configuration for localhost:8000
✅ HTTPS recommended for production
✅ Token rotation on refresh
✅ Account locking after 3 failed attempts
✅ Login history tracking
✅ 2FA support with TOTP

### What's Stored in localStorage
- Access token (automatically expires after 7 days)
- Refresh token (automatically expires after 30 days)
- User email and name (non-sensitive display info)

**Note**: localStorage is used for convenience in this demo. For production:
- Use httpOnly cookies for refresh tokens
- Consider using sessionStorage for access tokens
- Implement XSS protection
- Use secure HTTPS connections

## Next Steps

### Enable 2FA for Your Account
1. Login to the application
2. Go to http://localhost:8000/swagger/
3. Click "Authorize" and enter your JWT token
4. Navigate to `/api/auth/2fa/setup/` endpoint
5. Execute GET request to get QR code
6. Scan QR code with Google Authenticator app
7. Copy 6-digit code from app
8. Navigate to `/api/auth/2fa/verify/` endpoint
9. Execute POST with your user_id and token
10. 2FA is now enabled for your account

### Add Profile Management (Optional)
You can add profile editing features by calling:
- GET `/api/auth/profile/` - View profile
- PUT `/api/auth/profile/` - Update profile
- POST `/api/auth/change-password/` - Change password

### Start Celery Services
To enable background tasks (email, cleanup, etc.):

**Terminal 1 - Celery Worker:**
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
celery -A backend worker --loglevel=info --pool=solo
```

**Terminal 2 - Celery Beat:**
```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\backend"
celery -A backend beat --loglevel=info
```

## Troubleshooting

### Issue: CORS Error
**Error**: `Access to fetch at 'http://localhost:8000/api/auth/login/' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**: Ensure Django backend has CORS configured:
```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]
```

### Issue: Network Error on API Call
**Error**: `TypeError: Failed to fetch`

**Solutions**:
1. Ensure Django server is running: `python manage.py runserver`
2. Check API_BASE_URL is correct: `http://localhost:8000/api`
3. Verify endpoint exists in Swagger UI: http://localhost:8000/swagger/

### Issue: 401 Unauthorized
**Error**: Response status 401

**Solutions**:
1. Check if access token exists: `localStorage.getItem('access_token')`
2. Try refreshing token manually
3. Clear tokens and login again: `clearTokens()`

### Issue: Registration/Login Not Working
**Solutions**:
1. Open browser console (F12) to see detailed errors
2. Check Django server terminal for backend errors
3. Verify user database migrations: `python manage.py migrate`
4. Check Swagger UI to test endpoint directly

### Issue: 2FA Code Not Working
**Solutions**:
1. Ensure code is 6 digits
2. Make sure time is synced on your device
3. Code expires every 30 seconds - enter quickly
4. Verify 2FA is enabled: Check `/api/auth/profile/` → `two_factor_enabled: true`

## Summary

The frontend is now fully integrated with the Django REST API:

✅ **Registration** → Creates users in Django database
✅ **Login** → Authenticates with Django, returns JWT tokens  
✅ **2FA** → Verifies TOTP codes via backend API  
✅ **Token Management** → Automatic refresh on expiration  
✅ **Logout** → Clears tokens, notifies backend  
✅ **UI Updates** → Based on JWT token presence  

All authentication now flows through the Django backend with proper security, validation, and error handling!
