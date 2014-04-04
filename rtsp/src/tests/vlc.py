'''
Created on Mar 8, 2014

@author: ord
'''
import unittest
import subprocess
import multiprocessing
from server.server import RTSPServer
import time
import socket

class Test(unittest.TestCase):


    def setUp(self):
        self.my_ip = socket.gethostbyname(socket.gethostname())
        self.rtsp_server = RTSPServer(bind_address=str(self.my_ip))
        self.rtsp_server_process = multiprocessing.Process(target=self.rtsp_server.run)
        self.rtsp_server_process.start()


    def tearDown(self):
        print "Ending test...."
        self.rtsp_server_process.terminate()
        print "Done"


#     def testNormalPlayScenario(self):
#         self.vlc_client_process = subprocess.Popen('vlc -vvv rtsp://192.168.0.195:8554/30rock2.avi'.split())
#         time.sleep(20)
#         self.vlc_client_process.terminate()
#         time.sleep(1)

    def testMultipleClients(self):
        self.vlc_client_process = subprocess.Popen('vlc -vvv rtsp://{}:8554/30rock.avi'.format(self.my_ip).split())
        self.vlc_client_process1 = subprocess.Popen('vlc -vvv rtsp://{}:8554/30rock2.avi'.format(self.my_ip).split())
        time.sleep(20)
        self.vlc_client_process.terminate()
        self.vlc_client_process1.terminate()
        time.sleep(1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testNormalPlayScenario']
    unittest.main()
