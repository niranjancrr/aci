from Logger import Logger

class Datacenter:

    def __init__(self):
        self.log = Logger()
        self.log.info('Initializing Vcenter Datacenter Class')
        self.populate_datacenters()
        self.populate_datacenter_portgroups()
        self.populate_datacenter_hosts()

    def populate_datacenters(self):
        '''
            Populates datacenterDict under vcenter object which has DC name to DC object mappings
            Does not take any arguments
        '''
        self.datacenterDict = {}
        try:
            for datacenter in self.connection_handle.content.rootFolder.childEntity:
                self.datacenterDict[datacenter.name] = datacenter
                self.log.info('Vcenter {} has Datacenter {}' .format(self.ip,datacenter.name))
        except:
            self.log.error('Exception encountered while trying to populate Datacenter object {}' .format(datacenter))

    def populate_datacenter_portgroups(self):
        '''
            Populates datacenterPortGroupsDict under vcenter object based on datacenterDict
        '''
        self.datacenterPortGroupsDict = {}
        try:
            for datacenter in self.datacenterDict.values():
                portgroups = {}
                for portgroup in datacenter.network:
                    portgroups[portgroup.name]=portgroup
                self.log.info('Datacenter {} has portgroups {}' .format(datacenter.name,portgroups.keys()))
                self.datacenterPortGroupsDict[datacenter.name] = portgroups
        except:
            self.log.error('Exception encountered while trying to populate datacenter {} portgroups' .format(datacenter.name))
        
    def populate_datacenter_hosts(self):
        '''
            Populates datacenterHostsDict under vcenter object based on datacenterDict
        '''
        self.datacenterHostsDict = {}
        try:
            for datacenter in self.datacenterDict.values():
                hosts = {}
                for host in datacenter.hostFolder.childEntity:
                    hosts[host.name] = host
                self.log.info('Datacenter {} has hosts {}' .format(datacenter.name,hosts.keys()))
                self.datacenterHostsDict[datacenter.name] = hosts
        except:
            self.log.error('Exception encountered while trying to populate datacenter {} hosts' .format(datacenter.name))
      
    #def populate_datacenter_vms_per_host(self):

    #def get_host_mo(self):
    #    '''
    #    '''

    #def get_portgroup_mo(self):
    #    '''
    #    '''
        
