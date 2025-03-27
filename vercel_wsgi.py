import sys
from io import BytesIO
from urllib.parse import urlencode

def create_environ(event):
    """
    Convert Vercel event to a WSGI environ dictionary.
    This is a minimal adapter; you might need to expand it based on your needs.
    """
    environ = {}
    # HTTP method (default to GET)
    environ['REQUEST_METHOD'] = event.get('httpMethod', 'GET')
    
    # Path and query string
    path = event.get('path', '/')
    environ['PATH_INFO'] = path
    qs = event.get('queryStringParameters')
    if qs:
        environ['QUERY_STRING'] = urlencode(qs)
    else:
        environ['QUERY_STRING'] = ''

    # Server variables
    environ['SERVER_NAME'] = 'localhost'
    environ['SERVER_PORT'] = '80'

    # Headers
    headers = event.get('headers') or {}
    for header, value in headers.items():
        key = f'HTTP_{header.upper().replace("-", "_")}'
        environ[key] = value

    # WSGI-required keys
    body = event.get('body') or ''
    if event.get('isBase64Encoded'):
        import base64
        body = base64.b64decode(body)
    else:
        body = body.encode('utf-8')
    environ['wsgi.input'] = BytesIO(body)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.url_scheme'] = 'http'
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once'] = False

    return environ

def VercelWSGIHandler(app):
    """
    Wrap a WSGI application so that it can be called from Vercel's serverless runtime.
    Returns a callable that accepts (event, context) and returns a response dict.
    """
    def handler(event, context):
        environ = create_environ(event)
        response_body = []
        response_status = None
        response_headers = {}

        def start_response(status, headers, exc_info=None):
            nonlocal response_status, response_headers
            response_status = status
            response_headers = dict(headers)
            # The WSGI spec requires start_response to return a write callable, but we'll ignore that.
            return response_body.append

        result = app(environ, start_response)
        try:
            for data in result:
                response_body.append(data)
        finally:
            if hasattr(result, 'close'):
                result.close()

        # Build the response expected by Vercel.
        # For example, status is expected to be an integer.
        status_code = int(response_status.split()[0]) if response_status else 500

        return {
            "statusCode": status_code,
            "headers": response_headers,
            "body": b"".join(response_body).decode("utf-8"),
        }

    return handler
