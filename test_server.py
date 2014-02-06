import server

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

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    
    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html' and \
       'Hello, world.') not in result:
        assert False
    else:
        pass

def test_handle_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    
    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html' and \
       'This is the content page!') not in result:
        assert False
    else:
        pass

def test_handle_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html' and \
       'This is the file page!') not in result:
        assert False
    else:
        pass
    
def test_handle_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html' and \
       'This is the image page!') not in result:
        assert False
    else:
        pass
    
def test_handle_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html') not in result:
        assert False
    else:
        pass
    

def test_post_request():
    conn = FakeConnection("POST /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html') not in result:
        assert False
    else:
        pass

def test_handle_get_submit():
    conn = FakeConnection("GET /submit?firstName=Jason&lastName=Bull HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html') not in result:
        assert False
    else:
        pass

def test_handle_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\nfirstName=Jason&lastName=Bull")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 200 OK' and \
       'Content-type: text/html') not in result:
        assert False
    else:
        pass

def test_handle_no_page():
    conn = FakeConnection("GET /youdontexist HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)
    result = conn.sent
    if('HTTP/1.0 404 Not Found' and \
       'Content-type: text/html' and \
       'This page does not exist!') not in result:
        assert False
    else:
        pass
