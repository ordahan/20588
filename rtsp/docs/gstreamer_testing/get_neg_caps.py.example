#!/usr/bin/python
 
import pygst
pygst.require("0.10")
import gst
#import pygtk
#import gtk
 
class Main:
    def __init__(self):
        self.pipeline = gst.element_factory_make("playbin2", "src")
        self.pipeline.props.uri = "file:///home/ord/git/rtsp/rtsp/docs/30 Rock [3.18] Jackie Jormp-Jomp.avi"
 
        self.sink = gst.element_factory_make("xvimagesink", "sink")
 
        self.pipeline.props.video_sink = self.sink
 
        self.pipeline.set_state(gst.STATE_PAUSED)  # asynchroneous
        # wait for the pipeline to be prerolled so the caps get negotiated
        if gst.STATE_CHANGE_SUCCESS == self.pipeline.get_state(gst.CLOCK_TIME_NONE)[0]:
            pads = self.sink.pads()
            for pad in pads:
                neg_caps = pad.get_negotiated_caps()[0]  # simplified, there could be more caps
                framerate = neg_caps["framerate"]  # simplified, maybe there is no "framerate"
                print "The framerate of the src is %d/%dfps" % (framerate.num, framerate.denom)
        self.pipeline.set_state(gst.STATE_PLAYING)
 
start=Main()
#gtk.main()
