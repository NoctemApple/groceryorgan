"""
WSGI config for groceryorgan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import VercelWSGIHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groceryorgan.settings')

application = get_wsgi_application()
app = VercelWSGIHandler(application)
handler = app  # Exporting the handler class for Vercel's runtime
