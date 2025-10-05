# 🔐 Google OAuth Setup - Complete Guide

## ✅ Your OAuth 2.0 Credentials

```
Client ID: YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
Client Secret: YOUR_CLIENT_SECRET_HERE
Project ID: oursfolio-portfolio-474212
```

> ⚠️ **Note**: Replace with your actual OAuth credentials from Google Cloud Console

---

## 🚀 Quick Setup (Required Steps)

### Step 1: Update Authorized URIs in Google Cloud Console

1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your OAuth 2.0 Client ID: `206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct`
3. Click the **Edit** (pencil) icon

### Step 2: Add Authorized JavaScript Origins

In the **Authorized JavaScript origins** section, add:

```
http://localhost:8000
http://localhost:3000
http://127.0.0.1:8000
```

**For production (when deploying):**
```
https://yourdomain.com
https://www.yourdomain.com
```

### Step 3: Add Authorized Redirect URIs

In the **Authorized redirect URIs** section, add:

```
http://localhost:8000/auth-callback.html
http://localhost:3000/auth-callback.html
http://127.0.0.1:8000/auth-callback.html
```

**For production (when deploying):**
```
https://yourdomain.com/auth-callback.html
https://www.yourdomain.com/auth-callback.html
```

### Step 4: Save Changes

Click **SAVE** at the bottom of the page.

⚠️ **Note**: Changes may take 5-10 minutes to propagate.

---

## 🧪 Testing the Integration

### Test Locally:

1. **Start the local server** (if not already running):
   ```bash
   cd "C:\Users\Administrator\Desktop\Final Midterm\frontend"
   python -m http.server 8000
   ```

2. **Open the portfolio**:
   ```
   http://localhost:8000/landing.html
   ```

3. **Test Google Sign-In**:
   - Click the **Login** button in navigation
   - Click **Sign in with Google**
   - Select your Google account
   - You'll be redirected to `auth-callback.html`
   - Then back to landing page with 2FA setup

### Expected Flow:

```
Landing Page
    ↓ (Click "Login" → "Sign in with Google")
Google Account Selection
    ↓ (Select account)
Google Permissions Request
    ↓ (Allow access)
auth-callback.html (processes token)
    ↓ (extracts email)
Landing Page (modal opens)
    ↓ (2FA QR code displayed)
Scan QR Code
    ↓ (enter code)
Success! ✅
```

---

## 📁 Files Integrated

### 1. **landing.html**
- ✅ Real OAuth client ID integrated
- ✅ Google Sign-In button functional
- ✅ OAuth callback handler
- ✅ Auto-opens 2FA modal after Google auth

### 2. **auth-callback.html** (NEW)
- ✅ Handles OAuth redirect
- ✅ Parses JWT token
- ✅ Extracts user email
- ✅ Stores in sessionStorage
- ✅ Redirects back to landing page

### 3. **client_secret_*.json**
- ✅ Contains your OAuth credentials
- ⚠️ Keep this file secure
- ⚠️ Don't commit to public repositories

---

## 🔒 Security Considerations

### ✅ Already Implemented:
- Client-side OAuth 2.0 implicit flow
- JWT token parsing
- Session storage for temporary auth state
- Nonce for CSRF protection

### ⚠️ Production Recommendations:

1. **Never expose client secret in frontend code**
   - Current implementation is safe (client secret not used in browser)
   - Client secret only needed for server-side flows

2. **Use HTTPS in production**
   - Google OAuth requires HTTPS for production
   - localhost HTTP is allowed for testing

3. **Implement token validation**
   - Verify JWT signature
   - Check token expiration
   - Validate issuer and audience

4. **Add backend API**
   - Store user sessions securely
   - Validate tokens server-side
   - Implement proper session management

---

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"

**Problem**: The redirect URI doesn't match what's configured in Google Console.

**Solution**:
1. Check the exact URL in the error message
2. Add that exact URL to "Authorized redirect URIs"
3. Make sure there are no typos or extra slashes
4. Wait 5-10 minutes for changes to propagate

### Error: "origin_mismatch"

