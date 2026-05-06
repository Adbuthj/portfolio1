from portfolio_project.wsgi import application

# This is a bridge for Render's default 'gunicorn app:app' command
app = application
