"""
WSGI config for groceryorgan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import VercelWSGIHandler  # Make sure this file is at the root

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groceryorgan.settings')

application = get_wsgi_application()

# Wrap the Django WSGI app with our adapter.
# Expose the callable under both 'app' and 'handler' to satisfy Vercel.
app = VercelWSGIHandler(application)
handler = app
