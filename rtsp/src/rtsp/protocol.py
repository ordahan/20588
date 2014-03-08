'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, ResponseMessage, SetupResponseMessage, \
    PlayResponseMessage
from rtsp import directives
from rtsp import result_codes
import datetime
import subprocess


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

                self.client_video_rtp_port = request_message.client_rtp_port
                self.client_video_rtcp_port = request_message.client_rtcp_port

                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=self.client_video_rtp_port,
                                                client_rtcp_port=self.client_video_rtcp_port,
                                                # FIXME: Randome ports
                                                server_rtp_port=20000,
                                                server_rtcp_port=20001)

            elif (request_message.uri == self.audio_control_uri):

                self.client_audio_rtp_port = request_message.client_rtp_port
                self.client_audio_rtcp_port = request_message.client_rtcp_port

                response = SetupResponseMessage(sequence=request_message.sequence,
                                                result=result_codes.OK,
                                                client_rtp_port=self.client_audio_rtp_port,
                                                client_rtcp_port=self.client_audio_rtcp_port,
                                                # FIXME: Randome ports
                                                server_rtp_port=30000,
                                                server_rtcp_port=30001)
        elif (request_message.directive == directives.PLAY):
            response = PlayResponseMessage(sequence=request_message.sequence,
                                           result=result_codes.OK)
            # TODO: Start GStreamer
            self.rtp_streamer_process = subprocess.Popen(("gst-launch-0.10 -v gstrtpbin name=rtpbin1 \
filesrc location=/home/ord/Videos/30rock.avi ! decodebin name=dec \
dec.  ! queue ! x264enc ! rtph264pay ! rtpbin1.send_rtp_sink_0 \
rtpbin1.send_rtp_src_0 ! udpsink host=127.0.0.1 port=%d \
rtpbin1.send_rtcp_src_0 ! udpsink host=127.0.0.1 port=%d \
udpsrc port=%d ! rtpbin1.recv_rtcp_sink_0 \
dec. ! queue ! audioresample ! audioconvert ! alawenc ! rtppcmapay ! rtpbin1.send_rtp_sink_1 \
rtpbin1.send_rtp_src_1 ! udpsink host=127.0.0.1 port=%d \
rtpbin1.send_rtcp_src_1 ! udpsink host=127.0.0.1 port=%d \
udpsrc port=%d ! rtpbin1.recv_rtcp_sink_1" % (self.client_video_rtp_port,
                                              self.client_video_rtcp_port,
                                              20001,
                                              self.client_audio_rtp_port,
                                              self.client_audio_rtcp_port,
                                              30001,)) .split())

        elif (request_message.directive == directives.GET_PARAMETER):
            # TODO: Support GET_PARAMETER
            response = None
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
