# Simple Flask App for Vercel

## Quick Deploy Instructions

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Click "Deploy"

3. **That's it!** Your app will be live at `your-project.vercel.app`

## App Features

- ✅ Home page with interactive UI
- ✅ API endpoints for testing
- ✅ Echo service
- ✅ Simple calculator
- ✅ Health check endpoint

## Files Structure

- `index.py` - Entry point for Vercel
- `simple_app.py` - Main Flask application
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

## Test Your Deployment

After deployment, test these URLs:
- `/` - Main page
- `/health` - Health check
- `/api/test` - API test endpoint
