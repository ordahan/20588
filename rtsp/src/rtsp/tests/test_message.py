'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.message import RequestMessage
from rtsp import directives


class TestMessage(unittest.TestCase):
    '''
    ['OPTIONS rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',
     'CSeq: 2\r\n',
     'User-Agent: LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)\r\n',
     '\r\n']
    '''

    def testOptions(self):
        message_lines = \
            ['OPTIONS rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',
             'CSeq: 2\r\n',
             'User-Agent: ' + \
                'LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)\r\n',
             '\r\n']
        request = RequestMessage(message_lines=message_lines)

        self.assertEqual(2, request.sequence)
        self.assertEqual(directives.OPTIONS, request.directive)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
