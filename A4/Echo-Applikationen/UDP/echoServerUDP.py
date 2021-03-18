0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
import socket
import json

host = '0.0.0.0'
sport = 53      # own port
dataSize = 1024
database = dict()


def echo_server():
    receiveSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiveSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiveSock.bind((host,sport))
    print("Starting up echo server on %s port %s" % (host, sport))

    while True: 
        print("Waiting to receive message")
        data, address = receiveSock.recvfrom(dataSize)
        
        if data:
            print("receive data: %s from %s" % (data,address))
            data = json.loads(data)
            
            try:
                func = data.pop("function")
            except KeyError:
                func = None
            
            if func == "register":
                pass
            else:
                pass
            
            print("sent %s bytes back to %s" % (data,address))
            sendMSG(data,address)

def to_json_decorator(func):
    def wrapper(data,address):
        func(json.dumps({"message": data}), address)
    return wrapper

@to_json_decorator
def sendMSG(data,address):
    sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sendSock.sendto(data.encode(),address)
    sendSock.close()

def register(name, value, sid):
    pass

def unregister(name, sid):
    pass

def query(sid):
    pass

def reset(sid):
    pass



if __name__ == '__main__':
    echo_server()
