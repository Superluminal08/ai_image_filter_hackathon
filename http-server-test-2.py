import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.wfile.write(str(self.headers).encode())
        self.wfile.write("hello world!".encode())
        self.send_response(200)
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
if __name__ == '__main__':
    httpd = socketserver.TCPServer(("", 8080), MyHandler)
    httpd.serve_forever()
