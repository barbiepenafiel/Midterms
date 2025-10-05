# 🔄 OAuth Authentication Flow Diagram

## Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER STARTS LOGIN                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LANDING PAGE (landing.html)                                    │
│  • User clicks "Login" button                                   │
│  • Auth modal opens                                             │
│  • User clicks "Sign in with Google"                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ loginWithGoogle() called
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  REDIRECT TO GOOGLE                                             │
│  URL: https://accounts.google.com/o/oauth2/v2/auth              │
│  Parameters:                                                    │
│    • client_id: 206414229595-...googleusercontent.com           │
│    • redirect_uri: http://localhost:8000/auth-callback.html     │
│    • response_type: token id_token                              │
│    • scope: email profile openid                                │
│    • nonce: random-string-for-security                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  GOOGLE ACCOUNT SELECTION                                       │
│  • User sees their Google accounts                              │
│  • User selects account to sign in with                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  GOOGLE PERMISSIONS SCREEN                                      │
│  • "Oursfolio Portfolio wants to access:"                       │
│    - Your email address                                         │
│    - Your basic profile info                                    │
│  • User clicks "Allow"                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  REDIRECT TO CALLBACK PAGE                                      │
│  URL: http://localhost:8000/auth-callback.html#access_token=... │
│  Hash Fragment Contains:                                        │
│    • access_token: ya29.a0...                                   │
│    • id_token: eyJhbGciOiJSUzI1NiIsImtpZCI6...                  │
│    • expires_in: 3599                                           │
│    • token_type: Bearer                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  AUTH CALLBACK PAGE (auth-callback.html)                        │
│  Processing:                                                    │
│  1. Extract tokens from URL hash                                │
│  2. Decode JWT id_token                                         │
│  3. Parse user email from token payload                         │
│  4. Store in sessionStorage:                                    │
│     - google_auth_email                                         │
│     - google_auth_name                                          │
│     - google_auth_picture                                       │
│     - google_auth_complete: 'true'                              │
│  5. Redirect to landing.html                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  BACK TO LANDING PAGE (landing.html)                            │
│  On page load:                                                  │
│  1. handleOAuthCallback() runs                                  │
│  2. Checks for google_auth_complete flag                        │
│  3. Retrieves email from sessionStorage                         │
│  4. Pre-fills email in auth modal                               │
│  5. Opens modal automatically                                   │
│  6. Calls proceedTo2FA()                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2FA SETUP (Step 2 of Auth Modal)                               │
│  1. Generate random secret key (Base32)                         │
│  2. Create otpauth:// URI                                       │
│  3. Generate QR code with pink theme                            │
│  4. Display secret key for manual entry                         │
│  5. Wait for user to scan with Google Authenticator            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  USER SCANS QR CODE                                             │
│  • Opens Google Authenticator app                               │
│  • Scans QR code                                                │
│  • Gets 6-digit code (refreshes every 30 seconds)               │
│  • Enters code in modal                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CODE VERIFICATION                                              │
│  verify2FA() function:                                          │
│  • Validates 6-digit format                                     │
│  • (Demo: accepts any 6 digits)                                 │
│  • (Production: verify with TOTP algorithm)                     │
│  • Stores login state in sessionStorage                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  SUCCESS! (Step 3 of Auth Modal)                                │
│  • Shows success animation                                      │
│  • Displays user email                                          │
│  • User is now logged in                                        │
│  • Can access dashboard/protected content                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## JWT Token Structure

```
ID Token (JWT): eyJhbGciOiJSUzI1NiIs...
                │
                ├── HEADER
                │   {
                │     "alg": "RS256",
                │     "kid": "abc123",
                │     "typ": "JWT"
                │   }
                │
                ├── PAYLOAD
                │   {
                │     "iss": "https://accounts.google.com",
                │     "azp": "206414229595-...apps.googleusercontent.com",
                │     "aud": "206414229595-...apps.googleusercontent.com",
                │     "sub": "1234567890",
                │     "email": "user@gmail.com",
                │     "email_verified": true,
                │     "name": "User Name",
                │     "picture": "https://lh3.googleusercontent.com/...",
                │     "given_name": "User",
                │     "family_name": "Name",
                │     "iat": 1696531200,
                │     "exp": 1696534800,
                │     "nonce": "random-nonce"
                │   }
                │
                └── SIGNATURE
                    (Cryptographic signature to verify token authenticity)
```

