# Please start the batch file not the .py file

import pytest
from echoClientUDP import *

def fancy_decorator(func):
    def wrapper(sid):
        print("NEW TEST")
        func(sid)
        print("\n")
    return wrapper

def reset_decorator(func):
    def wrapper(sid):
        func(sid)
        msg = {"function": "reset", "SID": sid}
        echo_client(json.dumps(msg))
    return wrapper

@fancy_decorator
@reset_decorator
def test_json1(sid):
    msg = {"name": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "NameError(function not found)"

@fancy_decorator
@reset_decorator
def test_json2(sid):
    msg = {"": ""}
    assert echo_client(json.dumps(msg)) == "NameError(function not found)"

@fancy_decorator
@reset_decorator
def test_register1(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Name 'localhost' got 127.0.0.1 as value."

@fancy_decorator
@reset_decorator
def test_register2(sid):
    msg = {"function": "register", "namee": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Name, Value or SID is missing!"

@fancy_decorator
@reset_decorator
def test_unregister1(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg["function"] = "unregister"
    assert echo_client(json.dumps(msg)) == "Deleted: localhost - 127.0.0.1"

@fancy_decorator
@reset_decorator
def test_unregister2(sid):
    msg = {"function": "unregister", "name": "localhost", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Key 'localhost' not found!"

@fancy_decorator
@reset_decorator
def test_query1(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "ip", "value": "192.1.2.83", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "query", "SID": sid}
    assert echo_client(json.dumps(msg)) == {'localhost': '127.0.0.1', 'ip': '192.1.2.83'}

@fancy_decorator
@reset_decorator
def test_query2(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "ip", "value": "192.1.2.83", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "query", "SID": "1235"}
    assert echo_client(json.dumps(msg)) == "KeyError(SID does not exist)!"

@fancy_decorator
@reset_decorator
def test_reset1(sid):
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "KeyError(SID does not exist)!"

@fancy_decorator
@reset_decorator
def test_reset2(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"

@fancy_decorator
@reset_decorator
def test_reset3(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg["function"] = "unregister"
    echo_client(json.dumps(msg))
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"

@fancy_decorator
@reset_decorator
def test_reset4(sid):
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"
    
@fancy_decorator
@reset_decorator
def test_exit1(sid):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.2", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "exit", "SID": sid}
    assert echo_client(json.dumps(msg)) == "All clients connected to this server"
    
    
if __name__ == '__main__':
    test_query1(sid="1234")
    test_reset4(sid = "1234")
    test_reset2(sid="1234")
    test_exit1(sid="1234")
    
    test_json1(sid="1234")
    test_json1(sid="1234")
    test_register1(sid="1234")
    test_register2(sid="1234")
    test_unregister1(sid="1234")
    test_unregister2(sid="1234")
    
    test_query2(sid="1234")
    test_reset1(sid="1240")
   
    test_reset3(sid="1234")
    
