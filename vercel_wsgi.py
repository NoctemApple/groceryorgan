# vercel_wsgi.py
from http.server import BaseHTTPRequestHandler
from io import BytesIO

def VercelWSGIHandler(application):
    class VercelHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Build a basic WSGI environment from the GET request
            environ = {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': self.path,
                'SERVER_NAME': self.server.server_address[0] if self.server.server_address else 'localhost',
                'SERVER_PORT': str(self.server.server_address[1]) if self.server.server_address else '80',
                'wsgi.input': self.rfile,
                'wsgi.errors': self.wfile,
                'wsgi.version': (1, 0),
                'wsgi.run_once': False,
                'wsgi.url_scheme': 'http',
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
            }

            response_body = BytesIO()

            def start_response(status, headers, exc_info=None):
                # Parse the status code from status string ("200 OK" -> 200)
                code = int(status.split()[0])
                self.send_response(code)
                for header_name, header_value in headers:
                    self.send_header(header_name, header_value)
                self.end_headers()
                return response_body.write

            result = application(environ, start_response)
            try:
                for data in result:
                    response_body.write(data)
            finally:
                if hasattr(result, 'close'):
                    result.close()

            self.wfile.write(response_body.getvalue())

        def do_POST(self):
            # Similar implementation for POST if needed.
            self.do_GET()  # For simplicity, route POST to the same handler

    return VercelHandler
