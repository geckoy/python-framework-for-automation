from http.server import BaseHTTPRequestHandler
import json
import socketserver
from typing import Callable
import os
import re
import pathlib

def server_Handler(process:Callable):
    """
    the process receives a string message headers and dict of the message body of the request
    and should return a dict
    """
    def mimetype(filepath):
        # Replace with a more robust MIME type detection library if needed
        mimetype = filepath.split(".")[-1]
        if mimetype == "css":
            return "text/css"
        elif mimetype == "jpg":
            return "image/jpeg"
        elif mimetype == "js":
            return "application/javascript"
        else:
            return "application/octet-stream"  # Generic for unknown types
        
    class Handler(BaseHTTPRequestHandler):
        def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
            super().__init__(request, client_address, server)
        
        def log_request(code='-', size='-'):
            return
        
        def do_POST(self):
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len).decode("utf8")
            message = json.dumps(process(self.headers, json.loads(post_body)))
            self.wfile.write(bytes(message, "utf8"))


        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            
        def do_GET(self):
            # Serve the main HTML page
            MainPath = pathlib.Path().resolve();FullPath = f"{MainPath}{self.path}"
            if re.search("\.html$",self.path, re.IGNORECASE) and os.path.isfile(FullPath):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(FullPath, "r") as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode())

            # Serve assets (replace this logic if you have multiple assets)
            elif re.search("assets", self.path, re.IGNORECASE):
                with open(FullPath, "rb") as f:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype(FullPath))  # Set appropriate MIME type
                    self.end_headers()
                    self.wfile.write(f.read())

            # Handle other requests (optional)
            else:
                self.send_error(404, "Page not found")

    return Handler