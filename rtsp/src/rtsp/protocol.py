'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage, OptionsResponseMessage
from rtsp import directives, results


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
        if (request_message.parse(request) == False):
            print("Error parsing message: %s" % request)
            # TODO: Return an error response
            return ""

        if (request_message.directive == directives.OPTIONS):
            options_response = OptionsResponseMessage(sequence=request_message.sequence,
                                                      result=results.OK)
            return str(options_response)
        elif (request_message.directive == directives.DESCRIBE):
            print "DESCRIBE? YOU WANT ME TO DESCRIBE? ME? SURELY YOU MUST BE JOKING."
