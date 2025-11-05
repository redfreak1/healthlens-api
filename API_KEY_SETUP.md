# API Key Setup Instructions

## 🔑 Generating a New Gemini API Key

Your current API key has been reported as leaked and needs to be replaced. Follow these steps:

### Step 1: Generate New API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key"
4. Choose "Create API key in new project" or select existing project
5. Copy the new API key

### Step 2: Update Environment Variables

1. Open the `.env` file in your project root
2. Replace the `GEMINI_API_KEY` value with your new key:
   ```
   GEMINI_API_KEY=your-new-api-key-here
   ```

### Step 3: For GCP Deployment

For production deployment on GCP, use environment variables instead of .env files:

1. **Cloud Run**: Set environment variables in the Cloud Run service configuration
2. **App Engine**: Use app.yaml environment variables
3. **Compute Engine**: Set environment variables in the VM

Example for Cloud Run:
```bash
gcloud run deploy healthlens-api \
  --set-env-vars GEMINI_API_KEY=your-new-api-key-here
```

### Step 4: Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for production**
3. **Restrict API key usage** in Google Cloud Console:
   - Set application restrictions
   - Set API restrictions to only Generative AI APIs
4. **Monitor API key usage** in Google Cloud Console
5. **Rotate keys regularly**

## 🛡️ Security Checklist

- [ ] New API key generated
- [ ] Old API key deleted/disabled
- [ ] .env file updated with new key
- [ ] .gitignore includes .env file
- [ ] Production environment variables updated
- [ ] API key restrictions configured
- [ ] Usage monitoring enabled

## 🚨 If API Key Leaks Again

1. Immediately disable the leaked key in Google Cloud Console
2. Generate a new key
3. Update all environments
4. Review commit history to ensure no keys are in code
5. Consider using secret management services (Google Secret Manager, etc.)

## 📞 Support

If you continue to have issues:
1. Check the server logs for specific error messages
2. Verify API key permissions in Google Cloud Console
3. Test with a simple curl request to verify the key works
4. Contact support if needed