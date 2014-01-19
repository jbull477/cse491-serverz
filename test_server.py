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

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    content_conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    file_conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    image_conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    # Figure out how to dynamically fill in the host name of the link
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<p><a href=\"http:///content\">Content</a>\r\n</p>' + \
                      '<p><a href=\"http:///file\">Files</a>\r\n</p>' + \
                      '<p><a href=\"http:///image\">Images</a></p>'
    
    content_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is the content page!'
    
    file_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is the file page!'

    image_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is the image page!'
    
    server.handle_connection(conn)
    server.handle_connection(content_conn)
    server.handle_connection(file_conn)
    server.handle_connection(image_conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    assert content_conn.sent == content_return, 'Got: %s' % (repr(content_conn.sent),)
    assert file_conn.sent == file_return, 'Got: %s' % (repr(file_conn.sent),)
    assert image_conn.sent == image_return, 'Got: %s' % (repr(image_conn.sent),)
