0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
import socket, select, threading

host = '127.0.0.1'
port = 11111
dataSize = 1024
backlog = 5

def handleConnect(data, sock):
    msg = data.decode()
    print("Receive data: %r" % msg)
    sock.send(data)
    print("Sent back to %s:%s" % sock.getpeername()) 

def echo_server():
    live = True
    print("Starting up echo server on %s:%s" % (host, port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind((host, port))
    server.listen(5)
    inputs = [server]
    outputs = []
    exceptions= []
    while live:
        toRead, toWrite, exceptions = select.select(inputs, outputs, exceptions)
        for s in toRead:
            if s is server:
                client, address = server.accept()
                client.setblocking(False)
                inputs.append(client)
                print("Open connection to %s:%s" % address)
            else:
                try:
                    data = s.recv(dataSize)
                    if data:
                        handleConnect(data,s)
                    else:
                        print("Close connection to %s:%s" % s.getpeername())
                        s.close()
                        inputs.remove(s)
                except socket.error as e:
                        inputs.remove(s)
                        live= False
        for s in exceptions:
            print("Exception on connection to %s:%s" % s.getpeername())
            inputs.remove(s)
    server.close()
                    
if __name__ == '__main__':
    echo_server()
