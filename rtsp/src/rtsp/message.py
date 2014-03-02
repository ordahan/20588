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
    CONTENT_LENGTH = 'Content-Length: '
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

    def __init__(self, directive=None, sequence=0, uri=None):

        self.directive = directive
        self.sequence = sequence
        self.uri = uri

        Message.__init__(self, self.sequence)


    def parse_header(self, message):
    # Extract the directive
        try:
            parameters = re.match('([A-Z]+)\s+(.+)', message)

            return parameters.group(1, 2)
        except AttributeError as e:
            print "Failed to parse request header line"
            raise e
        return e


    def parse_sequence_number(self, message):
    # Extract the sequence number
        try:
            return int(re.search(self.SEQUENCE_FIELD + '(\d+)', message).group(1))
        except AttributeError as e:
            print "Failed to parse sequence"
            raise e

    def parse(self, message):
        '''
        Parses the given request into its different fields
        '''
        try:
            message_fields = message.split(self.NEWLINE)

            if (len(message_fields) == 0):
                return False

            self.directive, self.uri = self.parse_header(message_fields[0])

            self.sequence = self.parse_sequence_number(message)

            return True

        except BaseException as parse_error:
            print "Parse error: ", parse_error
            print "Originated from: '%s'" % message
            return False


    def _generate_header(self):
        if (self.uri is not None):
            return '{} {}'.format(self.directive, self.uri)
        else:
            return self.directive

    def __str__(self):
        return '\n\r'.join([self._generate_header(),
                            self.SEQUENCE_FIELD + str(self.sequence)])


class ResponseMessage(Message):
    '''
    An RTSP Response message
    '''

    def __init__(self, sequence, result, additional_fields=[], content_lines=[]):
        self.result = result
        self.additional_fields = additional_fields
        self.content_lines = content_lines

        Message.__init__(self, sequence)

    def __str__(self):

        # Create the response by joining the basic structure together
        # with the additional_fields and the content issued by the inheriting class

        response_field = '%s %d %s' % (self.PROTOCOL,
                                       self.result,
                                       result_codes.strings[self.result])

        sequence_field = self.SEQUENCE_FIELD + str(self.sequence)

        content_length = sum([len(content_line) for content_line in self.content_lines])
        content_length_field = self.CONTENT_LENGTH + str(content_length)

        # Basic RTSP message structure
        message = [response_field,
                   sequence_field,
                   content_length_field]

        # All the fields the specific message needs
        message.extend(self.additional_fields)

        # There is content attached to the message
        if (content_length > 0):
            message.append('')
            message.extend(self.content_lines)

        # Finalizing newline of the RTSP response
        message.append(self.NEWLINE)

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
                             directives.GET_PARAMETER)]

        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 additional_fields=payload)

class DescribeResponseMessage(ResponseMessage):

    def __init__(self,
                 sequence,
                 result,
                 date=None,
                 uri=None,
                 sdp_o_param=None):

        sdp_fields = [ 'v=0',
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
                       # TODO: Low, allow other encodings for video and audio
                       'a=rtpmap:96 H264/90000',
                       'a=fmtp:96 packetization-mode=1;profile-level-id=64001f;sprop-parameter-sets=Z2QAH6zZgLQz+sBagQEAoAAAfSAAF3AR4wYzQA==,aOl4fLIs;',
                       'a=control:%s/trackID=0' % uri,
                       'm=audio 0 RTP/AVP 8',
                       'b=RR:0',
                       'a=control:%s/trackID=1' % uri, ]

        payload = ['Server: VLC/2.0.8',
                   'Date: %s' % date,
                   'Content-Type: application/sdp',
                   'Content-Base: %s' % uri,
                   'Cache-Control: no-cache']

        ResponseMessage.__init__(self, sequence=sequence,
                                 result=result,
                                 additional_fields=payload,
                                 content_lines=sdp_fields)

    def get_deterministic_payload(self):
        deter_payload = [payload_line
                         for payload_line in self.additional_fields
                         if (not payload_line.startswith('Date') and
                             not payload_line.startswith('o=-'))]
        return deter_payload
