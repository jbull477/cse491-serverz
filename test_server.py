#! /usr/bin/env python
import server

def test_error():
    conn = FakeConnection("GET /error HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if 'HTTP/1.0 404 Not Found' not in result:
        assert False
    else:
        pass

def test_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Hello, world.') not in result:
        assert False
    else:
        pass

def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'content page') not in result:
        assert False
    else:
        pass

def test_files():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'file page') not in result:
        assert False
    else:
        pass

def test_images():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'image page') not in result:
        assert False
    else:
        pass

def test_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        '<form action=\'/submit\' method=\'GET\'>\r\n' and \
        'First Name: <input type=\'text\' name=\'firstName\'><br>\r\n' and \
        'Last Name: <input type=\'text\' name=\'lastName\'><br>\r\n' and \
        '<input type=\'submit\' name=\'submit\'>\r\n' and \
        '</form>') not in result:
        assert False
    else:
        pass

def test_submit():
    conn = FakeConnection("GET /submit?firstName=Jason&lastName=Bull&submit=Submit HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Hello Mr. Jason Bull') not in result:
        assert False
    else:
        pass

def test_post_app():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 31\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                          "firstName=Jason&lastName=Bull\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

class FakeConnection(object):
    """
A fake connection class that mimics a real TCP socket for the purpose
of testing socket I/O.
"""
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def settimeout(self, n):
        self.timeout = n

    def close(self):
        self.is_closed = True
