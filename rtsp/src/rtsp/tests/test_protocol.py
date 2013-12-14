'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.protocol import Protocol


class TestMessage(unittest.TestCase):
    '''
    ['OPTIONS rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',
     'CSeq: 2\r\n',
     'User-Agent: LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)\r\n',
     '\r\n']
    '''

    def setUp(self):
        self.protocol_handler = Protocol()

    def tearDown(self):
        pass

    def testOptions(self):
        self.assertEqual("RTSP/1.0",
                         self.protocol_handler.handle_request("OPTIONS"))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
