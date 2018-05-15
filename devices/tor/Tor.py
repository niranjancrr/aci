from SSHConnect import SSHConnect
from SSHConnectPExpect import SSHConnectPExpect
from Logger import Logger
from torLibs import *

class Tor(SSHConnect,SSHConnectPExpect,Utilities,TorTriggers,TorValidate):

    def __init__(self,ip,username='admin',password='ins3965!'):

        self.log = Logger()

        self.log.info("Initializing new TOR object for {}" .format(ip))
        self.ip = ip
        self.username = username
        self.password = password
        self.lastlogin = ''
        self.devtype='tor'
        SSHConnect.__init__(self)
        SSHConnectPExpect.__init__(self)
        Utilities.__init__(self)
        TorTriggers.__init__(self)
        TorValidate.__init__(self)

    def __repr__(self):
        return "<Tor: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "Tor IP : {}" .format(self.ip)
        print "Tor Username : {}" .format(self.username)
        print "Tor Password : {}" .format(self.password)
        return True

