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

    def handle_request(self, request_lines):
        '''
        Handles the given message.
        Returns the message to send back to the client (in
        the same format as the request_lines given)

        request_lines - List of lines that comprise the request
        '''
#         request_message = RequestMessage(sequence=sequence, request_lines)
#
#         if (request_message.directive_name == Directive.OPTIONS):
#             return ResponseMessage(request_message.sequence,)

        pass
