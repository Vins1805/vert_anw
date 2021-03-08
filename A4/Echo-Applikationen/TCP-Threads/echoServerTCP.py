0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
import socket, threading

host = '127.0.0.1'
port = 11111
dataSize = 1024
backlog = 5

class handleConnect(threading.Thread):
    def __init__(self,address,socket):
        threading.Thread.__init__(self)
        self.client = socket
        self.address = address
        self.start()
    def run(self):          # process 1 packet
        data = self.client.recv(dataSize)
        msg = data.decode()
        if data:
            print("receive data: %r" % msg)
            self.client.send(data)
            print("sent back to %s:%s" % self.address)
        self.client.close() 

def echo_server():
    print("Starting up echo server on %s:%s" % (host, port))
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(backlog) 
        client, address = sock.accept() 
        newThread = handleConnect(address, client)

if __name__ == '__main__':
    echo_server()
