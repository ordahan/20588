'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.protocol import Protocol
from rtsp import directives
from rtsp import result_codes
from rtsp.message import OptionsResponseMessage, RequestMessage, \
    DescribeResponseMessage, SetupResponseMessage


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.protocol_handler = Protocol("192.168.0.8")
        self.sequence = 0
        self.uri = 'rtsp://abcd.com/30rock.avi'

    def tearDown(self):
        pass

    def options(self):

        request = RequestMessage(directive=directives.OPTIONS,
                                 sequence=self.sequence,
                                 uri=self.uri)
        expected_response = OptionsResponseMessage(self.sequence,
                                                   result=result_codes.OK)

        self.assertEqual(str(expected_response),
                         str(self.protocol_handler.process_message(request)))

    def describe(self):

        request = RequestMessage(directive=directives.DESCRIBE,
                                 sequence=self.sequence,
                                 uri=self.uri)

        expected_response = DescribeResponseMessage(self.sequence,
                                                    result=result_codes.OK,
                                                    date='Hi Ho I dont know',
                                                    server_uri=self.uri,
                                                    sdp_o_param=1234,
                                                    video_control_uri=self.uri + '/trackID=0',
                                                    audio_control_uri=self.uri + '/trackID=1')

        actual_response = self.protocol_handler.process_message(request)

        self.assertResponsesEquals(expected_response, actual_response)
        self.assertEqual(expected_response.video_control_uri, self.protocol_handler.video_control_uri)
        self.assertEqual(expected_response.audio_control_uri, self.protocol_handler.audio_control_uri)

    def setup(self):

        # Video
        self.protocol_handler.video_control_uri = self.uri + '/vid'

        request = RequestMessage(directive=directives.SETUP,
                                 sequence=self.sequence,
                                 uri=self.protocol_handler.video_control_uri,
                                 transport='client_port=52656-52657')
        request.client_rtp_port = 52656
        request.client_rtcp_port = 52657

        expected_response = SetupResponseMessage(self.sequence,
                                                 result=result_codes.OK,
                                                 client_rtp_port=request.client_rtp_port,
                                                 client_rtcp_port=request.client_rtcp_port,
                                                 # FIXME: Randomize the ports selected, we can't really know these upfront :)
                                                 server_rtp_port=20000,
                                                 server_rtcp_port=20001)

        self.assertEqual(str(expected_response),
                         str(self.protocol_handler.process_message(request)))

        # Audio
        self.protocol_handler.audio_control_uri = self.uri + '/aud'

        request = RequestMessage(directive=directives.SETUP,
                                 sequence=self.sequence,
                                 uri=self.protocol_handler.audio_control_uri)
        request.client_rtp_port = 52656
        request.client_rtcp_port = 52657

        expected_response = SetupResponseMessage(self.sequence,
                                                 result=result_codes.OK,
                                                 client_rtp_port=request.client_rtp_port,
                                                 client_rtcp_port=request.client_rtcp_port,
                                                 # FIXME: Randomize the ports selected, we can't really know these upfront :)
                                                 server_rtp_port=30000,
                                                 server_rtcp_port=30001)

        self.assertEqual(str(expected_response),
                         str(self.protocol_handler.process_message(request)))

    def assertResponsesEquals(self, expected_response, actual_response):
        try:
            expected_response.compare_deterministics(actual_response)
        except ValueError as e:
            raise AssertionError(str(e))

    def exec_protocol_stage(self, phase_function_return_val):
        self.sequence += 1

class TestProtocolBuildingBlocks(TestProtocol):
    '''
    This class tests the most basic building blocks of the protocol.
    Unlike the TestMessage class, this class doesn't have any concern regarding
    the actualy syntax, it DOES NOT create / expect any raw messages - it
    solely relies on the rtsp.Message layer to handle its job.
    '''

    def testOptions(self):
        self.exec_protocol_stage(self.options())

    def testDescribe(self):
        self.exec_protocol_stage(self.describe())

    def testSetup(self):
        self.exec_protocol_stage(self.setup())


class TestNominalScenario(TestProtocol):
    '''
    This class tests the basic bare-bone protocol to initiate an RTSP connection
    '''

    def testHappyFlow(self):
        self.exec_protocol_stage(self.options())
        self.exec_protocol_stage(self.describe())
        self.exec_protocol_stage(self.setup())

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()

