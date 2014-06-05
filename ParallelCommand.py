__author__ = 'julien.lefevre'

import paramiko
import threading
import select
from pprint import  pprint
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

    def execute(self, sCommand, aGroupOfServer):
        # cleaning
        self.aThreads = []
        self.oEvent.set()
        for sServer in aGroupOfServer:

            oThread = Command(self.oLock, sCommand, sServer, self.oEvent)
            self.aThreads.append(oThread)
            oThread.start()
            # aTask = threading.Thread(None, self.__execCommandOnServer, None, [sCommand, sServer])
            # aTask.start()

    def stop(self):
        pprint('sending stop')
        self.oEvent.clear()
        for oThread in self.aThreads:
            oThread.join()
            # pass


class Command(threading.Thread):

    def __init__(self, oLock, sCommand, sServer, oEvent):
        super(Command, self).__init__()
        self.oLock = oLock
        self.sCommand = sCommand
        self.sServer = sServer
        self.bRunning = True
        self.oEvent = oEvent

    def run(self):
        oClient = paramiko.SSHClient()
        oClient.load_system_host_keys()
        oClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        oClient.connect(self.sServer, 22, 'prod')

        oChannel = oClient.get_transport().open_session()

        oChannel.get_pty()
        # return oChannel
        sResponse = ''
        sResponseStdErr = ''
        # pprint(self.sCommand)

        oChannel.exec_command(self.sCommand)
        while True:
            rl, wl, xl = select.select([oChannel],[],[],0.0)
            if len(rl) > 0:
                pprint('read '+self.sServer)
                sCurrent = oChannel.recv(1024)
                sResponse += sCurrent
                sResponseStdErr += oChannel.recv_stderr(1024)
            if oChannel.exit_status_ready():
                if '' == sResponse and '' == sResponseStdErr:
                    sResponse = bcolors.WARNING + 'no results' + bcolors.ENDC + "\n"
                break

        self.oLock.acquire()
        print bcolors.OKBLUE + '['+bcolors.WARNING+self.sServer+bcolors.OKBLUE+']'+' '+self.sCommand + bcolors.ENDC
        sResponse += "\n"
        sResponseStdErr += "\n"
        sys.stdout.write(sResponse)
        sys.stdout.write(sResponseStdErr)
        self.oLock.release()


