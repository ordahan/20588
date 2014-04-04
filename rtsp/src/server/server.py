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

    def __init__(self, bind_address="localhost", tcp_port=8554):
        '''
        Creates a new server that listens to the given tcp_port and provides
        RTSP streaming for files in the given folder
        '''
        # Allow the socket to be re-bound right after we shutdown
        # the server
        SocketServer.TCPServer.allow_reuse_address = True

        SocketServer.TCPServer.__init__(self,
                                        (bind_address, tcp_port),
                                        connection_handler.ConnectionHandler)

    def run(self):
        '''
        Runs the server.
        '''

        print "Starting to run RTSP server..."

        self.serve_forever()

        print "Shutting down RTSP server..."
