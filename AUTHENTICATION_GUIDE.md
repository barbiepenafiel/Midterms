# Authentication System Guide

## Overview
The Oursfolio portfolio now includes a secure registration and login system with the following features:

## Registration Requirements

### Username
- **Minimum length**: 6 characters
- Can contain letters, numbers, and special characters
- Must be unique across all users

### Password
- **Minimum length**: 8 characters
- **Must contain**:
  - At least one letter (a-z, A-Z)
  - At least one number (0-9)
  - At least one special character (!@#$%^&*(),.?":{}|<>)

### Password Strength Indicator
The registration form includes a real-time password strength indicator:
- **Red (Weak)**: Only 1 requirement met
- **Orange (Fair)**: 2 requirements met
- **Yellow (Good)**: 3 requirements met
- **Green (Strong)**: All 4 requirements met

## Login Security Features

### Failed Login Attempts
- Users are allowed **3 failed login attempts**
- After 3 failed attempts, the account is **automatically blocked**
- Blocked accounts cannot login until unblocked by support

### Login Process
1. Enter username or email
2. Enter password
3. If credentials are correct, proceed to 2FA verification
4. Scan QR code with Google Authenticator app
5. Enter 6-digit verification code
6. Successfully logged in!

## How to Use

### Registration
1. Click the "Login" button in the navbar
2. Click "Don't have an account? Register"
3. Fill in the registration form:
   - Username (min 6 characters)
   - Email address
   - Password (min 8 chars with letters, numbers & special chars)
   - Confirm password
4. Click "Register"
5. After successful registration, you'll be redirected to login

### Login
1. Click the "Login" button in the navbar
2. Enter your username or email
3. Enter your password
4. Click "Continue"
5. Scan the QR code with Google Authenticator
6. Enter the 6-digit code from your authenticator app
7. Click "Verify & Login"

### Google OAuth Login
1. Click the "Login" button in the navbar
2. Click "Sign in with Google"
3. Select your Google account
4. Grant permissions (email, profile)
5. You'll be redirected back to the portfolio
6. The 2FA modal opens automatically
7. Scan the QR code with Google Authenticator
8. Enter the 6-digit code
9. Successfully logged in!

**Note**: Google OAuth now requires 2FA authentication for enhanced security

## Security Notes

### Data Storage
- User data is stored in **browser localStorage** (for demo purposes)
- In production, this should use a secure backend database
- Passwords should be hashed (e.g., bcrypt) before storage

### Session Management
- Login state is stored in **sessionStorage**
- Session expires when browser tab is closed
- In production, use secure HTTP-only cookies with JWT tokens

### Account Recovery
- Currently, blocked accounts need manual intervention
- In production, implement:
  - Password reset functionality
  - Email verification
  - Account recovery options
  - Admin panel for account management

## Testing the System

### Test Registration
```
Username: testuser123
Email: test@example.com
Password: Test@123456
```

### Test Login Blocking
1. Register a new account
2. Try to login with wrong password 3 times
3. Account will be blocked
4. Check browser console to see localStorage data

### View User Database
Open browser console and run:
```javascript
console.log(JSON.parse(localStorage.getItem('userDatabase')));
```

### Reset User Database
To clear all users (for testing):
```javascript
localStorage.clear();
sessionStorage.clear();
```

## Technical Implementation

### Files Modified
- `frontend/landing.html` - Main authentication UI and logic

### Key Functions
- `registerUser()` - Handles user registration with validation
- `validatePassword()` - Validates password requirements
- `validateUsername()` - Validates username requirements
- `checkPasswordStrength()` - Real-time password strength feedback
- `proceedTo2FA()` - Validates credentials and checks login attempts
- `verify2FA()` - Completes the authentication process
- `switchToRegister()` / `switchToLogin()` - Toggle between forms

### LocalStorage Structure
```javascript
{
  "username": {
    "email": "user@example.com",
    "password": "encrypted_password",
    "createdAt": "2025-01-01T00:00:00.000Z",
    "loginAttempts": 0,
    "blocked": false
  }
}
```

## Future Enhancements
- Email verification on registration
- Password reset functionality
- Remember me option
- Session timeout warnings
- Admin dashboard for user management
- Account unlock mechanism
- Password change functionality
- Login history tracking
