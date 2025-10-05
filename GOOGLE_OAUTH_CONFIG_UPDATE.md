# 🔧 Google OAuth Configuration Update Required

## 📋 Current Configuration

Your OAuth client is currently configured for:
- **Redirect URI**: `http://localhost:3000/auth/google/callback`
- **JavaScript Origin**: `http://localhost:3000`

## ⚠️ Required Changes

You need to add additional URIs to support the Oursfolio portfolio setup.

---

## 🚀 Step-by-Step Instructions

### Step 1: Go to Google Cloud Console

Open this URL in your browser:
```
https://console.cloud.google.com/apis/credentials?project=oursfolio-portfolio-474212
```

Or manually:
1. Go to: https://console.cloud.google.com/
2. Select project: **oursfolio-portfolio-474212**
3. Navigate to: **APIs & Services** → **Credentials**

### Step 2: Find Your OAuth 2.0 Client ID

Look for:
```
Client ID: 206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com
Type: Web application
```

Click the **pencil icon (✏️)** to edit.

### Step 3: Add Authorized JavaScript Origins

In the **Authorized JavaScript origins** section, ADD these URLs (keep existing ones):

```
http://localhost:3000
http://localhost:8000
http://localhost:5500
http://127.0.0.1:8000
http://127.0.0.1:5500
```

**Why multiple ports?**
- Port 3000: Original configuration
- Port 8000: Python HTTP server (recommended)
- Port 5500: VS Code Live Server
- 127.0.0.1: Alternative localhost address

### Step 4: Add Authorized Redirect URIs

In the **Authorized redirect URIs** section, ADD these URLs (keep existing ones):

```
http://localhost:3000/auth/google/callback
http://localhost:8000/frontend/auth-callback.html
http://localhost:8000/auth-callback.html
http://localhost:5500/frontend/auth-callback.html
http://127.0.0.1:8000/frontend/auth-callback.html
http://127.0.0.1:8000/auth-callback.html
```

### Step 5: Save Changes

1. Scroll to the bottom
2. Click **SAVE**
3. Wait 5-10 minutes for changes to propagate

---

## 📸 Visual Guide

### What Your Configuration Should Look Like:

#### Authorized JavaScript Origins:
```
✓ http://localhost:3000
✓ http://localhost:8000
✓ http://localhost:5500
✓ http://127.0.0.1:8000
✓ http://127.0.0.1:5500
```

#### Authorized Redirect URIs:
```
✓ http://localhost:3000/auth/google/callback
✓ http://localhost:8000/frontend/auth-callback.html
✓ http://localhost:8000/auth-callback.html
✓ http://localhost:5500/frontend/auth-callback.html
✓ http://127.0.0.1:8000/frontend/auth-callback.html
✓ http://127.0.0.1:8000/auth-callback.html
```

---

## 🧪 Testing After Configuration

### Option 1: Using Python HTTP Server (Recommended)

1. Open PowerShell in your project folder:
   ```powershell
   cd "C:\Users\Administrator\Desktop\Final Midterm"
   python -m http.server 8000
   ```

2. Open browser:
   ```
   http://localhost:8000/frontend/landing.html
   ```

3. Click "Login" → "Sign in with Google"

### Option 2: Using VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `landing.html` → "Open with Live Server"
3. It will open at `http://localhost:5500/frontend/landing.html`
4. Click "Login" → "Sign in with Google"

---

## ✅ Expected Behavior

### Successful Flow:
1. Click "Sign in with Google" button
2. Redirected to Google login page
3. Select your Google account
4. Grant permissions
5. Redirected back to `auth-callback.html`
6. Automatically extracts email from token
7. Redirected back to landing page
8. 2FA modal opens automatically
9. Scan QR code or enter 6-digit code
10. Login successful! ✅

### Error: "redirect_uri_mismatch"
**Cause**: The redirect URI is not configured in Google Cloud Console

**Solution**:
1. Check the error message for the exact URI being used
2. Add that exact URI to Google Cloud Console
3. Wait 5-10 minutes
4. Try again

### Error: "Access blocked: Authorization Error"
**Cause**: JavaScript origin not configured

**Solution**:
1. Add the origin URL to "Authorized JavaScript origins"
2. Make sure it matches exactly (http vs https, port number)
3. Wait 5-10 minutes
4. Try again

---

## 🔒 Security Notes

### For Development:
- Using `http://localhost` is OK for testing
- Client ID can be public (it's in frontend code)
- Client Secret should be kept private (don't commit to Git)

### For Production:
- **Must use HTTPS** (not HTTP)
- Update redirect URIs to your production domain
- Example:
  ```
  https://oursfolio.com/auth-callback.html
  https://www.oursfolio.com/auth-callback.html
  ```

---

## 📁 Files Already Configured

### ✅ `frontend/landing.html`
- Google OAuth button enabled
- Client ID: `206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com`
- Redirect handling ready

### ✅ `frontend/auth-callback.html`
- JWT token parsing
- Email extraction
- Auto-redirect to landing page
- Opens 2FA modal

### ✅ OAuth Configuration
- Client ID: Ready
- Client Secret: Available (if needed)
- Project ID: oursfolio-portfolio-474212

---

## 🐛 Troubleshooting

### Problem: "redirect_uri_mismatch"
```
Error 400: redirect_uri_mismatch
The redirect URI in the request, http://localhost:8000/frontend/auth-callback.html, 
does not match the ones authorized for the OAuth client.
```

**Solution**: Add the exact URI shown in error to Google Cloud Console

### Problem: Google OAuth works but 2FA doesn't open
**Solution**: Check browser console for JavaScript errors

### Problem: Stuck on auth-callback.html page
**Solution**: 
1. Check if `landing.html` is in the correct path
2. Open browser console to see error messages
3. Make sure both files are served from same origin

### Problem: Changes don't take effect
**Solution**: 
1. Clear browser cache (Ctrl + Shift + Delete)
2. Try incognito mode
3. Wait 10-15 minutes for Google changes to propagate

---

## 📞 Quick Help

### Check Current Configuration:
```javascript
// Open browser console on landing.html and run:
console.log('Client ID:', '206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com');
console.log('Current URL:', window.location.href);
console.log('Expected Redirect:', window.location.origin + '/frontend/auth-callback.html');
```

### Test OAuth URL Manually:
```
https://accounts.google.com/o/oauth2/v2/auth?client_id=206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct.apps.googleusercontent.com&redirect_uri=http://localhost:8000/frontend/auth-callback.html&response_type=token%20id_token&scope=email%20profile%20openid&nonce=test123
```

Replace `localhost:8000` with your actual server URL.

---

## ✨ Summary

1. **Go to**: https://console.cloud.google.com/apis/credentials?project=oursfolio-portfolio-474212
2. **Edit**: OAuth 2.0 Client (206414229595...)
3. **Add Origins**: localhost:8000, localhost:5500, etc.
4. **Add Redirects**: /frontend/auth-callback.html paths
5. **Save** and wait 5-10 minutes
6. **Test**: Start server and try Google login

**Need help?** Check the troubleshooting section above! 🚀
