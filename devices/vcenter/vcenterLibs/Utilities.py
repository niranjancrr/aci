from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim,vmodl
from Logger import Logger

class Utilities:

    def __init__(self):
        self.log = Logger()
        self.log.info('Initializing Vcenter Utilities Class')
        self.connect()

    def connect(self):
        '''
            Initialize connection to the current Vcenter
            Does not take any arguments
        '''
        try:
            self.connection_handle = SmartConnect(host=self.ip, user=self.username, pwd=self.password)
            self.log.info('Connection to VC {} was successful' .format(self.ip))
            return True
        except:
            self.log.info('Connection to VC {} failed' .format(self.ip))
            return False

