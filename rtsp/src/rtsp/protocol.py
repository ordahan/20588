'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage


class Protocol(object):
    '''
    Handles the RTP protocol for a single connection.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def handle_request(self, request):
        '''
        Handles the given message.
        Returns the message to send back to the client (in
        the same format as the request given)

        request - String representing the request to handle
        '''
        # Create a request from the given string
        request_message = RequestMessage()
        request_message.parse(request)

        pass
