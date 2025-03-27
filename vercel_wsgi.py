# vercel.wsgi
from http.server import BaseHTTPRequestHandler
from io import BytesIO

def VercelWSGIHandler(application):
    class VercelHandler(BaseHTTPRequestHandler):
        def handle_one_request(self):
            # Build a minimal WSGI environ (you’ll need to adjust this for your needs)
            environ = {
                'REQUEST_METHOD': self.command,
                'PATH_INFO': self.path,
                'SERVER_NAME': self.server.server_address[0],
                'SERVER_PORT': str(self.server.server_address[1]),
                'wsgi.input': self.rfile,
                'wsgi.errors': None,
                'wsgi.version': (1, 0),
                'wsgi.run_once': False,
                'wsgi.url_scheme': 'http',
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
            }

            response_body = BytesIO()

            def start_response(status, response_headers, exc_info=None):
                code = int(status.split()[0])
                self.send_response(code)
                for header in response_headers:
                    self.send_header(*header)
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

        def handle(self):
            # Instead of the default, process only one request per invocation
            self.handle_one_request()

    return VercelHandler
