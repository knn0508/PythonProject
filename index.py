from app import app

# This is the entry point for Vercel
def handler(event, context):
    return app

# Export the app for Vercel
application = app

# For local development
if __name__ == "__main__":
    app.run(debug=False)
