import socketserver
import threading
import socket
import time
class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        self.request.send(data)
        return

address = ('localhost', 8080)
server = socketserver.TCPServer(address, RequestHandler)
ip, port = server.server_address
print (ip, port)

t = threading.Thread(target=server.serve_forever)
t.daemon = True
t.start()
t.join()


