'''
Created on Dec 14, 2013

@author: ord
'''
import re
from rtsp import results, directives
import rtsp


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
        try:

            # Extract the directive
            try:
                self.directive = re.match('([A-Z]+)', message).group(1)
            except AttributeError as e:
                print "Failed to parse directive"
                raise e

            # Extract the sequence number
            try:
                self.sequence = int(re.search(self.SEQUENCE_FIELD +
                                              '(\d+)',
                                              message).group(1))
            except AttributeError as e:
                print "Failed to parse sequence"
                raise e

            return True

        except BaseException as parse_error:
            print "Parse error: ", parse_error
            print "Originated from: '%s'" % message
            return False

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
        return (rtsp.protocol.NEWLINE).join(message)


class OptionsResponseMessage(ResponseMessage):

    def __init__(self, sequence, result):
        payload = ["Public: %s,%s,%s,%s,%s,%s" %
                            (directives.DESCRIBE,
                             directives.SETUP,
                             directives.TEARDOWN,
                             directives.PLAY,
                             directives.PAUSE,
                             directives.GET_PARAMETER),
                   rtsp.protocol.NEWLINE]
        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 payload=payload)
