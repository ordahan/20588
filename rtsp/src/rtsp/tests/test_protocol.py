'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.protocol import Protocol
from rtsp import directives


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.protocol_handler = Protocol()

    def tearDown(self):
        pass

    def testOptions(self):
        request = \
            '\r\n'.join(
                 ['OPTIONS rtsp://localhost:10554/hello_world.avi RTSP/1.0',
                 'CSeq: 2',
                 ''])
        self.assertEqual("RTSP/1.0 200 OK\r\n" +
                         "CSeq: 2\r\n" +
                         "Public: %s %s %s %s %s" %
                            (directives.DESCRIBE,
                             directives.SETUP,
                             directives.TEARDOWN,
                             directives.PLAY,
                             directives.PAUSE),
                         self.protocol_handler.handle_request(request))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
