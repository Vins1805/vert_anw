0<0# : ^
''' 
@echo off
python "%~f0" %*
pause
exit /b 0
'''
#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter 1
import socket

host = '127.0.0.1'
dataSize = 32

sockList =[socket.socket(socket.AF_INET, socket.SOCK_STREAM),
           socket.socket(socket.AF_INET, socket.SOCK_STREAM),
           socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          ]

def writeTexts(sock, value, cnt=17):
    text= ""
    for i in range(0,cnt):
        text+= value
    print("Sending %s" % text)
    sendMSG(sock, text)
    return len(text)

def readTexts(sock, amount):
    received = 0
    while received < amount:
        data = receiveMSG(sock)
        received += len(data)
        print("Received: %r" % data)

def echo_client(port):
    letters= "abcdefghi"
    datasz= 0
    try:
        for s in sockList:
            s.connect((host, port))
            print("Open connection to %s:%s" % (host, port))
        no= 0
        for s in sockList:
            datasz= writeTexts(s, letters[no])
            no += 1
        for s in sockList:
            readTexts(s, datasz)
    except Exception as e:
        print("Socket error: %s" %str(e))
    finally:
        for s in sockList:
            print("Close connection to %s:%s" % (host, port))
            s.close()
    
def sendMSG(sock, data):
    sock.send(data.encode())
    
def receiveMSG(sock) -> str:
    #data, address = sock.recvfrom(dataSize)
    data= sock.recv(dataSize)
    return data.decode()
    
if __name__ == '__main__':
    echo_client(11111)
