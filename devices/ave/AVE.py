from SSHConnect import SSHConnect
from SSHConnectPExpect import SSHConnectPExpect
from Logger import Logger
#from aveLibs import *

#class AVE(SSHConnect,AVEValidate,AVETriggers):
class AVE(SSHConnect):

    def __init__(self,ip,username='admin',password='Sfish123'):

        #self.log = Logger(filename='logfile.log',path ='/auto/AVS1/niranjan/scripts/framework/logs/')
        self.log = Logger()

        self.log.info("Initializing new ESX object for {}" .format(ip))
        self.ip = ip
        self.username = username
        self.password = password
        self.lastlogin = ''
        self.devtype='ave'
        SSHConnect.__init__(self)
        #AVEValidate.__init__(self)
        #AVETriggers.__init__(self)

    def __repr__(self):
        return "<AVE: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "ESX IP : {}" .format(self.ip)
        print "ESX Username : {}" .format(self.username)
        print "ESX Password : {}" .format(self.password)
