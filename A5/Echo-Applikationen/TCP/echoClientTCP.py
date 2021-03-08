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
port = 11111
dataSize = 32

def echo_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to %s port %s" % (host, port))
        sock.connect((host, port))
        sallust = """Igitur initio reges – nam in terris nomen imperi
                  id primum fuit – divorsi pars ingenium, alii
                  corpus exercebant: Etiam tum vita hominum sine
                  cupiditate agitabatur; sua cuique satis placebant.
                  """
        print("Sending %s" % sallust)
        sendMSG(sock, sallust)

        amount_received = 0
        while amount_received < len(sallust):
            data = receiveMSG(sock)
            amount_received += len(data)
            print("Received: %r" % data)
    except Exception as e:
        print("Socket error: %s" %str(e))
    finally:
        print("Closing connection to the server")
        sock.close()
        
def sendMSG(sock, data):
    sock.send(data.encode())
    
def receiveMSG(sock) -> str:
    #data, address = sock.recvfrom(dataSize)
    data= sock.recv(dataSize)
    return data.decode()
    
if __name__ == '__main__':
    echo_client()
