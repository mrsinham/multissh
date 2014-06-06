__author__ = 'julien.lefevre'

import paramiko
import threading
from threading import Lock
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class ParallelCommand:

    def __init__(self):
        self.oLock = Lock()
        self.aThreads = []
        self.oEvent = threading.Event()
        self.bFinished = False

    def execute(self, sCommand, aGroupOfServer):
        # cleaning
        self.aThreads = []
        self.oEvent.set()
        for sServer in aGroupOfServer:
            oThread = Command(self.oLock, sCommand, sServer, self.oEvent)
            self.aThreads.append(oThread)
            oThread.daemon = True
            oThread.start()

        while True:
            i = 0
            for oThread in self.aThreads:
                if not oThread.isAlive():
                    i += 1
            if len(self.aThreads) == i:
                raise SystemExit()

    def stop(self):
        self.oEvent.clear()
        for oThread in self.aThreads:
            oThread.stop()
            # pass



class Command(threading.Thread):

    def __init__(self, oLock, sCommand, sServer, oEvent):
        super(Command, self).__init__()
        self.oLock = oLock
        self.sCommand = sCommand
        self.sServer = sServer
        self.bRunning = True
        self.oEvent = oEvent
        self.oChannel = None
        self.bActive = True

    def run(self):
        oClient = paramiko.SSHClient()
        oClient.load_system_host_keys()
        oClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        oClient.connect(self.sServer, 22, 'prod')

        oChannel = oClient.get_transport().open_session()

        sResponse = ''
        sResponseStdErr = ''

        oChannel.exec_command(self.sCommand)
        oChannel.set_combine_stderr(True)
        self.oChannel = oChannel
        while self.oEvent.is_set():
            if oChannel.exit_status_ready():
                if '' == sResponse and '' == sResponseStdErr:
                    sResponse = bcolors.WARNING + 'no results' + bcolors.ENDC + "\n"
                break
            try:
                oData = oChannel.recv(1024)
                while oData:
                    sResponse += oData
                    oData = oChannel.recv(1024)
            except (SSHException, e):
                pass
                return

        oClient.close()

        sResponse += "\n"
        # if self.bActive:
        self.oLock.acquire()
        sys.stdout.write(bcolors.OKBLUE + '['+bcolors.WARNING+self.sServer+bcolors.OKBLUE+']'+' '+self.sCommand + bcolors.ENDC+"\n")
        sys.stdout.write(sResponse)
        self.oLock.release()

    def stop(self):
        self.bActive = False
        self.oEvent.clear()
        if self.oChannel is not None:
            self.oChannel.shutdown(0)
            self.oChannel.close()

