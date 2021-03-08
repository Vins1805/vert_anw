0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
import socket

host = '127.0.0.1'
port = 11111
dataSize = 1024
backlog = 5 

def echo_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Starting up echo server on %s:%s" % (host, port))
    sock.bind((host, port))
    sock.listen(backlog) 
    while True: 
        print("Waiting to receive message")
        client, address = sock.accept() 
        data = client.recv(dataSize) 
        if data:
            print("receive data: %r" % data)
            client.send(data)
            print("sent back to %s:%s" % address)
        client.close() 
   
if __name__ == '__main__':
    echo_server()
