

import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print ("request made")
        self.wfile.write("hello world!!".encode())
        self.send_response(200)

httpd = socketserver.TCPServer(("", 8080), MyHandler)
httpd.serve_forever()
