'''
Created on Dec 14, 2013

@author: ord
'''


class Session(object):
    '''
    Handles an RTSP session
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def handle_msg(self, msg):
        '''
        Handles the given message.
        Returns the message to send back to the client (in
        the same format as the msg given)

        msg - List of lines that comprise the request
        '''
        pass
