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
import threading, queue
import os




host = '0.0.0.0'
sport = 53      # own port
dataSize = 1024

q = queue.Queue()




class Datenbank():
    def __init__(self, print_locks = True):
        self.lock = threading.Lock()
        self.data = {}
        self.print_locks = print_locks

    def p(self):
        """ Acquire. """
        self.lock.acquire()
        self.data = get_data()
        if self.print_locks:
            print("lock acquired")
        return self.data

    def v(self, value):
        """ Release. """
        store_data(value)
        self.lock.release()
        if self.print_locks:
            print("lock releases")

db = Datenbank()


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
                data = exit1()
            elif func == "reset_all":
                try:
                    data = reset_all()
                except KeyError:
                    data = "Error in function reset_all"
            else:
                data = "NameError(function not found)"
            
            #Alle Fehler wurden abgedeckt. Data kann nur None sein, wenn es sich um einen Thread handelt. dann soll er die Message aus der queue nehmen
            if data == None:
                data = q.get()                
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



def thread_decorator(func):
    def wrapper(*args):
        x = threading.Thread(target = lambda arg, queue: queue.put(func(*arg)), args = (args, q))
        x.start()
        x.join()
    return wrapper

@thread_decorator
def register(name, value, sid):
    """Gets a KeyError if SID doesn't exist, so a new SID gets created."""
    if not isinstance(name, str):
        return "ValueError(Name isn't a string)"
    if not isinstance(value, str):
        return "ValueError(Value isn't a string)"
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    data = db.p()
    try:
        data[sid][name] = value
    except KeyError:
        print("KeyError")
        data[sid] = {}
        data[sid][name] = value       
    db.v(data)
    return f"Name '{name}' got {value} as value."

@thread_decorator
def unregister(name, sid):
    if not isinstance(name, str):
        return "ValueError(Value isn't a string)"
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    data = db.p()
    try:
        del data[sid][name]
        db.v(data)
        return f"Deleted Client with Name: {name}"
    except KeyError:
        db.v(data)
        return f"Key '{name}' not found!"

@thread_decorator  
def query(sid):
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    data = db.p()
    db.v(data)
    try:
        return data[sid]
    except KeyError:
        return "KeyError(SID does not exist)!"

@thread_decorator
def reset(sid):
    if not isinstance(sid, str):
        return "ValueError(sid isn't a string)"
    data = db.p()
    try:
        del data[sid]
        db.v(data)        
        return "Database got cleared!"
    except KeyError:
        db.v(data)
        return "KeyError(SID does not exist)!"

@thread_decorator
def exit1(*args):
    print("------------------Server shut down---------------------")
    #sys.exit("Sever shut down. In sys.exit()")
    
@thread_decorator 
def reset_all(*args):
    data = db.p()
    data = {}
    db.v(data)
    return "All data got deleted"

        

def get_data():
    try:
        with open("test.pkl", "rb") as pickle_file:
            data = pickle.load(pickle_file)
        return data
    except (OSError, IOError) as e:
        return dict()

def store_data(data):
    with open("test.pkl", "wb") as pickle_file:
        pickle.dump(data, pickle_file)

    

if __name__ == '__main__':
    while True:
        echo_server()