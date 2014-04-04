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
        print("*****************************************")
        print("        Creating a new connection")
        print("*****************************************")
        self.rtsp_protocol_handler = rtsp.protocol.Protocol(client_ip_address=self.client_address[0])
        SocketServer.StreamRequestHandler.setup(self)

    def finish(self):
        '''
        Terminate the connection and cleanup
        '''
        self.rtsp_protocol_handler.kill_streamer()
        SocketServer.StreamRequestHandler.finish(self)

    def respond_to_client(self, response):
        '''
        Write the response to the wfile
        '''
        return self.wfile.write(response)


    def read_client_request(self):
        '''
        Read message from receive buffer
        '''
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

            # If no data was read, sleep and try again.
            if (request == None):
                time.sleep(0.1)
                continue

            print "Got:"
            print "--------------------------------------------"
            print request
            print "--------------------------------------------"

            response, connection_alive = self.rtsp_protocol_handler.handle_request(request)

            if (response is None):
                print "No response sent to client"
            else:
                print "Sent:"
                print "--------------------------------------------"
                print response
                print "--------------------------------------------"

                self.respond_to_client(response)

            if (__profile__):
                pr.disable()
                pr.print_stats()

        print "Connection is terminated."
