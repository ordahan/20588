'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, ResponseMessage
from rtsp import directives
from rtsp import result_codes
import datetime


class Protocol(object):
    '''
    Handles the RTP protocol for a single connection.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.uri = ''


    def process_message(self, request_message):

        if (request_message.directive == directives.OPTIONS):
            self.uri = request_message.uri

            response = OptionsResponseMessage(sequence=request_message.sequence,
                                              result=result_codes.OK)

        elif (request_message.directive == directives.DESCRIBE):
            current_time = datetime.datetime.utcnow()
            time_diff_from_ntp_epoch = current_time - datetime.datetime(1900, 1, 1, 0, 0, 0)
            ntp_timestamp = time_diff_from_ntp_epoch.days * 24 * 60 * 60 + time_diff_from_ntp_epoch.seconds

            response = DescribeResponseMessage(sequence=request_message.sequence,
                                               result=result_codes.OK,
                                               date=current_time.strftime("%a, %d %b %Y %X GMT"),
                                               uri=request_message.uri,  # TODO: Low, Is the uri 'saved' for this connection? or does it come from the describe msg?
                                               sdp_o_param=ntp_timestamp)
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
        else:
            response = self.process_message(request_message)

        return str(response)
