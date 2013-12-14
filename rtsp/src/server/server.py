'''
Created on Dec 13, 2013

@author: ord
'''
import SocketServer
import connection_handler


class RTSPServer(SocketServer.TCPServer):
    '''
    Implements an RTSP based video server
    '''

    def __init__(self, bind_address="localhost", tcp_port=10554, folder="./"):
        '''
        Creates a new server that listens to the given tcp_port and provides
        RTSP streaming for files in the given folder
        '''
        self.folder = folder

        SocketServer.TCPServer.__init__(self,
                                        (bind_address, tcp_port),
                                        connection_handler.ConnectionHandler)

    def run(self):
        '''
        Runs the server.
        '''
        self.serve_forever()
