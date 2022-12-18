from http.server import BaseHTTPRequestHandler
import json
import socketserver
from typing import Callable
def server_Handler(process:Callable):
    """
    the process receives a string message headers and dict of the message body of the request
    and should return a dict
    """
    class Handler(BaseHTTPRequestHandler):
        def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
            super().__init__(request, client_address, server)

        def do_POST(self):
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len).decode("utf8")
            message = json.dumps(process(self.headers, json.loads(post_body)))
            self.wfile.write(bytes(message, "utf8"))

    return Handler
    
# EXample of the handler
# def processor(metaData, requestMessage):
#     print(metaData)
#     print((requestMessage))
#     return {
#         "message":"Assalamualykum"
#     }
# server_address = ('', 6969)
# httpd = HTTPServer(server_address, server_Handler(processor))

# while True:
    
#     httpd.serve_forever()
