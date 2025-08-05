# AI Onboarding System - Vercel Deployment

This Flask application is ready for deployment on Vercel.

## Project Structure

- `app.py` - Main Flask application
- `index.py` - WSGI entry point for Vercel
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `config.py` - Application configuration
- `models.py` - Data models and AI integration
- `file_manager.py` - File management system
- `templates/` - HTML templates
- `documents/` - Uploaded documents storage

## Deployment Steps

### 1. Prerequisites
- Git repository (GitHub, GitLab, or Bitbucket)
- Vercel account

### 2. Environment Variables
Set these environment variables in Vercel dashboard:

```
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_DEBUG=False
```

### 3. Deploy to Vercel

1. **Connect Repository:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your Git repository

2. **Configure Project:**
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

3. **Set Environment Variables:**
   - Go to Project Settings → Environment Variables
   - Add the variables listed above

4. **Deploy:**
   - Click "Deploy"
   - Vercel will automatically detect the Python app and deploy it

### 4. Post-Deployment

The application will be available at your Vercel URL (e.g., `your-project.vercel.app`).

**Default Login Accounts:**
- Admin: `admin` / `admin123`
- Minister: `nazir` / `nazir123`
- Analyst: `analitik` / `data123`

## Features

- AI-powered chat assistant using Google Gemini
- Document upload and management
- User authentication and authorization
- File search and indexing
- Responsive web interface
- Admin dashboard

## Important Notes

1. **Database:** Uses SQLite which works in Vercel's serverless environment
2. **File Storage:** Temporary files are stored in `/tmp` directory
3. **Static Files:** All static assets are served by Flask
4. **AI Model:** Uses Google Gemini 2.5 Flash model

## Troubleshooting

- Make sure all environment variables are set correctly
- Check Vercel function logs for any errors
- Ensure the GEMINI_API_KEY is valid and has proper permissions

## Local Development

To run locally:

```bash
pip install -r requirements.txt
python app.py
```

The application will be available at `http://localhost:5000`.
