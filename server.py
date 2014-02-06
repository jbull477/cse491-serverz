#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from urlparse import parse_qs
import cgi
from StringIO import StringIO
import jinja2


#Globals
app_content = 'Content-type: application/x-www-form-urlencoded\r\n\r\n'
error_header = 'HTTP/1.0 404 Not Found\r\n'
multi_content = 'Content-type: multipart/form-data\r\n\r\n'
okay_header = 'HTTP/1.0 200 OK\r\n'
text_content = 'Content-type: text/html\r\n\r\n'
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        handle_connection(c)
        

# Handles the connection
def handle_connection(conn):
    info = conn.recv(1)
    while info[-4:] != '\r\n\r\n':
        info += conn.recv(1)
    
    request = info.split(' ')
    urlRequest = request[1]
    urlInfo = urlparse(urlRequest)
    urlPath = urlInfo.path

    if request[0] == 'GET':
        handle_get(conn, urlPath, info)
    elif request[0] == 'POST':
        handle_post(conn, urlPath)
    conn.close()

# Taken from leflerja
def handle_get(conn, path, info):
    params = parse_qs(urlparse(path)[4])
    page = urlparse(path)[2]
    vars_dict = {}
    get_pages = { '/'  :  'index.html',  \
                  '/favicon.ico'  :  'index.html',  \
                  '/content'  : 'content.html',  \
                  '/file'  :  'files.html',  \
                  '/image'  :  'image.html',  \
                  '/form'  :  'get_form.html',  \
                  '/submit'  :  'get_submit.html'  }
    print page
    if page in get_pages:
        template = env.get_template(get_pages[page])
        if(page == "/submit"):
            firstName, lastName = handle_submit(conn, urlparse(info.split(' ')[1]), info, info.split(' ')[0])
            vars_dict = {'firstName': firstName, 'lastName': lastName}
        conn.send(okay_header)
        conn.send(text_content)
        conn.send(template.render(vars_dict))
    else:
        template = env.get_template('error.html')
        conn.send(error_header)
        conn.send(text_content)
        conn.send(template.render())
    
# Taken from leflerja
def handle_post(conn, path, info):
    headers = []
    body = ""
    has_body = False

    for line in request.split("\r\n"):
        if has_body:
            body = line
            continue
        if line == "":
            has_body = True
        headers.append(line)

    path = request.split()[1]
    page = urlparse(path)[2]
    params = parse_qs(body)

    post_pages = {'/' : post_request, \
                  '/form' : post_form, \
                  '/submit' : post_submit }

    conn.send(okay_header)
    conn.send(app_content)
    conn.send(post_pages[page](conn, params))

def handle_submit(conn, urlInfo, info, reqType):
    if reqType == "GET":
        query = urlInfo.query
    elif reqType == "POST":
        query = info.splitlines()[-1]
        
    data = parse_qs(query)
    firstName = data['firstName'][0]
    lastName = data['lastName'][0]
    return (firstName, lastName)

def handle_post(conn, info):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h2>hello world</h2>'
    conn.send(toSend)

def post_request(conn, request):
    return 'HTTP/1.0 200 OK\r\n\r\n' + \
           'This is a post request'

def post_form(conn, params):
    return '<h1>Form Page</h1>\r\n' + \
           '<form action=\'/submit\' method=\'POST\'>\r\n' + \
           'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' + \
           'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' + \
           '<input type=\'submit\' name=\'submit\'>\r\n' + \
           '</form>\r\n'

def post_submit(conn, params):
    return '<h1>Submit Page</h1>\r\n' + \
           'Hello {0} {1}'.format(params['firstname'][0], params['lastname'][0])
    

if __name__ == '__main__':
    main()
