'''
Created on Dec 14, 2013

@author: ord
'''
import SocketServer
import rtsp.protocol
import time

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
        For each new connection.
        '''

        __profile__ = False

        while (True):
            if (__profile__):
                import cProfile

                pr = cProfile.Profile()
                pr.enable()

            request = self.request.recv(4096)
            if (request == ''):
                time.sleep(0.1)
                continue
    #         self.timeout = 0.2
    #         self.rbufsize = 0
    #         request = ''.join(self.rfile.readlines())

            print "Got:"
            print "--------------------------------------------"
            print request
            print "--------------------------------------------"

            response = self.rtsp_protocol_handler.handle_request(request)

            print "Sent:"
            print "--------------------------------------------"
            print response
            print "--------------------------------------------"


            self.wfile.write(response)

            if (__profile__):
                pr.disable()
                pr.print_stats()
