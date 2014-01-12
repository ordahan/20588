'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, ResponseMessage
from rtsp import directives
from rtsp import result_codes


class Protocol(object):
    '''
    Handles the RTP protocol for a single connection.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass


    def generate_response_for_request(self, request_message):

        if (request_message.directive == directives.OPTIONS):
            response = OptionsResponseMessage(sequence=request_message.sequence,
                                              result=result_codes.OK)

        elif (request_message.directive == directives.DESCRIBE):
            response = DescribeResponseMessage(sequence=request_message.sequence,
                                               result=result_codes.OK,
                                               date='Sun, 12 Jan 2014 13:04:23 GMT',
                                               uri='rtsp://localhost:8554/homeland.avi',
                                               length=717,  # TODO: Use the data from the file opened
                                               sdp_o_param=15455528565056244265)
        else:
            response = ResponseMessage()

        return response

    def handle_request(self, request):
        '''
        Handles the given message.
        Returns the message to send back to the client (in
        the same format as the request given)
        This method is in charge of translating from string to request/response
        objects and back (CLEAN CODE? ME THINK NOT :D)

        request - String representing the request to handle
        '''

        # Create a request from the given string
        request_message = RequestMessage()
        if (request_message.parse(request) == False):
            print("Error parsing message: %s" % request)
            # TODO: Return an error response
            return ""

        response = self.generate_response_for_request(request_message)

        return str(response)
