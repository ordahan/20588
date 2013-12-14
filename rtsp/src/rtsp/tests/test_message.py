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

    def setUp(self):
        self.request = RequestMessage()

    def testConstructor(self):

        request_generated = RequestMessage(directives.OPTIONS, 13)

        self.assertEqual(directives.OPTIONS, request_generated.directive)
        self.assertEqual(13, request_generated.sequence)
        self.assertEqual(['OPTIONS', 'CSeq: 13'],
                         request_generated.to_lines())

    def testOptions(self):
        '''
        Tests the parsing of the options message
        '''
        # Basic valid message
        message_lines = \
            ['OPTIONS rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',
             'CSeq: 2\r\n',
             'User-Agent: ' + \
                'LibVLC/2.0.8 (LIVE555 Streaming Media v2011.12.23)\r\n',
             '\r\n']

        self.request.parse(message_lines)

        self.assertEqual(2, self.request.sequence)
        self.assertEqual(directives.OPTIONS, self.request.directive)

        # TODO: More validity tests for parsing


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
