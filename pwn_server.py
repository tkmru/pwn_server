#! /usr/local/bin/python
# coding: UTF-8

import sys
import subprocess

try:
    import socketserver # for python3
except ImportError:
    import SocketServer as socketserver # for python2


class PwnableTCPServer(socketserver.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, target):
        self.target = target
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


class PwnableTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.received = self.request.recv(1024).strip()
        print('\nReceived:{0}'.format(self.received))

        self.result = subprocess.check_output([self.server.target, self.received])
        self.request.sendall(self.result)
        print('Sent:    {0}'.format(self.result))


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 3:
        target = sys.argv[1]
        arg_port = int(sys.argv[2])

        HOST, PORT = 'localhost', arg_port
        print('Pwnable server starts...')
        print('Host:    {0}'.format(HOST))
        print('Port:    {0}'.format(PORT))
        print('Target:  {0}'.format(target))

        server = PwnableTCPServer((HOST, PORT), PwnableTCPHandler, target)
        server.serve_forever()

    else:
        print('pwnserver.py [EXECUTABLE FILE PATH] [PORT]')
