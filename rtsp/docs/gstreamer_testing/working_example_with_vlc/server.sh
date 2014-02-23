gst-launch-0.10 -v gstrtpbin name=rtpbin1 filesrc location=/home/ord/git/rtsp/rtsp/docs/30rock.avi ! decodebin ! x264enc ! rtph264pay ! rtpbin1.send_rtp_sink_0 rtpbin1.send_rtp_src_0 ! udpsink host=127.0.0.1 port=5004 rtpbin1.send_rtcp_src_0 ! udpsink host=127.0.0.1 port=5012 udpsrc port=5013 ! rtpbin1.recv_rtcp_sink_0 

