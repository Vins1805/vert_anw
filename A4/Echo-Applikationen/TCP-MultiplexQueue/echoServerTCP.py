0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
import socket, select, threading, queue

host = '127.0.0.1'
port = 11111
dataSize = 1024
backlog = 5
MsgQueues = {}
EOI = object() # leeres Objekt

class handleConnect(threading.Thread):
    def __init__(self,socket,q):
        threading.Thread.__init__(self)
        self.client = socket
        self.queue = q
        self.start()
    def run(self):
        live= True
        while live:
            data= self.queue.get()
            if data is EOI:
                del MsgQueues[self.client]
                live= False
            else:
                msg = data.decode()
                print("receive data: %r" % msg)
                self.client.send(data)
                print("sent back to %s:%s" % self.client.getpeername())
        print("Thread %s terminates" % self.getName())           

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
                print("Open connection to %s:%s" % address)
                client.setblocking(False)
                inputs.append(client)
                MsgQueues[client] = queue.Queue()
                thread= handleConnect(client,MsgQueues[client])
            else:
                try:
                    data = s.recv(dataSize)
                    if data:
                        MsgQueues[s].put(data)
                    else:
                        print("Close connection to %s:%s" % s.getpeername())
                        s.close()
                        inputs.remove(s)
                        MsgQueues[s].put(EOI)
                except socket.error as e:
                        inputs.remove(s)
                        live= False
        for s in exceptions:
            print("Exception on connection to %s:%s" % s.getpeername())
            inputs.remove(s)
            MsgQueues[s].put(EOI)
    server.close()
                    
if __name__ == '__main__':
    echo_server()
