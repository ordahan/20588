'''
Created on Dec 14, 2013

@author: ord
'''
from rtsp import directives


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

    def __init__(self, message_lines):
        '''
        Parses the given lines into a request message.
        '''

        self.directive = None
        sequence = 0

        Message.__init__(self, sequence)
        pass
