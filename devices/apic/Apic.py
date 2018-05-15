from SSHConnect import SSHConnect
from SSHConnectPExpect import SSHConnectPExpect
from Logger import Logger
from apicLibs import ApicTriggers,XML,Utilities

class Apic(SSHConnect,SSHConnectPExpect,ApicTriggers,XML,Utilities):

    def __init__(self,ip,username='admin',password='ins3965!'):

        #self.log = Logger(filename='logfile.log',path ='/auto/AVS1/niranjan/scripts/framework/logs/')
        self.log = Logger()

        self.log.info("Initializing new Apic object for {}" .format(ip))
        self.devtype='apic'
        self.ip = ip
        self.username = username
        self.password = password
        self.lastlogin = ''
        SSHConnect.__init__(self)
        SSHConnectPExpect.__init__(self)
        ApicTriggers.__init__(self)
        Utilities.__init__(self)
        XML.__init__(self)
        #MoQuery.__init__(self)

    def __repr__(self):
        return "<Apic: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "Apic IP : {}" .format(self.ip)
        print "Apic Username : {}" .format(self.username)
        print "Apic Password : {}" .format(self.password)
        return True

    def execute_root(self,cmd):
        #self.connect(override=True)
        op = self.execute(cmd,override=True)
        return op
        #self.disconnect()

    def execute_root_pexpect(self,cmd):
        #self.pexpect_connect(override=True)
        op = self.pexpect_execute(cmd,override=True)
        return op
        #self.pexpect_disconnect()
