from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, ResponseMessage, SetupResponseMessage
from rtsp import directives
from rtsp import result_codes
import datetime
import os
from rtp.streamer import Streamer


class Protocol(object):
    '''
    Handles the RTSP protocol for a single connection.
    '''

    def __init__(self, client_ip_address):
        '''
        Constructor
        '''
        self.uri = ''
        self.video_control_uri = ''
        self.audio_control_uri = ''
        self.rtp_streamer = Streamer()
        self.client_ip_address = client_ip_address
        self.file = ''
        self.session = 12345


    def process_message(self, request_message):
        '''
        Processes the request message and generates a response
        '''
        response = None

        # Options request - returns the options on the given file
        if (request_message.directive == directives.OPTIONS):

            response = OptionsResponseMessage(sequence=request_message.sequence,
                                              result=result_codes.OK)

        # Describe request - returns the file's details (including the file's streams)
        elif (request_message.directive == directives.DESCRIBE):

            current_time = datetime.datetime.utcnow()
            time_diff_from_ntp_epoch = current_time - datetime.datetime(1900, 1, 1, 0, 0, 0)
            ntp_timestamp = time_diff_from_ntp_epoch.days * 24 * 60 * 60 + time_diff_from_ntp_epoch.seconds
            self.uri = request_message.uri

            self.file = os.environ["HOME"] + "/Videos/" + request_message.uri.rsplit('/', 1)[1]

            # If the file exists
            if (os.access(self.file, os.R_OK)):
                self.video_control_uri = request_message.uri + '/trackID=0'
                self.audio_control_uri = request_message.uri + '/trackID=1'
                response = DescribeResponseMessage(sequence=request_message.sequence,
                                                   result=result_codes.OK,
                                                   date=current_time.strftime("%a, %d %b %Y %X GMT"),
                                                   server_uri=request_message.uri,
                                                   sdp_o_param=ntp_timestamp,
                                                   video_control_uri=self.video_control_uri,
                                                   audio_control_uri=self.audio_control_uri)
            else:
                print "File '{}' doesn't exist ({})".format(self.file, self.uri)

        # Setup request - client's setup configurations for each stream
        elif (request_message.directive == directives.SETUP):

            # Setup for video channel
            if (request_message.uri == self.video_control_uri):

                self.client_video_rtp_port = request_message.client_rtp_port
                self.client_video_rtcp_port = request_message.client_rtcp_port

                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=self.client_video_rtp_port,
                                                client_rtcp_port=self.client_video_rtcp_port,
                                                server_rtp_port=self.rtp_streamer.server_video_rtcp_port - 1,
                                                server_rtcp_port=self.rtp_streamer.server_video_rtcp_port,
                                                session=self.session)
            # Setup for audio channel
            elif (request_message.uri == self.audio_control_uri):

                self.client_audio_rtp_port = request_message.client_rtp_port
                self.client_audio_rtcp_port = request_message.client_rtcp_port

                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=self.client_audio_rtp_port,
                                                client_rtcp_port=self.client_audio_rtcp_port,
                                                server_rtp_port=self.rtp_streamer.server_audio_rtcp_port - 1,
                                                server_rtcp_port=self.rtp_streamer.server_audio_rtcp_port,
                                                session=self.session)
        # Play request
        elif (request_message.directive == directives.PLAY):
            response = ResponseMessage(sequence=request_message.sequence,
                                       result=result_codes.OK)

            self.rtp_streamer.play(self.file,
                                     self.client_video_rtp_port,
                                     self.client_video_rtcp_port,
                                     self.client_audio_rtp_port,
                                     self.client_audio_rtcp_port,
                                     self.client_ip_address)

        # Get parameter request
        elif (request_message.directive == directives.GET_PARAMETER):
            response = ResponseMessage(sequence=request_message.sequence,
                                       result=result_codes.OK)
        # Teardown request - tear down the session
        elif (request_message.directive == directives.TEARDOWN):
            self.kill_streamer()
            response = None
        # Unknown request - responding none
        else:
            response = ResponseMessage(request_message.sequence,
                                       result_codes.OPTION_NOT_SUPPORTED)

        return response

    def handle_request(self, request_text):
        '''
        Handles the given message.
        Returns the response_text to send back to the client (in
        the same format as the request_text was given)
        This method is in charge of translating from string to request_message/response_message
        objects and back to string

        request_text - String representing the request_text to handle

        returns - A response_text to send, and whether or not the protocol is alive
        '''

        protocol_is_alive = True
        response_text = None

        # Create a request_message from the given string
        request_message = RequestMessage()
        if (request_message.parse(request_text) == True):
            response_message = self.process_message(request_message)
        else:
            print("Error parsing message: %s" % request_text)
            response_message = ResponseMessage(0,
                                       result_codes.INTERNAL_SERVER_ERROR)

        if (response_message is not None):
            response_text = str(response_message)

            if (response_message.result != result_codes.OK):
                protocol_is_alive = False

        return (response_text, protocol_is_alive)

    def kill_streamer(self):
        self.rtp_streamer.stop()

