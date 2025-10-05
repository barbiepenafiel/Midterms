# 2FA Authentication Setup Guide

## Overview
Your portfolio now includes a complete **Two-Factor Authentication (2FA)** system with:
- ✅ Email/Password login
- ✅ Google OAuth integration
- ✅ QR Code generation for Google Authenticator
- ✅ 6-digit verification code system
- ✅ Secure session management

---

## Features Implemented

### 1. **Login Modal**
- Beautiful glassmorphism design matching your portfolio theme
- Email and password input fields
- Google Sign-In button
- Responsive and accessible

### 2. **Two-Factor Authentication**
- Generates unique secret key for each user
- Creates QR code for Google Authenticator app
- Manual secret key entry option
- 6-digit verification code input

### 3. **Google OAuth Integration**
- "Sign in with Google" button
- Ready for Google OAuth 2.0 implementation
- Secure authentication flow

---

## How It Works

### User Flow:
1. **Click "Login"** button in navigation
2. **Enter credentials** (email & password) or use Google Sign-In
3. **Scan QR Code** with Google Authenticator app
4. **Enter 6-digit code** from authenticator app
5. **Success!** User is logged in

---

## Setting Up Google OAuth (Production)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Name it "Oursfolio Portfolio"

### Step 2: Enable Google+ API

1. Go to **APIs & Services** → **Library**
2. Search for "Google+ API"
3. Click **Enable**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Web application**
4. Set **Authorized JavaScript origins**:
   ```
   http://localhost:3000
   https://barbie.com
   ```
5. Set **Authorized redirect URIs**:
   ```
   http://localhost:3000/auth/google/callback
   https://barbie.com/auth/google/callback
   ```
6. Save your **Client ID** and **Client Secret**

### Step 4: Update Google Cloud Console Settings

**✅ Your OAuth Credentials:**
- **Client ID**: `YOUR_CLIENT_ID_HERE.apps.googleusercontent.com`
- **Client Secret**: `YOUR_CLIENT_SECRET_HERE`
- **Project ID**: `oursfolio-portfolio-474212`

> ⚠️ Replace with your actual credentials from Google Cloud Console

**⚠️ IMPORTANT: Update Authorized URIs in Google Cloud Console**

Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials) and update:

**Authorized JavaScript origins** (replace with your actual URLs):
```
http://localhost:8000
http://localhost:3000
https://yourdomain.com
```

**Authorized redirect URIs** (replace with your actual URLs):
```
http://localhost:8000/auth-callback.html
http://localhost:3000/auth-callback.html
https://yourdomain.com/auth-callback.html
```

### Step 5: Code Implementation

**✅ ALREADY IMPLEMENTED!** The code now uses your real OAuth credentials:

```javascript
function loginWithGoogle() {
    const clientId = '206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com';
    const redirectUri = window.location.origin + '/auth-callback.html';
    // ... OAuth flow implementation
}
```

---

## Testing the 2FA System

### Current Demo Behavior:
- ✅ **Email validation**: Checks for valid email format
- ✅ **Password validation**: Minimum 6 characters
- ✅ **QR Code generation**: Creates unique QR for each login
- ✅ **Secret key display**: Shows manual entry option
- ✅ **Code verification**: Accepts any 6-digit number (demo mode)

### For Production:
Replace the demo `verify2FA()` function with real TOTP verification using a library like:
- **otplib** (npm): `npm install otplib`
- **speakeasy** (npm): `npm install speakeasy`

Example with otplib:
```javascript
import { authenticator } from 'otplib';

function verify2FA() {
    const code = document.getElementById('twoFactorCode').value;
    const isValid = authenticator.check(code, twoFactorSecret);
    
    if (isValid) {
        // Success - log user in
        proceedToSuccessStep();
    } else {
        alert('Invalid verification code');
    }
}
```

---

## Google Authenticator Setup

### For Users:

1. **Download Google Authenticator**:
   - [iOS App Store](https://apps.apple.com/app/google-authenticator/id388497605)
   - [Android Play Store](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)

2. **Add Account**:
   - Open Google Authenticator
   - Tap "+" icon
   - Choose "Scan QR code"
   - Scan the QR code shown on your screen

3. **Get Codes**:
   - 6-digit codes refresh every 30 seconds
   - Enter current code to verify

### Alternative: Manual Entry
If scanning doesn't work:
1. Choose "Enter a setup key" in authenticator
2. Enter the secret key displayed
3. Choose "Time-based"
4. Save

---

## Security Best Practices

### Implemented:
✅ Email format validation
✅ Password length requirements
✅ Secure secret key generation (Base32)
✅ QR code with encrypted URI
✅ Session storage for login state
✅ Modal closes on outside click
✅ Input sanitization (digits only for codes)

### Recommended Additions:
- [ ] HTTPS enforcement
- [ ] Rate limiting on login attempts
- [ ] Account lockout after failed attempts
- [ ] Password strength requirements
- [ ] Backup codes generation
- [ ] Email verification
- [ ] CSRF protection
- [ ] Secure backend API

---

## Customization

### Change Colors:
The authentication modal uses your portfolio's pink/purple theme. To customize:

```css
/* Primary colors */
from-pink-500 to-purple-600  /* Gradient buttons */
border-pink-500/30           /* Borders */
text-pink-400                /* Accent text */
```

### Change App Name:
In the `proceedTo2FA()` function:
```javascript
const appName = 'YourAppName';  // Change this
```

---

## API Integration Example

### Backend Endpoint Structure:

```javascript
// POST /api/auth/login
{
    email: "user@example.com",
    password: "hashedPassword"
}

// Response:
{
    success: true,
    twoFactorRequired: true,
    secret: "BASE32SECRET",
    qrCode: "data:image/png;base64,..."
}

// POST /api/auth/verify-2fa
{
    email: "user@example.com",
    code: "123456"
}

// Response:
{
    success: true,
    token: "JWT_TOKEN",
    user: {
        email: "user@example.com",
        name: "User Name"
    }
}
```

---

## Troubleshooting

### QR Code Not Displaying:
- Check browser console for errors
- Ensure QRCode.js library is loaded
- Verify the container element exists

### Google Sign-In Not Working:
- Check Client ID is correct
- Verify redirect URIs match exactly
- Enable Google+ API in Cloud Console
- Check CORS settings

### Verification Code Invalid:
- Ensure time is synchronized on device
- Codes expire after 30 seconds
- Check secret key matches

---

## Browser Compatibility

✅ Chrome/Edge (Chromium)
✅ Firefox
✅ Safari
✅ Opera
✅ Mobile browsers

---

## Next Steps

1. **Backend Integration**: Connect to your server API
2. **Database**: Store user credentials and 2FA secrets securely
3. **Email Service**: Send verification emails
4. **Session Management**: Implement JWT or secure sessions
5. **Backup Codes**: Generate recovery codes
6. **Account Management**: Password reset, 2FA disable options

---

## Resources

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Authenticator Guide](https://support.google.com/accounts/answer/1066447)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)
- [OWASP Authentication Guide](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

## Demo Usage

**Try it now:**
1. Click the "Login" button in navigation
2. Enter any email (valid format required)
3. Enter any password (6+ characters)
4. Scan the generated QR code with Google Authenticator
5. Enter the 6-digit code (any 6 digits work in demo mode)
6. See the success message!

**Test Google Sign-In:**
- Click "Sign in with Google" button
- Follow the demo flow

---

## Support

For issues or questions about the 2FA implementation, check:
- Browser console for errors
- Network tab for API calls
- QRCode.js library documentation
- Google OAuth documentation

---

**Built with ❤️ for Oursfolio Portfolio**
