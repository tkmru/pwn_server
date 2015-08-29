#! /usr/local/bin/python3

import socket
import sys

argc = len(sys.argv)

if argc == 3:
    arg_port = int(sys.argv[1])

    HOST, PORT = 'localhost', arg_port
    data = ' '.join(sys.argv[2:])

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        try:
            sock.sendall(bytes(data + '\n', 'utf-8'))
            # Receive data from the server and shut down
            received = str(sock.recv(1024), 'utf-8')

        except TypeError:
            sock.sendall(bytes(data + '\n'))
            # Receive data from the server and shut down
            received = str(sock.recv(1024))

    finally:
        sock.close()

    print('Sent:     {}'.format(data))
    print('Received: {}'.format(received))

else:
    print('pwn_test.py [EXECUTABLE FILE PATH] [PORT]')
