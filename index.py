from app import app

# This is the WSGI entry point for Vercel
def handler(request, context):
    return app(request, context)

# For local development
if __name__ == "__main__":
    app.run(debug=False)
