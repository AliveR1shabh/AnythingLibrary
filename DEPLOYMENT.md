# Vercel Deployment Guide

## 🚀 Deploy AnythingLibrary to Vercel

### Prerequisites
- GitHub repository: https://github.com/AliveR1shabh/AnythingLibrary
- Vercel account (free)
- API keys for AI services

### Step 1: Deploy to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Click "New Project"**
3. **Import GitHub Repository**: 
   - Search for "AnythingLibrary"
   - Click "Import"
4. **Configure Project**:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: `npm run vercel-build` (auto-detected)
   - Output Directory: `frontend/build` (auto-detected)
   - Install Command: `npm install` (auto-detected)
5. **Environment Variables** (add these):
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `GROQ_API_KEY`: Your GROQ API key  
   - `CEREBRAS_API_KEY`: Your Cerebras API key
6. **Click "Deploy"**

### Step 2: Verify Deployment

Once deployed, your app will be available at:
- Frontend: `https://your-app-name.vercel.app`
- API: `https://your-app-name.vercel.app/api`

### Step 3: Test the Application

1. Open your deployed URL
2. Test login (any username/password works)
3. Test AI comparison with different providers
4. Test "Explain Like I'm 10" toggle

### 🔧 Configuration Files

The following files were added for Vercel compatibility:

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless API function
- `api/requirements.txt` - Python dependencies
- Updated `frontend/package.json` - Build scripts

### 🐛 Troubleshooting

**Build Errors:**
- Check that all environment variables are set
- Verify API keys are valid
- Check Vercel build logs

**API Errors:**
- Ensure environment variables are configured in Vercel dashboard
- Check API key permissions
- Verify rate limits on AI services

**Frontend Issues:**
- Clear browser cache
- Check console for errors
- Verify API endpoint is accessible

### 📝 Environment Variables Setup

In Vercel Dashboard → Settings → Environment Variables:

```
GOOGLE_API_KEY=your_google_gemini_api_key
GROQ_API_KEY=your_groq_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
```

### 🎯 Features Available

✅ Multi-AI comparison (Google, GROQ, Cerebras)
✅ "Explain Like I'm 10" toggle
✅ Responsive design
✅ Login system
✅ Professional UI/UX
✅ Fast API responses

### 🌟 Your Live App

After deployment, share your Vercel URL with others to showcase your AI comparison platform!

**Deployment typically takes 2-3 minutes.**
