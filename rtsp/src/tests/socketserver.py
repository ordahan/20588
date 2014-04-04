'''
Created on Apr 4, 2014

@author: ord
'''
import unittest
import SocketServer
import socket
import sys
import multiprocessing
import os
import time


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        while(True):
            # self.rfile is a file-like object created by the handler;
            # we can now use e.g. readline() instead of raw recv() calls
            self.data = self.rfile.readline().strip()
            print "{} wrote:".format(self.client_address[0])
            print self.data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class Test(unittest.TestCase):

    def testMultipleConnections(self):
        # Create the server, binding to localhost on port 9999
        server = ThreadedTCPServer(("localhost", 9999), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server_process = multiprocessing.Process(target=server.serve_forever)
        server_process.start()

        # Run client 1
        client_process1 = multiprocessing.Process(target=client_side)
        client_process1.start()

        # Run client 1
        client_process2 = multiprocessing.Process(target=client_side2)
        client_process2.start()

        time.sleep(30)

        server_process.terminate()
        client_process1.terminate()
        client_process2.terminate()


def client_side():
    HOST, PORT = "localhost", 9999
    data = "nika"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        while(True):
            sock.sendall(data + "\n")
            time.sleep(3)
    finally:
        sock.close()

def client_side2():
    HOST, PORT = "localhost", 9999
    data = "OrDahan"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        while(True):
            sock.sendall(data + "\n")
            time.sleep(3)
    finally:
        sock.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testMultipleConnections']
    unittest.main()




