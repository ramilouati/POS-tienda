#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from waitress import serve
from django.core.wsgi import get_wsgi_application

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

    if getattr(sys, 'frozen', False):  # Check if running as an executable
        application = get_wsgi_application()
        print("Starting Waitress Server on http://127.0.0.1:8000")
        serve(application, host='127.0.0.1', port=8000)
    else:
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
