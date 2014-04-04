import subprocess
import socket


class Streamer(object):
    '''
    Streams the requested file to given RTP port and listens to the given RTCP port.
    '''


    def _get_free_port_from_os(self):
        '''
        Gets a free port from the OS and binds a socket to it
        '''
        placeholder_sock = socket.socket()
        placeholder_sock.bind(('', 0))
        free_port_received_from_os = placeholder_sock.getsockname()[1]

        return (free_port_received_from_os, placeholder_sock)

    def __init__(self):
        '''
        Constructor
        '''

        # RTP process handler
        self.rtp_streamer = None

        # Server ports
        self.server_video_rtcp_port, self.video_placeholder_sock = self._get_free_port_from_os()
        self.server_audio_rtcp_port, self.audio_placeholder_sock = self._get_free_port_from_os()


    def play(self, media_file, client_video_rtp_port, client_video_rtcp_port,
             client_audio_rtp_port, client_audio_rtcp_port, client_ip_address):
        '''
        Sends a play command to the GStreamer with the given parameters
        '''

        # Play command parameters
        self.file = media_file
        self.client_video_rtp_port = client_video_rtp_port
        self.client_video_rtcp_port = client_video_rtcp_port
        self.client_audio_rtp_port = client_audio_rtp_port
        self.client_audio_rtcp_port = client_audio_rtcp_port
        self.client_ip_address = client_ip_address

        self.play_command = "gst-launch-0.10 -v gstrtpbin name=rtpbin1 \
            filesrc location={file} ! decodebin name=dec \
            dec.  ! queue ! x264enc ! rtph264pay ! rtpbin1.send_rtp_sink_0 \
            rtpbin1.send_rtp_src_0 ! udpsink host={ip} port={client_video_rtp_port} \
            rtpbin1.send_rtcp_src_0 ! udpsink host={ip} port={client_video_rtcp_port} \
            udpsrc port={server_video_rtcp_port} ! rtpbin1.recv_rtcp_sink_0 \
            dec. ! queue ! audioresample ! audioconvert ! alawenc ! rtppcmapay ! rtpbin1.send_rtp_sink_1 \
            rtpbin1.send_rtp_src_1 ! udpsink host={ip} port={client_audio_rtp_port} \
            rtpbin1.send_rtcp_src_1 ! udpsink host={ip} port={client_audio_rtcp_port} \
            udpsrc port={server_audio_rtcp_port} ! rtpbin1.recv_rtcp_sink_1".format(file=self.file,
                                                      client_video_rtp_port=self.client_video_rtp_port,
                                                      client_video_rtcp_port=self.client_video_rtcp_port,
                                                      server_video_rtcp_port=self.server_video_rtcp_port,
                                                      client_audio_rtp_port=self.client_audio_rtp_port,
                                                      client_audio_rtcp_port=self.client_audio_rtcp_port,
                                                      server_audio_rtcp_port=self.server_audio_rtcp_port,
                                                      ip=self.client_ip_address)

        print ("Play command sent to GStreamer: " + self.play_command)

        # Closes the sockets which held the port occupied,
        # right before we grant the ports to the streamer
        self.audio_placeholder_sock.close()
        self.video_placeholder_sock.close()

        self.rtp_streamer = subprocess.Popen(self.play_command.split())

    def stop(self):
        '''
        Terminates the RTP streamer process
        '''
        if (self.rtp_streamer is not None):
            print "Killing rtp_streamer (%d)" % self.rtp_streamer.pid
            self.rtp_streamer.kill()
            self.rtp_streamer = None

