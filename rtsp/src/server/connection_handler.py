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

        self.rtsp_protocol_handler = rtsp.protocol.Protocol(client_ip_address=self.client_address[0])
        SocketServer.StreamRequestHandler.setup(self)

    def finish(self):
        self.rtsp_protocol_handler.kill_streamer()
        SocketServer.StreamRequestHandler.finish(self)

    def respond_to_client(self, response):
        return self.wfile.write(response)


    def read_client_request(self):
        # TODO: LOW Config the received size + make global define
        request = self.request.recv(4096)

        if (request == ''):
            return None
        else:
            return request

    def handle(self):
        '''
        This method is called by the server 'behind-the-scenes'
        For each new connection.
        '''

        __profile__ = False
        connection_alive = True

        while (connection_alive):
            if (__profile__):
                import cProfile

                pr = cProfile.Profile()
                pr.enable()

            request = self.read_client_request()

            # TODO: LOW consider blocking until receiving data

            # If no data was read, sleep and try again.
            if (request == None):
                time.sleep(0.1)
                continue

            print "Got:"
            print "--------------------------------------------"
            print request
            print "--------------------------------------------"

            response = self.rtsp_protocol_handler.handle_request(request)

            if (response is None):
                print "Connection is terminated (no response sent to client)"
                connection_alive = False
            else:
                print "Sent:"
                print "--------------------------------------------"
                print response
                print "--------------------------------------------"

                self.respond_to_client(response)

            if (__profile__):
                pr.disable()
                pr.print_stats()
