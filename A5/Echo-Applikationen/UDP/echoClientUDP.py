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

host = '127.0.0.1'
sport = 53
dataSize = 1024
msg = dict()


def echo_client(message):
    sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        print("Sending %s to %s:%s" % (message,host,sport))
        sendMSG(sendSock, message)
        
        data = json.loads(receiveMSG(sendSock));
        if data: 
            print("Received: %s" % data)
    except Exception as err:
        print("Socket error: %s" %str(err))
    finally:
        print("Closing connection to the server")
        sendSock.close()
        return data["message"]
        
def sendMSG(sock, data):
    sock.sendto(data.encode(),(host, sport))

def receiveMSG(sock) -> str:
    data, address = sock.recvfrom(dataSize)
    return data.decode()


if __name__ == '__main__':
    msg["function"] = "query"
    msg["name"] = "ip2"
    msg["value"] = "127.0.0.1"
    msg["SID"] = "1234"

    echo_client(json.dumps(msg))
    
