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
import sys
import pickle
import os

host = '0.0.0.0'
sport = 53      # own port
dataSize = 1024

client = {    
}


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
                try:
                    data = register(data["name"], data["value"], data["SID"])
                except KeyError:
                    data = "Name, Value or SID is missing!"
            elif func == "unregister":
                try:
                    data = unregister(data["name"], data["SID"])
                except KeyError:
                    data = "Name, Value or SID is missing!"
            elif func == "query":
                try:
                    data = query(data["SID"])
                except KeyError:
                    data = "Name, Value or SID is missing!"
            elif func == "reset":
                try:
                    data = reset(data["SID"])
                except KeyError:
                    data = "Name, Value or SID is missing!"
            elif func == "exit":
                try:
                    data = exit(data["SID"])
                except KeyError:
                    data = "Name, Value or SID is missing!"
            else:
                data = "NameError(function not found)"
            
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
    """Gets a KeyError if SID doesn't exist, so a new SID gets created."""
    if not isinstance(name, str):
        return "ValueError(Name isn't a string)"
    if not isinstance(value, str):
        return "ValueError(Value isn't a string)"
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    try:
        client[sid][name] = value
        store_data(client)
    except KeyError:
        print("KeyError")
        client[sid] = {}
        client[sid][name] = value
        store_data(client)
    return f"Name '{name}' got {value} as value."

def unregister(name, sid):
    if not isinstance(name, str):
        return "ValueError(Value isn't a string)"
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    try:
        data = get_data()
        print(data)
        
        del data[sid][name]
        print(data)
        store_data(data)
        return f"Deleted Client with Name: {name}"
    except KeyError:
        return f"Key '{name}' not found!"

    
def query(sid):
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    try:
        data = get_data()
        print(data)
        return data[sid]
    except KeyError:
        return "KeyError(SID does not exist)!"

def reset(sid):
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    try:
        data = get_data()
        print(data)
        del data[sid]
        print(data)
        store_data(data)        
        return "Database got cleared!"
    except KeyError:
        return "KeyError(SID does not exist)!"

def exit(*args):
    return "Server shut down"
    sys.exit()
    
        

def get_data():
    with open("test.pkl", "rb") as pickle_file:
        data = pickle.load(pickle_file)
    return data

def store_data(data):
    with open("test.pkl", "wb") as pickle_file:
        pickle.dump(data, pickle_file)

    

if __name__ == '__main__':
    echo_server()
    echo_server()
    

    
