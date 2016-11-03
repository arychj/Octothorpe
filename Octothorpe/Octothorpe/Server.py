import http.server
import threading

from socketserver import ThreadingMixIn

class Server:
    @classmethod
    def Start(cls):
        httpd = cls._threading_server(("0.0.0.0", 1664), cls._server_request_handler)

        t = threading.Thread(target=httpd.serve_forever)
        t.start()

    @classmethod
    def Stop(cls):
        pass

    class _threading_server(ThreadingMixIn, http.server.HTTPServer):
        pass

    class _server_request_handler(http.server.BaseHTTPRequestHandler):
        def do_GET(s):
            s.send_response(200)
            s.send_header("Content-type", "application/json")
            s.end_headers()
            s.wfile.write("blah".encode("utf-8"))
            return