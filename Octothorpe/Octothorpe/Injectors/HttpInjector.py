import http.server
import json, time

from socketserver import ThreadingMixIn

from ..Injector import Injector
from ..Instruction import Instruction

class HttpInjector(Injector):
    def Start(self):
        self._httpd = self._threading_server(("0.0.0.0", 1664), self._server_request_handler)
        self._httpd.serve_forever()

    def Stop(self):
        self._httpd.shutdown()

    class _threading_server(ThreadingMixIn, http.server.HTTPServer):
        pass

    class _server_request_handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write("blah".encode("utf-8"))

        def do_POST(self):
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len).decode("utf-8")

            result = self.Inject(post_body)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
