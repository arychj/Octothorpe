import http.server
import json, time

from socketserver import ThreadingMixIn

from ..Injector import Injector
from ..Instruction import Instruction
from ..InstructionQueue import InstructionQueue

class HttpInjector(Injector):
    def Start(self):

        httpd = self._threading_server(("0.0.0.0", 1664), self._server_request_handler)
        httpd.serve_forever()
        print("hi")
#
#        t = threading.Thread(target=httpd.serve_forever)
#        t.start()

    def Stop(self):
        pass

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
            instruction = Instruction.Parse(post_body)
            InstructionQueue.Enqueue(instruction)

            while(instruction.IsComplete == False):
                time.sleep(0.1)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(instruction.Result).encode("utf-8"))
