# Please start the batch file not the .py file

import pytest
from echoClientUDP import *

def reset_decorator(func):
    def wrapper():
        msg = {"function": "reset", "SID": "1234"}
        echo_client(json.dumps(msg))
        func()
    return wrapper

tests = [
    ({"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": "1234"}, "Name 'localhost' got 127.0.0.1 as value."),
    ({"function": "unregister", "name": "localhost", "SID": "1234"}, "Deleted: localhost - 127.0.0.1"),
    ({"function": "query", "SID": "1234"}, {}),
    ({"function": "reset", "SID": "1234"}, "Database got cleared!"),
    ({"function": "register", "namee": "localhost", "value": "127.0.0.1", "SID": "1234"}, "Name, Value or SID is missing!"),
    ({"function": "register", "name": "localhost", "valuee": "127.0.0.1", "SID": "1234"}, "Name, Value or SID is missing!"),
    ({"function": "register", "name": "localhost", "SID": "1234"}, "Name, Value or SID is missing!"),
    ({"function": "unregister", "name": "localhost"}, "Name, Value or SID is missing!"),
    ({"name": "localhost", "value": "127.0.0.1", "SID": "1234"}, "NameError(function not found)"),
    ({"": ""}, "NameError(function not found)"),
    ]

@reset_decorator
def test_unregister1(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg["function"] = "unregister"
    assert echo_client(json.dumps(msg)) == "Deleted Client with Name: localhost"

@reset_decorator
def test_unregister2(sid="1234"):
    msg = {"function": "unregister", "name": "localhost", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Key 'localhost' not found!"



@pytest.mark.parametrize("msg,result", tests)
def test_json(msg, result):
    assert echo_client(json.dumps(msg)) == result



@reset_decorator
def test_json1(sid="1234"):
    msg = {"name": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "NameError(function not found)"

@reset_decorator
def test_json2(sid="1234"):
    msg = {"": ""}
    assert echo_client(json.dumps(msg)) == "NameError(function not found)"

@reset_decorator
def test_register1(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Name 'localhost' got 127.0.0.1 as value."

@reset_decorator
def test_register2(sid="1234"):
    msg = {"function": "register", "namee": "localhost", "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Name, Value or SID is missing!"

def test_register3(sid="1234"):
    msg = {"function": "register", "name": True, "value": "127.0.0.1", "SID": sid}
    assert echo_client(json.dumps(msg)) == "ValueError(Name isn't a string)"

@reset_decorator
def test_register4(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": "13"}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": "12124"}
    echo_client(json.dumps(msg))





@reset_decorator
def test_query1(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "ip", "value": "192.1.2.83", "SID": "123456"}
    echo_client(json.dumps(msg))
    msg = {"function": "query", "SID": sid}
    assert echo_client(json.dumps(msg)) == {'localhost': '127.0.0.1'}

@reset_decorator
def test_query2(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "ip", "value": "192.1.2.83", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "query", "SID": "1235"}
    assert echo_client(json.dumps(msg)) == "KeyError(SID does not exist)!"
    
def test_query3(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.2", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "ip", "value": "192.1.2.83", "SID": "123456"}
    echo_client(json.dumps(msg))
    msg = {"function": "query", "SID": "1234"}
    assert echo_client(json.dumps(msg)) == {'localhost': '127.0.0.1', 'localhost': '127.0.0.2'}


@reset_decorator
def test_reset1(sid="1240"):
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "KeyError(SID does not exist)!"

@reset_decorator
def test_reset2(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"

@reset_decorator
def test_reset3(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg["function"] = "unregister"
    echo_client(json.dumps(msg))
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"


@reset_decorator
def test_reset4(sid="1234"):
    msg = {"function": "reset", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Database got cleared!"
    

@reset_decorator
def test_exit1(sid="1234"):
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "register", "name": "localhost", "value": "127.0.0.2", "SID": sid}
    echo_client(json.dumps(msg))
    msg = {"function": "exit", "SID": sid}
    assert echo_client(json.dumps(msg)) == "Server shut down"
