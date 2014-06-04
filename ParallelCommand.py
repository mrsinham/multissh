__author__ = 'julien.lefevre'

import paramiko
import threading
import select
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

    def execute(self, sCommand, aGroupOfServer):
        # cleaning
        self.aThreads = []
        for sServer in aGroupOfServer:
            aTask = threading.Thread(None, self.__execCommandOnServer, None, [sCommand, sServer])
            aTask.start()
            self.aThreads.append(aTask)

    def __execAndRead(self, oChannel, sCommand):
        oChannel.exec_command(sCommand)
        sResponse = ''
        sResponseStdErr = ''
        while True:
            if oChannel.exit_status_ready():
                if '' == sResponse and '' == sResponseStdErr:
                    sResponse = bcolors.WARNING + 'no results' + bcolors.ENDC + "\n"
                break
            sCurrent = oChannel.recv(1024)
            if len(sCurrent) > 0:
                sResponse += sCurrent
                sResponseStdErr += oChannel.recv_stderr(1024)  # + "\n"
        return sResponse, sResponseStdErr

    def __execCommandOnServer(self, sCommand, sServer):
        oClient = paramiko.SSHClient()
        oClient.load_system_host_keys()
        oClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        oClient.connect(sServer, 22, 'prod')

        oChannel = oClient.get_transport().open_session()
        try:
            sResponse, sResponseStdErr = self.__execAndRead(oChannel, sCommand)
        except KeyboardInterrupt:
            oClient.close()

        self.oLock.acquire()
        print bcolors.OKBLUE + '['+bcolors.WARNING+sServer+bcolors.OKBLUE+']'+' '+sCommand + bcolors.ENDC

        sys.stdout.write(sResponse)
        sys.stdout.write(sResponseStdErr)

        self.oLock.release()
        oClient.close()
