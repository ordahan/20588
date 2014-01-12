'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.message import RequestMessage, OptionsResponseMessage
from rtsp import directives, results


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.request = RequestMessage()

    def testConstructor(self):

        request_generated = RequestMessage(directives.OPTIONS, 13)

        self.assertEqual(directives.OPTIONS, request_generated.directive)
        self.assertEqual(13, request_generated.sequence)
        self.assertEqual('OPTIONS\n\rCSeq: 13',
                         str(request_generated))

class TestOptions(TestMessage):

    def testNominalParse(self):
        '''
        Tests the parsing of the options message
        '''
        # Basic valid message
        message = \
            ''.join(
                    ['OPTIONS' + \
                        'rtsp://localhost:10554/hello_world.avi RTSP/1.0\r\n',

                     'CSeq: 2\r\n',

                     'User-Agent: LibVLC/2.0.8 ' + \
                        '(LIVE555 Streaming Media v2011.12.23)\r\n',

                     '\r\n'])

        self.request.parse(message)

        self.assertEqual(2, self.request.sequence)
        self.assertEqual(directives.OPTIONS, self.request.directive)

        # TODO: More validity tests for parsing
        # 1) Options without URI - atm failing

    def testNominalResponse(self):
        response = \
            '\r\n'.join(["RTSP/1.0 200 OK",
                         "CSeq: 2",
                         "Public: DESCRIBE,SETUP,TEARDOWN" +
                            ",PLAY,PAUSE,GET_PARAMETER",
                         '\r\n'])
        self.assertEqual(response,
                         str(OptionsResponseMessage(sequence=2,
                                                    result=results.OK)))

class TestDescribe(TestMessage):

    def testDescribe(self):
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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMessage.testOptions']
    unittest.main()
