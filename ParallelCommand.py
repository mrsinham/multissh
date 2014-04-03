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

    def execute(self, sCommand, aGroupOfServer):
        for sServer in aGroupOfServer:
            aTask = threading.Thread(None, self.__execCommandOnServer, None, [sCommand, sServer])
            aTask.start()

    def __execCommandOnServer(self, sCommand, sServer):
        print "executing "+sCommand+" on "+sServer
        oClient = paramiko.SSHClient()
        oClient.load_system_host_keys()
        oClient.connect(sServer, 22, 'prod')
        (stdin, stdout, stderr) = oClient.exec_command(sCommand)
        self.oLock.acquire()
        print bcolors.OKBLUE + "\nresults on " + sServer + ":" + bcolors.ENDC

        for line in stdout.readlines():
            sys.stdout.write(line)
        self.oLock.release()
        oClient.close()

#oCommandExecutor = ParallelCommand()
#oCommandExecutor.execute('grep "8780145292375003232" -R /opt/twenga/var/log/front-b2c-prod-showcase-item-service-update/', aServer['cli'])

#execCommand('grep "8780145292375003232" -R /opt/twenga/var/log/front-b2c-prod-showcase-item-service-update/', aServer['cli'])