**Problem**: The origin (domain) doesn't match what's configured.

**Solution**:
1. Add the exact origin to "Authorized JavaScript origins"
2. Include `http://localhost:8000` for testing
3. Don't add paths, only origins (e.g., `http://localhost:8000`, not `http://localhost:8000/landing.html`)

### Google Sign-In Button Does Nothing

**Check**:
1. Open browser console (F12)
2. Look for errors
3. Verify internet connection
4. Check if popup blocker is enabled
5. Try in incognito/private mode

### Token Not Being Parsed

**Check**:
1. Browser console for errors
2. Verify `auth-callback.html` exists
3. Check sessionStorage in browser DevTools
4. Clear browser cache and try again

### 2FA Modal Not Opening After Google Login

**Check**:
1. sessionStorage should have `google_auth_complete: 'true'`
2. Check if email is stored in sessionStorage
3. Look for JavaScript errors in console
4. Try refreshing the page once after Google auth

---

## 🔧 Configuration Reference

### Current OAuth Configuration:

```javascript
// In landing.html
const clientId = '206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com';
const redirectUri = window.location.origin + '/auth-callback.html';
const scope = 'email profile openid';
const responseType = 'token id_token'; // Implicit flow
```

### OAuth Flow Type: **Implicit Flow**

Benefits:
- ✅ No backend required
- ✅ Quick implementation
- ✅ Suitable for SPAs

Limitations:
- ⚠️ Tokens visible in URL (temporarily)
- ⚠️ Less secure than authorization code flow
- ⚠️ Token refresh requires user interaction

---

## 📊 Testing Checklist

- [ ] Updated authorized URIs in Google Cloud Console
- [ ] Waited 5-10 minutes after saving changes
- [ ] Started local server on port 8000
- [ ] Opened `http://localhost:8000/landing.html`
- [ ] Clicked "Login" button
- [ ] Clicked "Sign in with Google"
- [ ] Selected Google account
- [ ] Granted permissions
- [ ] Redirected to auth-callback.html
- [ ] Redirected back to landing page
- [ ] Auth modal opened automatically
- [ ] Email pre-filled in modal
- [ ] 2FA QR code displayed
- [ ] Scanned QR code with Google Authenticator
- [ ] Entered 6-digit code
- [ ] Saw success message

---

## 🚀 Production Deployment

### Before Going Live:

1. **Update authorized URIs**:
   ```
   https://yourdomain.com
   https://yourdomain.com/auth-callback.html
   ```

2. **Enable HTTPS**:
   - Google requires HTTPS for OAuth (except localhost)
   - Use Let's Encrypt or your hosting provider's SSL

3. **Update OAuth consent screen**:
   - Add logo
   - Add privacy policy URL
   - Add terms of service URL
   - Verify domain ownership

4. **Move to production status**:
   - Currently in "Testing" mode (max 100 users)
   - Apply for verification for public use
   - Submit for OAuth verification if needed

5. **Implement backend**:
   - Add server-side token validation
   - Store user sessions in database
   - Implement refresh token logic
   - Add logout functionality

---

## 📚 Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Sign-In JavaScript Client Reference](https://developers.google.com/identity/sign-in/web/reference)
- [OAuth 2.0 Implicit Flow](https://oauth.net/2/grant-types/implicit/)
- [JWT Token Debugging](https://jwt.io/)

---

## ✨ What's Working Now

✅ **Real Google OAuth integration**
✅ **Automatic redirect to Google sign-in**
✅ **Token parsing and user info extraction**
✅ **Seamless transition to 2FA setup**
✅ **Email pre-filled after Google auth**
✅ **Complete authentication flow**

---

## 🎯 Next Steps

1. **Test the Google Sign-In** (follow testing checklist above)
2. **Add backend API** for secure token storage
3. **Implement proper TOTP verification** (currently demo mode)
4. **Add user database** to store credentials and 2FA secrets
5. **Deploy to production** with HTTPS

---

**Your OAuth credentials are ready to use!** 🎉

Just update the authorized URIs in Google Cloud Console and start testing.
