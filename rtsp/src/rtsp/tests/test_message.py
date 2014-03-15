'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.message import RequestMessage, OptionsResponseMessage, \
    DescribeResponseMessage, SetupResponseMessage
from rtsp import directives
from rtsp import result_codes
from difflib import context_diff
import rtsp


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.request = RequestMessage()

    def assertMessagesEqual(self, expected_message, actual_message):

        expected_message_lines = expected_message.split(rtsp.message.Message.NEWLINE)
        actual_message_lines = actual_message.split(rtsp.message.Message.NEWLINE)

        delta = context_diff(expected_message_lines,
                             actual_message_lines,
                             fromfile='expected',
                             tofile='actual',
                             lineterm=rtsp.message.Message.NEWLINE)

        try:
            starting_line = delta.next()
            raise AssertionError('\n' + starting_line + rtsp.message.Message.NEWLINE.join(delta))
        except StopIteration:
            pass

    def testInit(self):

        request_generated = RequestMessage(directives.OPTIONS, 13)

        self.assertEqual(directives.OPTIONS, request_generated.directive)
        self.assertEqual(13, request_generated.sequence)
        self.assertEqual('OPTIONS\n\rCSeq: 13',
                         str(request_generated))

class TestOptions(TestMessage):

    def testParse(self):
        '''
        Tests the parsing of the options message
        '''
        # Basic valid message
        message = \
            ''.join(
                    ['OPTIONS ' + \
                     'rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',

                     'CSeq: 2\r\n',

                     'User-Agent: LibVLC/2.0.8 ' + \
                        '(LIVE555 Streaming Media v2011.12.23)\r\n',

                     '\r\n'])

        self.request.parse(message)

        self.assertEqual(2, self.request.sequence)
        self.assertEqual(directives.OPTIONS, self.request.directive)

    def testResponse(self):
        expected_response = \
            '\r\n'.join(["RTSP/1.0 200 OK",
                         "CSeq: 2",
                         "Content-Length: 0",
                         "Public: DESCRIBE,SETUP,TEARDOWN" +
                            ",PLAY,PAUSE,GET_PARAMETER",
                         '\r\n'])

        actual_response = str(OptionsResponseMessage(sequence=2,
                result=result_codes.OK))

        self.assertMessagesEqual(expected_response, actual_response)

class TestDescribe(TestMessage):

    def testParse(self):
        '''
        Tests the parsing of the describe message
        '''
        # Basic valid message
        message = \
            '\r\n'.join(['DESCRIBE rtsp://localhost:8554/homeland.avi RTSP/1.0',
                         'CSeq: 3',
                         'User-Agent: LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)',
                         'Accept: application/sdp',
                         '\r\n'])

        self.request.parse(message)

        self.assertEqual(3, self.request.sequence)
        self.assertEqual(directives.DESCRIBE, self.request.directive)

    def testResponse(self):

        date = 'Sun, 12 Jan 2014 13:04:23 GMT'
        server_ip = '127.0.0.1:18554'
        uri = 'rtsp://' + server_ip + '/homeland.avi'
        video_control = uri + '/trackID=0'
        audio_control = uri + '/trackID=1'
        length = 517
        sdp_o_param = 15455528565056244265

        expected_response = \
            '\r\n'.join([
                       'RTSP/1.0 200 OK',
                       'CSeq: 3',
                       'Content-Length: %d' % length,
                       'Server: VLC/2.0.8',
                       'Date: %s' % date,
                       'Content-Type: application/sdp',
                       'Content-Base: %s' % uri,
                       'Cache-Control: no-cache',
                       '',
                       'v=0',
                       'o=- {time} {time} IN IP4 {ip}'.format(time=sdp_o_param, ip=server_ip),
                       's=Unnamed',
                       'i=N/A',
                       'c=IN IP4 0.0.0.0',
                       't=0 0',
                       'a=tool:vlc 2.0.8',
                       'a=recvonly',
                       'a=type:broadcast',
                       'a=charset:UTF-8',
                       'a=control:%s' % uri,
                       'm=video 0 RTP/AVP 96',
                       'b=RR:0',
                       'a=rtpmap:96 H264/90000',
                       'a=fmtp:96 packetization-mode=1;profile-level-id=64001f;sprop-parameter-sets=Z2QAH6zZgLQz+sBagQEAoAAAfSAAF3AR4wYzQA==,aOl4fLIs;',
                       'a=control:%s' % video_control,
                       'm=audio 0 RTP/AVP 8',
                       'b=RR:0',
                       'a=control:%s' % audio_control,
                        '\r\n'])

        actual_response = str(DescribeResponseMessage(sequence=3,
                                                      result=result_codes.OK,
                                                      date=date,
                                                      server_uri=uri,
                                                      sdp_o_param=sdp_o_param,
                                                      video_control_uri=video_control,
                                                      audio_control_uri=audio_control))

        self.assertMessagesEqual(expected_response, actual_response)


class TestSetup(TestMessage):

    def testParse(self):
        '''
        Tests the parsing of the setup message
        '''
        # Basic valid message
        message = \
            '\r\n'.join(['SETUP rtsp://127.0.0.1:18554/homeland.avi/trackID=0 RTSP/1.0',
                         'CSeq: 4',
                         'User-Agent: LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)',
                         'Transport: RTP/AVP;unicast;client_port=52656-52657',
                         '\r\n'])

        self.request.parse(message)

        self.assertEqual(4, self.request.sequence)
        self.assertEqual(directives.SETUP, self.request.directive)
        self.assertEqual(52656, self.request.client_rtp_port)
        self.assertEqual(52657, self.request.client_rtcp_port)

    def testResponse(self):

        expected_response = \
            '\r\n'.join(['RTSP/1.0 200 OK',
                         'CSeq: 4',
                         'Content-Length: 0',
                         'Transport: RTP/AVP/UDP;unicast;client_port=52656-52657;server_port=30000-30001',
                         # FIXME: HIGH Generate a session for the message..not hardcode it
                         'Session: 12345',
                         '\r\n'])

        actual_response = str(SetupResponseMessage(sequence=4,
                                                      result=result_codes.OK,
                                                      client_rtp_port=52656,
                                                      client_rtcp_port=52657,
                                                      server_rtp_port=30000,
                                                      server_rtcp_port=30001))

        self.assertMessagesEqual(expected_response, actual_response)

# FIXME: LOW Test PLAY message

class TestGetParameter(TestMessage):

    def testParse(self):
        '''
        Tests the parsing of the GET_PARAMETER message
        '''
        # Basic valid message
        message = \
            '\r\n'.join(['GET_PARAMETER rtsp://127.0.0.1:18554/homeland.avi RTSP/1.0',
                         'CSeq: 7',
                         'User-Agent: LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)',
                         'Session: 18d000fccc6ddd5a',
                         '\r\n'])

        self.request.parse(message)

        self.assertEqual(7, self.request.sequence)
        self.assertEqual(directives.GET_PARAMETER, self.request.directive)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
