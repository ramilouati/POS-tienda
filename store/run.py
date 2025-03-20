import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

# Start the WSGI application with Waitress
application = get_wsgi_application()
print("Starting Waitress Server on http://127.0.0.1:8000")
serve(application, host='127.0.0.1', port=8000)
