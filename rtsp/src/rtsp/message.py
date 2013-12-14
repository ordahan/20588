'''
Created on Dec 14, 2013

@author: ord
'''
import re
from rtsp import results, directives


class Message(object):
    '''
    An RTSP message parser / container
    '''

    PROTOCOL = 'RTSP/1.0'
    SEQUENCE_FIELD = 'CSeq: '

    def __init__(self, sequence):
        '''
        Creates a new message with the given sequence number
        '''
        self.sequence = sequence


class RequestMessage(Message):
    '''
    An RTSP Request message
    '''

    def __init__(self, directive=None, sequence=0):

        self.directive = directive
        self.sequence = sequence

        Message.__init__(self, self.sequence)

    def parse(self, message):
        '''
        Parses the given request into its different fields
        '''

        # Extract the directive
        self.directive = re.match('([A-Z]+)', message).group(1)

        # Extract the sequence number
        self.sequence = int(re.search(self.SEQUENCE_FIELD +
                                      '(\d+)',
                                      message).group(1))

    def __str__(self):
        return '\n\r'.join([self.directive,
                            self.SEQUENCE_FIELD + str(self.sequence)])


class ResponseMessage(Message):
    '''
    An RTSP Response message
    '''

    def __init__(self, sequence, result, payload=[]):
        self.result = result
        self.payload = payload

        Message.__init__(self, sequence)

    def __str__(self):
        # Create the response by joining the basic structure together
        # with the payload issued by the inheriting class
        message = ['%s %d %s' % (self.PROTOCOL,
                                          self.result,
                                          results.strings[self.result]),
                        self.SEQUENCE_FIELD + str(self.sequence)]
        message.extend(self.payload)
        return '\r\n'.join(message)


class OptionsResponseMessage(ResponseMessage):

    def __init__(self, sequence, result):
        payload = ["Public: %s %s %s %s %s" %
                            (directives.DESCRIBE,
                             directives.SETUP,
                             directives.TEARDOWN,
                             directives.PLAY,
                             directives.PAUSE)]
        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 payload=payload)
