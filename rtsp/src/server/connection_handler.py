'''
Created on Dec 14, 2013

@author: ord
'''
import SocketServer
import rtsp.session


class ConnectionHandler(SocketServer.StreamRequestHandler):
    '''
    Implements a hook between the SocketServer object we use for the server
    and the underlying RTSP session handler that takes care of the given
    session
    '''
    def setup(self):
        '''
        Creates a new RTSP session handler and saves it
        for future requests
        '''
        self.rtsp_session_handler = rtsp.session.Session()
        SocketServer.StreamRequestHandler.setup(self)

    def handle(self):
        '''
        Reads the request received and calls the given session handler
        giving the request as argument
        '''
        request = self.rfile.readlines()

        response = self.rtsp_session_handler.handle_msg(request)

        self.wfile.write(''.join(response))
