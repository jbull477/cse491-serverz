#!/usr/bin/env python
import random
import socket
import time

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
        
    

def handle_connection(conn):
    info = conn.recv(1000)
    print info
    htmlHeader = 'HTTP/1.0 200 OK\r\n'
    htmlContentType = 'Content-type: text/html\r\n\r\n'
    htmlBody = ' '
    
    request = info.split(' ')
    if request[0] == 'GET':
        try:
            host = request[3].split('\r')
            host = host[0]
        except IndexError:
            host = '';
        
        if request[1] == '/':
            contentLink = host + '/content'
            fileLink = host + '/file'
            imageLink = host + '/image'
            htmlBody = '<p><a href=\"http://' + contentLink + '\">Content</a>\r\n</p>' \
                       '<p><a href=\"http://' + fileLink + '\">Files</a>\r\n</p>' \
                       '<p><a href=\"http://' + imageLink + '\">Images</a></p>'
        elif request[1] == '/content':
            htmlBody = 'This is the content page!'
        elif request[1] == '/file':
            htmlBody = 'This is the file page!'
        elif request[1] == '/image':
            htmlBody = 'This is the image page!'
        else:
            htmlBody = '<h2>This page does not exist!</h2>'

        conn.send(htmlHeader)
        conn.send(htmlContentType)
        conn.send(htmlBody)
    elif request[0] == 'POST':
        conn.send('hello world')
        
    conn.close()

if __name__ == '__main__':
    main()
