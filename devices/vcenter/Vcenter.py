from vcenterLibs import *
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim,vmodl
from Logger import Logger

class Vcenter(Utilities,Datacenter):

    def __init__(self, ip, username='root', password='vmware'):
        self.ip = ip
        self.username = username
        self.password = password
        self.devtype = 'vcenter'
        Utilities.__init__(self)
        Datacenter.__init__(self)

    def __repr__(self):
        return "<Vcenter: {}>" .format(self.ip)

    def __call__(self):
        print "Device Type : {}" .format(self.devtype.capitalize())
        print "Vcenter IP : {}" .format(self.ip)
        print "Vcenter Username : {}" .format(self.username)
        print "Vcenter Password : {}" .format(self.password)
        return True
