'''
Created on Dec 14, 2013

@author: ord
'''
import re
from rtsp import directives
from rtsp import result_codes

class Message(object):
    '''
    An RTSP message parser / container
    '''

    PROTOCOL = 'RTSP/1.0'
    SEQUENCE_FIELD = 'CSeq: '
    NEWLINE = '\r\n'

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
                                 result_codes.strings[self.result]),
                                 self.SEQUENCE_FIELD + str(self.sequence)]
        message.extend(self.payload)

        return (self.NEWLINE).join(message)

    def get_deterministic_payload(self):
        pass

    def compare_deterministics(self, other_message):
        '''
        True - match
        False - don't match
        '''
        my_deter_payload = self.get_deterministic_payload()
        other_deter_payload = other_message.get_deterministic_payload()

        if (len(my_deter_payload) != len (other_deter_payload)):
            raise ValueError(len(my_deter_payload) + '!=' + len(other_deter_payload))

        line_changes = []
        for line_number in range(len(my_deter_payload)):
            if (my_deter_payload[line_number] !=
                other_deter_payload[line_number]):
                line_changes.append((my_deter_payload[line_number], other_deter_payload[line_number]))

        if (len(line_changes) > 0):
            raise ValueError('\n' + '\n'.join([str(change) for change in line_changes]))

        return True

class OptionsResponseMessage(ResponseMessage):

    def __init__(self, sequence, result):
        payload = ["Public: %s,%s,%s,%s,%s,%s" %
                            (directives.DESCRIBE,
                             directives.SETUP,
                             directives.TEARDOWN,
                             directives.PLAY,
                             directives.PAUSE,
                             directives.GET_PARAMETER),
                   self.NEWLINE]
        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 payload=payload)

class DescribeResponseMessage(ResponseMessage):

    def __init__(self,
                 sequence,
                 result,
                 date=None,
                 uri=None,
                 length=None,
                 sdp_o_param=None):
        payload = ['Server: VLC/2.0.8',
                   'Date: %s' % date,
                   'Content-Type: application/sdp',
                   'Content-Base: %s' % uri,
                   'Content-Length: %d' % length,
                   'Cache-Control: no-cache',
                   '',
                   'v=0',
                   'o=- {time} {time} IN IP4 desktop'.format(time=sdp_o_param),
                   's=Unnamed',
                   'i=N/A',
                   'c=IN IP4 0.0.0.0',  # TODO: Make the IP configurable as well
                   't=0 0',
                   'a=tool:vlc 2.0.8',
                   'a=recvonly',
                   'a=type:broadcast',
                   'a=charset:UTF-8',
                   'a=control:%s' % uri,
                   'm=video 0 RTP/AVP 96',
                   'b=RR:0',
                   'a=rtpmap:96 H264/90000',
                   'a=fmtp:96 packetization-mode=1;profile-level-id=64001f;sprop-parameter-sets=Z2QAH6zZgLQz+sBagQEAoAAAfSAAF3AR4wYzQA==,aOl4fLIs;',
                   'a=control:%s/trackID=0' % uri,
                   'm=audio 0 RTP/AVP 96',
                   'b=RR:0',
                   'a=rtpmap:96 mpeg4-generic/48000/2',
                   'a=fmtp:96 streamtype=5; profile-level-id=15; mode=AAC-hbr; config=1190; SizeLength=13; IndexLength=3; IndexDeltaLength=3; Profile=1;',
                   'a=control:%s/trackID=1' % uri,
                   self.NEWLINE]

        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 payload=payload)

    def get_deterministic_payload(self):
        deter_payload = [payload_line
                         for payload_line in self.payload
                         if (not payload_line.startswith('Date') and
                             not payload_line.startswith('o=-'))]
        return deter_payload
