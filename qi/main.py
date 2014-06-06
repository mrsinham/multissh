from qi import config, command

__author__ = 'julien.lefevre'

import time
try:
    import argparse
except ImportError:
    raise ImportError('you need arg parse module to use twssh')


def main():
    oMain = Main()
    try:
        oMain.run()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        oMain.stop()

class Main:

    def __init__(self):
        self.oConfigurationServer = config.Main()
        self.oParallel = command.ParallelCommand()
        self.sServerAlias = None
        self.sCmd = None
        self.aArgs = None
        self.oParser = None

    def __executeFromExecute(self):
        if self.aArgs.serveralias is None:
            raise Exception('unable to know serveralias')
        self.sServerAlias = self.aArgs.serveralias
        self.sCmd = self.aArgs.execute
        sServerList = self.oConfigurationServer.getServerByAlias(self.sServerAlias)
        self.oParallel.execute(self.sCmd, sServerList)

    def run(self):
        self.__parseArgument()
        self.oConfigurationServer.loadConfigurationFromFile()

        if self.aArgs.execute is not None:
            if self.aArgs.serveralias is None:
                raise Exception('unable to execute without server alias')
            self.__executeFromExecute()

        if self.aArgs.command is not None:
            aArgs = []
            if self.aArgs.args is not None:
                aArgs = self.aArgs.args
            aAliasAndCmd = self.oConfigurationServer.getAliasAndCmd(self.aArgs.command, aArgs)
            self.oParallel.execute(aAliasAndCmd['cmd'], self.oConfigurationServer.getServerByAlias(aAliasAndCmd['alias']))

    def __parseArgument(self):
        self.oParser = argparse.ArgumentParser(description='Execute multiple commands in qi on server')
        self.oParser.add_argument('-e', '--execute', help='Command to execute')
        self.oParser.add_argument('-s', '--serveralias', help='Servers alias as specified in configuration file')
        self.oParser.add_argument('-c', '--command', help='prefilled command in the cmd section')
        self.oParser.add_argument('-a', '--args', nargs='*')
        self.aArgs = self.oParser.parse_args()

    def stop(self):
        self.oParallel.stop()




