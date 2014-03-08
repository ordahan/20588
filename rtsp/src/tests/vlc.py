'''
Created on Mar 8, 2014

@author: ord
'''
import unittest
import subprocess
import multiprocessing
from server.server import RTSPServer
import time

class Test(unittest.TestCase):


    def setUp(self):
        self.rtsp_server_process = multiprocessing.Process(target=RTSPServer().run)
        self.rtsp_server_process.start()


    def tearDown(self):
        self.rtsp_server_process.terminate()


    def testNormalPlayScenario(self):
        self.vlc_client_process = subprocess.Popen('cvlc -vvv rtsp://localhost:8554/30rock.avi'.split(),)
        time.sleep(1)
        self.vlc_client_process.terminate()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testNormalPlayScenario']
    unittest.main()
