# 🚀 Quick Start: Enable Google OAuth Login

## ⚡ 5-Minute Setup

### Step 1: Update Google Cloud Console (REQUIRED)

1. **Go to**: https://console.cloud.google.com/apis/credentials
2. **Sign in** with your Google account
3. **Find your OAuth Client**: `206414229595-4me8f2fdq3usnnapnedkpfgcopnqtgct`
4. **Click Edit** (pencil icon)

### Step 2: Add Authorized JavaScript Origins

Add these URLs:
```
http://localhost:8000
http://127.0.0.1:8000
http://localhost:3000
```

### Step 3: Add Authorized Redirect URIs

Add these URLs:
```
http://localhost:8000/auth-callback.html
http://127.0.0.1:8000/auth-callback.html
http://localhost:3000/auth-callback.html
```

### Step 4: Save Changes

Click **SAVE** at the bottom. Wait 5-10 minutes for changes to take effect.

---

## 🧪 Test It Now!

### 1. Start Local Server

Open PowerShell in the frontend folder:

```powershell
cd "C:\Users\Administrator\Desktop\Final Midterm\frontend"
python -m http.server 8000
```

**Or if Python 3:**
```powershell
python3 -m http.server 8000
```

**Don't have Python?** Use this instead:
```powershell
# Install http-server (one-time)
npm install -g http-server

# Run server
http-server -p 8000
```

### 2. Open in Browser

```
http://localhost:8000/landing.html
```

### 3. Test Google Sign-In

1. Click **"Login"** button in navbar
2. Click **"Sign in with Google"**
3. Select your Google account
4. Grant permissions
5. You're logged in! ✅

---

## ✅ What's Already Configured

✓ **Google OAuth Client ID**: Already in code
✓ **auth-callback.html**: Already created
✓ **OAuth handler**: Already implemented
✓ **Redirect flow**: Already working
✓ **User info extraction**: Already done

**You ONLY need to update Google Cloud Console URIs!**

---

## 🎯 Expected Behavior

### Login Flow:
```
1. Click "Sign in with Google"
   ↓
2. Redirected to Google account selection
   ↓
3. Select account and grant permissions
   ↓
4. Redirected to auth-callback.html (shows loading)
   ↓
5. Automatically redirected back to landing page
   ↓
6. Logged in! Username appears in navbar
```

### What Gets Saved:
- ✓ User email
- ✓ User name
- ✓ Profile picture URL
- ✓ Access token
- ✓ Login state

---

## ⚠️ Troubleshooting

### Error: "Access blocked: Authorization Error"

**Cause**: Authorized URIs not configured in Google Cloud Console

**Solution**: 
1. Go to Google Cloud Console
2. Add the required URIs (see Step 2 & 3 above)
3. Save and wait 5-10 minutes
4. Try again

### Error: "redirect_uri_mismatch"

**Cause**: The redirect URI doesn't match exactly

**Solution**:
1. Copy the EXACT URL from the error message
2. Add it to "Authorized redirect URIs"
3. Make sure no typos or extra slashes
4. Save and wait

### Google Sign-In Button Does Nothing

**Check**:
1. Open browser console (F12) for errors
2. Make sure you're running on `http://localhost:8000`
3. Check if popup blocker is enabled
4. Try in incognito/private mode

### Stuck on "Authenticating..." Page

**Check**:
1. Browser console for JavaScript errors
2. Make sure `auth-callback.html` is in the same folder as `landing.html`
3. Clear browser cache and try again

---

## 📋 Testing Checklist

- [ ] Updated authorized URIs in Google Cloud Console
- [ ] Saved changes and waited 5-10 minutes
- [ ] Started local server on port 8000
- [ ] Opened `http://localhost:8000/landing.html`
- [ ] Clicked "Login" → "Sign in with Google"
- [ ] Selected Google account
- [ ] Saw loading screen on auth-callback.html
- [ ] Redirected back to landing page
- [ ] Username appeared in navbar dropdown
- [ ] Can logout successfully

---

## 🔒 Security Notes

### Current Setup:
- ✅ Uses OAuth 2.0 Implicit Flow
- ✅ Safe for localhost testing
- ✅ No client secret exposed in frontend
- ✅ CSRF protection with nonce

### For Production:
- ⚠️ Must use HTTPS (required by Google)
- ⚠️ Update authorized URIs to your domain
- ⚠️ Consider switching to Authorization Code Flow
- ⚠️ Add backend for token validation
- ⚠️ Store sessions securely in database

---

## 🎉 You Now Have 3 Login Options!

### Option 1: Google OAuth (NEW!)
- Click "Sign in with Google"
- One-click authentication
- No password needed

### Option 2: Register & Login
- Username: min 6 chars
- Password: min 8 chars with letters, numbers & special chars
- 2FA with QR code
- 3-attempt security

### Option 3: Direct 2FA (for testing)
- Enter any username/email
- Enter any password
- Complete 2FA with any 6-digit code

---

## 📚 Full Documentation

For complete setup details, see:
- `GOOGLE_OAUTH_SETUP.md` - Full OAuth guide
- `AUTHENTICATION_GUIDE.md` - Complete auth system docs
- `TESTING_INSTRUCTIONS.md` - Testing procedures

---

## 🚀 Quick Commands Reference

### Start Server (Python):
```powershell
cd frontend
python -m http.server 8000
```

### Start Server (Node.js):
```powershell
cd frontend
npx http-server -p 8000
```

### View Users (Browser Console):
```javascript
console.log(JSON.parse(localStorage.getItem('userDatabase')));
```

### Check Login Status (Browser Console):
```javascript
console.log('Logged in:', sessionStorage.getItem('isLoggedIn'));
console.log('User:', sessionStorage.getItem('userName'));
```

### Clear All Data (Browser Console):
```javascript
localStorage.clear();
sessionStorage.clear();
location.reload();
```

---

**🎯 Bottom Line**: Just update Google Cloud Console URIs, start a local server, and Google OAuth will work! 🎉