---

## Session Storage Data Flow

```
After Google OAuth Success:
┌──────────────────────────────────────────┐
│ sessionStorage                           │
├──────────────────────────────────────────┤
│ google_auth_email: "user@gmail.com"      │
│ google_auth_name: "User Name"            │
│ google_auth_picture: "https://..."       │
│ google_auth_token: "ya29.a0..."          │
│ google_auth_complete: "true"             │
└──────────────────────────────────────────┘
         │
         │ On landing.html page load
         ▼
┌──────────────────────────────────────────┐
│ handleOAuthCallback()                    │
│ • Reads sessionStorage                   │
│ • Extracts email                         │
│ • Opens auth modal                       │
│ • Pre-fills email field                  │
│ • Triggers 2FA setup                     │
└──────────────────────────────────────────┘

After 2FA Verification:
┌──────────────────────────────────────────┐
│ sessionStorage                           │
├──────────────────────────────────────────┤
│ isLoggedIn: "true"                       │
│ userEmail: "user@gmail.com"              │
│ (Previous Google auth data...)           │
└──────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────┐
│  User clicks "Sign in with Google"      │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Possible Errors:                       │
├─────────────────────────────────────────┤
│  ❌ redirect_uri_mismatch               │
│     → Update authorized URIs in Console │
│                                         │
│  ❌ origin_mismatch                     │
│     → Update JavaScript origins         │
│                                         │
│  ❌ access_denied                       │
│     → User clicked "Cancel"             │
│     → Redirect back to landing          │
│                                         │
│  ❌ invalid_client                      │
│     → Check client ID is correct        │
│                                         │
│  ❌ Token parsing failed                │
│     → JWT format error                  │
│     → Show error, redirect to landing   │
└─────────────────────────────────────────┘
```

---

## Security Checkpoints

```
✅ Client-Side Security:
├── Nonce validation (CSRF protection)
├── Token expiration check
├── HTTPS enforcement (production)
├── sessionStorage (tab-specific)
└── No client_secret in frontend

⚠️ Add for Production:
├── Backend API for token validation
├── Server-side session management
├── Database for user storage
├── Rate limiting on auth endpoints
└── Token refresh mechanism
```

---

## File Responsibilities

```
landing.html
├── Login UI (modal)
├── Google Sign-In button
├── OAuth redirect initiation
├── Callback handling
├── 2FA setup UI
├── Code verification
└── Success screen

auth-callback.html
├── Receive OAuth response
├── Parse URL hash
├── Decode JWT token
├── Extract user info
├── Store in sessionStorage
└── Redirect to landing

client_secret_*.json
├── Client ID (public)
├── Client Secret (keep secure)
├── Project ID
├── Authorized URIs
└── OAuth endpoints
```

---

## Timeline

```
0 ms    │ User clicks "Sign in with Google"
        │
100 ms  │ Redirect to Google OAuth
        │
~2 sec  │ Google shows account selection
        │
~3 sec  │ User selects account
        │
~4 sec  │ Google shows permissions
        │
~5 sec  │ User clicks "Allow"
        │
~5.5 s  │ Redirect to auth-callback.html
        │
~5.7 s  │ Token parsed, stored
        │
~6 sec  │ Redirect to landing.html
        │
~6.2 s  │ Modal opens with 2FA
        │
~6.5 s  │ QR code generated
        │
[User]  │ Scans QR with authenticator
        │
[User]  │ Enters 6-digit code
        │
~1 sec  │ Verification (demo: instant)
        │
~1.5 s  │ Success screen shown!
```

---

**Total Time**: ~6-7 seconds + user interaction time
