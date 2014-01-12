'''
Created on Dec 14, 2013

@author: ord
'''
import SocketServer
import rtsp.protocol

class ConnectionHandler(SocketServer.StreamRequestHandler):
    '''
    Implements a hook between the SocketServer object we use for the server
    and the underlying RTSP session handler that takes care of the given
    session
    '''
    def setup(self):
        '''
        This method is called by the server 'behind-the-scenes'
        when a new connection is established.

        Initializes the objects we need in order to handle the
        connection.
        '''
        self.rtsp_protocol_handler = rtsp.protocol.Protocol()
        SocketServer.StreamRequestHandler.setup(self)

    def handle(self):
        '''
        This method is called by the server 'behind-the-scenes'
        each time a new packet arrives on the connection.
        '''

        import cProfile

        pr = cProfile.Profile()
        pr.enable()

        request = self.request.recv(2 ** 16 - 1)

        print request

        response = self.rtsp_protocol_handler.handle_request(request)

        print response

        self.wfile.write(response)

        pr.disable()

#         pr.print_stats()
