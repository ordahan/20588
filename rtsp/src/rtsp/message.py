'''
Created on Dec 14, 2013

@author: ord
'''
import re


class Message(object):
    '''
    An RTSP message parser / container
    '''

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

    def parse(self, message_lines):
        '''
        Parses the given lines into a request message.
        '''

        # Extract the directive
        self.directive = re.match('([A-Z]+)', message_lines[0]).group(1)

        # Extract the sequence number
        self.sequence = int(re.match('CSeq\: (\d+)',
                                     message_lines[1]).group(1))

    def to_lines(self):
        return [self.directive, 'CSeq: ' + str(self.sequence)]
