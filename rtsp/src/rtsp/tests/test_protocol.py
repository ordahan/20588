'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.protocol import Protocol
from rtsp import directives
from rtsp import result_codes
from rtsp.message import OptionsResponseMessage, RequestMessage, \
    DescribeResponseMessage


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.protocol_handler = Protocol()
        self.sequence = 1

    def tearDown(self):
        pass

    def options(self):

        request = RequestMessage(directive=directives.OPTIONS,
                                 sequence=self.sequence)
        expected_response = str(OptionsResponseMessage(self.sequence,
                                                       result=result_codes.OK))

        self.assertEqual(expected_response, self.protocol_handler.handle_request(str(request)))

    def describe(self):

        request = RequestMessage(directive=directives.DESCRIBE,
                                 sequence=self.sequence)

        expected_response = DescribeResponseMessage(self.sequence,
                                                    result=result_codes.OK,
                                                    date='Hi Ho I dont know',
                                                    uri='rtsp://localhost:8554/homeland.avi',  # FIXME: Save this from the previous phase
                                                    length=717,  # FIXME: Get this from somewhere else
                                                    sdp_o_param=1234)

        actual_response = self.protocol_handler.generate_response_for_request(request)

        self.assertResponsesEquals(expected_response, actual_response)

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


class TestNominalScenario(TestProtocol):
    '''
    This class tests the basic bare-bone protocol to initiate an RTSP connection
    '''

    def testHappyFlow(self):
        self.exec_protocol_stage(self.options())
        self.exec_protocol_stage(self.describe())

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()

