import socketserver
from http.server import SimpleHTTPRequestHandler

response = input("what should I say?")

class MyHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle browser preflight CORS requests
        self.send_response(200, "OK")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()

    def end_headers(self):
        # Automatically inject the CORS header for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # 1. Send response code first
        self.send_response(200)
        
        # 2. Set content type and finish headers 
        # (end_headers will call our overridden end_headers() to add CORS)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        # 3. Write response body
        self.wfile.write(str(self.headers).encode('utf-8'))
        self.wfile.write((f"\n{response}").encode("utf-8"))
    def do_POST(self):
        # 1. Get the content length to know how many bytes to read
        content_length = int(self.headers.get('Content-Length', 0))
        
        # 2. Read the request body bytes from rfile
        request_body = self.rfile.read(content_length)
        print (request_body)
        
        # 3. Send response status and headers
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        # 4. Echo the request body back to the client
        self.wfile.write("echoing".encode())
        self.wfile.write(request_body)
if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()