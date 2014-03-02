gst-launch-0.10 -v gstrtpbin name=rtpbin1 \
filesrc location=/home/ord/git/rtsp/rtsp/docs/30rock.avi ! decodebin name=dec \
dec.  ! queue ! x264enc ! rtph264pay ! rtpbin1.send_rtp_sink_0 \
rtpbin1.send_rtp_src_0 ! udpsink host=127.0.0.1 port=5004 \
rtpbin1.send_rtcp_src_0 ! udpsink host=127.0.0.1 port=5005 \
udpsrc port=5009 ! rtpbin1.recv_rtcp_sink_0 \
dec. ! queue ! audioresample ! audioconvert ! alawenc ! rtppcmapay ! rtpbin1.send_rtp_sink_1 \
rtpbin1.send_rtp_src_1 ! udpsink host=127.0.0.1 port=5006 \
rtpbin1.send_rtcp_src_1 ! udpsink host=127.0.0.1 port=5007 \
udpsrc port=5011 ! rtpbin1.recv_rtcp_sink_1
