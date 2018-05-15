from SSHConnect import SSHConnect
from SSHConnectPExpect import SSHConnectPExpect
from Logger import Logger

class VM(SSHConnect):

    def __init__(self,ip,username='root',password='insieme'):

        #self.log = Logger(filename='logfile.log',path ='/auto/AVS1/niranjan/scripts/framework/logs/')
        self.log = Logger()

        self.log.info("Initializing new VM object for {}" .format(ip))
        self.ip = ip
        self.username = username
        self.password = password
        self.lastlogin = ''
        self.devtype='vm'
        SSHConnect.__init__(self)

    def __repr__(self):
        return "<VM: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "VM IP : {}" .format(self.ip)
        print "VM Username : {}" .format(self.username)
        print "VM Password : {}" .format(self.password)
