# Please start the batch file not the .py file

import pytest
from echoClientUDP import *

# wird später als decorator vor jedem test ausgeführt
def reset_decorator(func):
    def wrapper():
        msg = {"function": "reset", "SID": "1234"}
        echo_client(json.dumps(msg))
        func()
    return wrapper

tests = [
    ({"function": "register", "name": "localhost", "value": "127.0.0.1", "SID": "1234"}, "Created localhost with 127.0.0.1 as value."),
    ({"function": "unregister", "name": "localhost", "SID": "1234"}, "Delected localhost."),
    ({"function": "query", "SID": "1234"}, "KeyError"),
    ({"function": "reset", "SID": "1234"}, "KeyError"),
    ({"function": "register", "namee": "localhost", "value": "127.0.0.1", "SID": "1234"}, "ValueError"),
    ({"function": "register", "name": "localhost", "valuee": "127.0.0.1", "SID": "1234"}, "ValueError"),
    ({"function": "register", "name": "localhost", "SID": "1234"}, "ValueError"),
    ({"function": "unregister", "name": "localhost"}, "ValueError"),
    ({"name": "localhost", "value": "127.0.0.1", "SID": "1234"}, "KeyError"),
    ({"": ""}, "KeyError"),
    ]


@pytest.mark.parametrize("msg,result", tests)
def test_json(msg, result):
    assert echo_client(json.dumps(msg)) == result
    msg["function"] = "reset"
    echo_client(json.dumps(msg))
