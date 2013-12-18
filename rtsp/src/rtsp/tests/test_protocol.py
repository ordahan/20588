'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.protocol import Protocol
from rtsp import directives, results
from rtsp.message import OptionsResponseMessage, RequestMessage


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.protocol_handler = Protocol()
        self.sequence = 17

    def tearDown(self):
        pass

    def testOptions(self):
        request = RequestMessage(directive=directives.OPTIONS,
                                 sequence=self.sequence)
        self.assertEqual(str(OptionsResponseMessage(self.sequence,
                                                    results.OK)),
                         self.protocol_handler.handle_request(str(request)))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
