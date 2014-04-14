__author__ = 'julien.lefevre'

import os,ConfigParser,pprint

class Main:

    def __init__(self):
        self.sFilename = os.path.expanduser('~')+'/.parallel'
        self.oConfigParser = None
        self.oServer = None
        self.oCmd = None

    def loadConfigurationFromFile(self, sFilename=None):
        """
        Load configuration from file on disk
        """
        if None != sFilename:
            self.sFilename = sFilename
        self.sFilename = os.path.abspath(self.sFilename)
        if not os.path.isfile(self.sFilename):
            raise Exception('file ' + self.sFilename + ' dont exists')

        oConfigParser = ConfigParser.ConfigParser()
        oConfigParser.read(self.sFilename)
        self.oConfigParser = oConfigParser

    def getServerByAlias(self, sAlias):

        if None == self.oServer:
            self.oServer = Server()
            self.oServer.parseServerSection(self.oConfigParser)
        return self.oServer.getServerByAlias(sAlias)

    def getAliasAndCmd(self, sCmdName, aCmdArgs):
        if None == self.oCmd:
            self.oCmd = Command()
            self.oCmd.parseCmdSection(self.oConfigParser)
        return self.oCmd.getCmd(sCmdName, aCmdArgs)


class Server:

    def __init__(self):
        self.aConfiguration = {}

    def parseServerSection(self, oConfigParser):
        aSection = oConfigParser.sections()
        if 'server' not in aSection:
            raise Exception('server section not found in ' + self.sFilename)

        for aKeyValues in oConfigParser.items('server'):
            (sKey, mValue) = aKeyValues
            self.aConfiguration[sKey] = mValue.split(',')

    def getServerByAlias(self, sAlias):
        """
        Returns loaded section
        """
        if sAlias not in self.aConfiguration:
            raise Exception('alias '+sAlias+' not filled in server file')
        return self.aConfiguration[sAlias]

class Command:

    def __init__(self):
        self.aConfiguration = {}

    def parseCmdSection(self, oConfigParser):
        aSection = oConfigParser.sections()
        if 'cmd' not in aSection:
            return False

        for aKeyValues in oConfigParser.items('cmd'):
            (sKey, mValue) = aKeyValues
            aAliasAndCmd = mValue.split(',')
            if len(aAliasAndCmd) != 2:
                raise Exception('cmd '+sKey+' not well filled. Must be alias,cmd')
            self.aConfiguration[sKey] = {
                'alias': aAliasAndCmd[0],
                'cmd': aAliasAndCmd[1]
            }

    def getCmd(self, sCmdName, aArguments):

        if sCmdName not in self.aConfiguration:
            raise Exception('cmd '+sCmdName+' not filled in configuration file')

        sCmd = self.aConfiguration[sCmdName]
        for sArgs in aArguments:
            sCmd['cmd'] = sCmd['cmd'].replace('[-]', sArgs, 1)
        return self.aConfiguration[sCmdName]

