'''
Created on Dec 14, 2013

@author: ord
'''
import unittest
from rtsp.session import Session


class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        pass

    def testOptionsDirective(self):
        self.assertEqual("RTSP/1.0", self.session.handle_msg("OPTIONS"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestSession.testOptions']
    unittest.main()
