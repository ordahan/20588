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
        self.sequence = 17

    def tearDown(self):
        pass


    def exec_options_phase(self):
        request = RequestMessage(directive=directives.OPTIONS, sequence=self.sequence)
        expected_response = str(OptionsResponseMessage(self.sequence,
                                                       result_codes.OK))
        self.assertEqual(expected_response, self.protocol_handler.handle_request(str(request)))

    def exec_describe_phase(self):
        request = RequestMessage(directive=directives.DESCRIBE, sequence=self.sequence)
        expected_response = str(DescribeResponseMessage(self.sequence,
                                                        result_codes.OK))
        self.assertEqual(expected_response, self.protocol_handler.handle_request(str(request)))

class TestProtocolBuildingBlocks(TestProtocol):
    '''
    This class tests the most basic building blocks of the protocol.
    Unlike the TestMessage class, this class doesn't have any concern regarding
    the actualy syntax, it DOES NOT create / expect any raw messages - it
    solely relies on the rtsp.Message layer to handle its job.
    '''

    def testOptions(self):
        self.exec_options_phase()

    def testParse(self):
        self.exec_describe_phase()


class TestNominalScenario(TestProtocol):
    '''
    This class tests the basic bare-bone protocol to initiate an RTSP connection
    '''

    def testHappyFlow(self):
        self.exec_options_phase()
        self.exec_describe_phase()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()

