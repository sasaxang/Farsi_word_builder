# Security Configuration

## Protected Files (NOT committed to Git)

The following sensitive files are protected by `.gitignore`:

- `streamlit-app/config/firebase-credentials.json` - Firebase service account credentials
- `streamlit-app/.streamlit/secrets.toml` - Local secrets file

## Security Measures

### 1. Firebase Authentication
- ✅ User passwords are securely hashed by Firebase Auth
- ✅ Service account credentials stored in Streamlit Cloud secrets (encrypted)
- ✅ Firebase Security Rules can be configured in Firebase Console

### 2. API Security
- ✅ Firebase Admin SDK uses secure authentication
- ✅ HTTPS enforced by Streamlit Cloud and Firebase
- ✅ No API keys exposed in frontend code

### 3. Data Protection
- ✅ User data stored in Firestore with user-level isolation
- ✅ Only authenticated users can access their own favorites
- ✅ No sensitive data in client-side code

### 4. Git Security
- ✅ All credential files in `.gitignore`
- ✅ No secrets committed to version control
- ✅ Helper script provided to generate deployment secrets

## Recommended Firebase Security Rules

Add these rules in Firebase Console → Firestore Database → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Prevent unauthorized access to any other collections
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

## Additional Security Recommendations

1. **Enable Firebase App Check** (optional, for production):
   - Protects against abuse and automated attacks
   - Configure in Firebase Console → App Check

2. **Monitor Usage**:
   - Check Firebase Console → Usage dashboard
   - Set up alerts for unusual activity

3. **Regular Credential Rotation**:
   - Rotate service account keys periodically
   - Update Streamlit Cloud secrets when rotating

4. **Rate Limiting**:
   - Firebase automatically rate-limits authentication attempts
   - Monitor in Firebase Console → Authentication → Usage

## Deployment Checklist

- [ ] Firebase credentials added to Streamlit Cloud secrets
- [ ] Firestore security rules configured
- [ ] App deployed and tested
- [ ] No secrets in Git history
- [ ] Firebase usage monitoring enabled
