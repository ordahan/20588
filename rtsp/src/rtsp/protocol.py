'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, ResponseMessage, SetupResponseMessage
from rtsp import directives
from rtsp import result_codes
import datetime


class Protocol(object):
    '''
    Handles the RTSP protocol for a single connection.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.uri = ''
        self.video_control_uri = ''
        self.audio_control_uri = ''


    def process_message(self, request_message):

        # Options request - returns the options on the given file
        if (request_message.directive == directives.OPTIONS):
            self.uri = request_message.uri

            response = OptionsResponseMessage(sequence=request_message.sequence,
                                              result=result_codes.OK)

        # Describe request - returns the file's details (including the file's streams)
        elif (request_message.directive == directives.DESCRIBE):
            current_time = datetime.datetime.utcnow()
            time_diff_from_ntp_epoch = current_time - datetime.datetime(1900, 1, 1, 0, 0, 0)
            ntp_timestamp = time_diff_from_ntp_epoch.days * 24 * 60 * 60 + time_diff_from_ntp_epoch.seconds

            self.video_control_uri = request_message.uri + '/trackID=0'
            self.audio_control_uri = request_message.uri + '/trackID=1'
            response = DescribeResponseMessage(sequence=request_message.sequence,
                                               result=result_codes.OK,
                                               date=current_time.strftime("%a, %d %b %Y %X GMT"),
                                               uri=request_message.uri,  # TODO: Low, Is the uri 'saved' for this connection? or does it come from the describe msg?
                                               sdp_o_param=ntp_timestamp,
                                               video_control_uri=self.video_control_uri,
                                               audio_control_uri=self.audio_control_uri)

        # Setup request - client's setup configurations for each stream
        elif (request_message.directive == directives.SETUP):

            if (request_message.uri == self.video_control_uri):
                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=request_message.client_rtp_port,
                                                client_rtcp_port=request_message.client_rtcp_port,
                                                # FIXME: Randome ports
                                                server_rtp_port=20000,
                                                server_rtcp_port=20001)

            elif (request_message.uri == self.audio_control_uri):
                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=request_message.client_rtp_port,
                                                client_rtcp_port=request_message.client_rtcp_port,
                                                # FIXME: Randome ports
                                                server_rtp_port=30000,
                                                server_rtcp_port=30001)
        # TODO: Play request
#         elif (request_message.directive == directives.SETUP):
        elif (request_message.directive == directives.TEARDOWN):
            response = None
        else:
            response = None

        return response

    def handle_request(self, request):
        '''
        Handles the given message.
        Returns the response to send back to the client (in
        the same format as the request was given)
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

        response = self.process_message(request_message)

        if (response is None):
            return None

        return str(response)
