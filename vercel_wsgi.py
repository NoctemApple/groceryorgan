from wsgiref.simple_server import make_server
from django.core.wsgi import get_wsgi_application

def VercelWSGIHandler(application):
    def handler(event, context):
        return application(event, context)
    return handler
