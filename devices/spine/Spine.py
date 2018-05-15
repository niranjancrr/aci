from SSHConnect import SSHConnect
from SSHConnectPExpect import SSHConnectPExpect
from Logger import Logger
from spineLibs import *

class Spine(SSHConnect, SSHConnectPExpect, SpineTriggers):

    def __init__(self,ip,username='admin',password='ins3965!'):

        #self.log = Logger(filename='logfile.log',path ='/auto/AVS1/niranjan/scripts/framework/logs/')
        self.log = Logger()

        self.log.info("Initializing new Spine object for {}" .format(ip))
        self.ip = ip
        self.username = username
        self.password = password
        self.lastlogin = ''
        self.devtype='spine'
        SSHConnect.__init__(self)
        SSHConnectPExpect.__init__(self)
        SpineTriggers.__init__(self)

    def __repr__(self):
        return "<Spine: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "Spine IP : {}" .format(self.ip)
        print "Spine Username : {}" .format(self.username)
        print "Spine Password : {}" .format(self.password)
        return True
