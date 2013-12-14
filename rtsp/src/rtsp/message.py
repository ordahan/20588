'''
Created on Dec 14, 2013

@author: ord
'''
import re


class Message(object):
    '''
    An RTSP message parser / container
    '''

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
