import time
import re

class AVEValidate():

    def __init__(self):
        self.log.info("Intializing API's for AVEi show command Validations")

    #VMK related procs
    def validate_vmk(self,vmk='vmk1',subnet=10):
        '''
            make sure the specified vmk is getting dhcp ip from specified network.
            default vmk is vmk1
            default expected subnet is 10.X.X.X
        '''
        flag = False

        #Max wait time is 4 mins for vmk1 to get IP
        counter  = 240
        elapsed = 0
        while counter:
            try:
                ip = self.get_vmk_ip(vmk)
                if re.search('{}\.\d+\.\d+\.\d+'.format(subnet),self.contents) == None:
                    raise
                flag = True
                self.log.info("AVE {} was able to aquire DHCP IP {} on {} interface in {} secs" .format(self.ip,ip,vmk,elapsed))
                return flag
            except:
                self.log.error("AVE {} did not get DHCP IP on {} interface in {} secs" .format(self.ip,vmk,elapsed))
                self.log.info("Sleeping for 10 secs")
                time.sleep(10)
                elapsed += 10
                counter -= 10

        return flag

    def get_vmk_ip(self,vmk='vmk1'):
        '''
            get the DHCP IP that was assigned to the specified vmk interface
        '''
        cmd = 'esxcfg-vmknic -l | grep {}' .format(vmk)
        self.contents = self.execute(cmd)
        #self.log.info(self.contents)
        ip = re.search('{}\s+\d+\s+\w+\s+(\d+\.\d+\.\d+\.\d+)'.format(vmk),self.contents).group(1)
        return ip

    #Opflex related procs
    def validate_opflex(self, override=False):
        '''
            Make sure opflex channels(s) are up on the host
            'override' is disabled by default, both channels should be up for this proc to pass
            if 'override' is enabled, it is enough if one opflex channel is up
        '''
        flag = False
 
        #Max wait time is 5 mins for opflex to come up on host
        counter  = 300
        elapsed = 0
        while counter:
            try:
                if override:
                    if self.get_opflex_status(override):
                        self.log.info("Opflex came up on AVE {} in {} secs" .format(self.ip,elapsed))
                        return True
                    else:
                        raise
                else:
                    if self.get_opflex_status():
                        self.log.info("Opflex came up on AVE {} in {} secs" .format(self.ip,elapsed))
                        return True
                    else:
                        raise
            except:
                self.log.error("Opflex did not come up on AVE {} in {} secs" .format(self.ip,elapsed))
                self.log.info("Sleeping for 10 secs")
                time.sleep(10)
                elapsed += 10
                counter -= 10

        return flag

    def get_opflex_status(self, override=False):
        '''
            Return the opflex status on host based on override flag
            'override' enabled means validate for one opflex active channel
        '''
        flag = False
        cmd = 'vemcmd show opflex'
        self.contents = self.execute(cmd)
        #self.log.info(self.contents)
        if override:
            if len(re.findall('(12 \(Active\))',self.contents)) == 2:
                flag = True
        else:
            if len(re.findall('(12 \(Active\))',self.contents)) == 3:
                flag = True
            
        return flag
                
    def get_vemcmd_show_port_info(self):
        '''
            Get relavant information by executing vemcmd show port command
        '''
        portDict = {}
        cmd = 'vemcmd show port'
        op = self.execute(cmd)
        #self.log.info(op)
        params = re.findall('\s+(\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+-\s+\d+\s+(\d+)\s+\d+\s+\d+\s+([\w-]*\.*\w+)',op)
        for entry in params:
            portDict[entry[-1]] = {'ltl':entry[0],'admin':entry[1],'link':entry[2],'state':entry[3],'sgid':entry[4]}
        return portDict

    def get_vemcmd_show_port_vlans_info(self,ltl=None):
        '''
            Get relavant information by executing vemcmd show port vlans command
            if ltl is passed, we get info for that ltl, else we get for all ltl 
        '''
        portDict = {}
        cmd = 'vemcmd show port vlans'
        op = self.execute(cmd)
        #self.log.info(op)
        if ltl == None:
            params = re.findall('\s+(\d+)\s+\w+\s+(\d+)\s+(\w+)\s+(\d+)\s+(\w+)\s+(\d+)',op)
        else:
            params = re.findall('\s+({})\s+\w+\s+(\d+)\s+(\w+)\s+(\d+)\s+(\w+)\s+(\d+)'.format(ltl),op)

        for entry in params:
            portDict[entry[0]] = {'native vlan':entry[1],'vlan state':entry[2],'allowed vlans':entry[3],'encap type': entry[4], 'encap id':entry[5]}

        return portDict

    def validate_port_state(self):
        '''
            Make sure all ports are in FWD state on the current AVE host
            Does not take any parameters
        '''
        portDict = self.get_vemcmd_show_port_info() 
        ltlDict = self.get_vemcmd_show_port_vlans_info()

        flag1 = True
        flag2 = True

        for entry in portDict.values():
            if entry['state'] != 'FWD':
                flag1 = False
                self.log.info('ltl {} is in {} state' .format(entry['ltl'],entry['state']))

        
        for entry in ltlDict.keys():
            value = ltlDict[entry]
            if value['vlan state'] != 'FWD':
                flag2 = False
                self.log.info('ltl {} is in {} state' .format(entry,value['vlan state']))

        if flag1 and flag2:
            return True
        else:
            return False

    def get_vem_version_info(self):
        '''
            Get Parameters from 'vemcmd show version' command
        '''
        cmd = 'vemcmd show version'
        op = self.execute(cmd)
        self.log.info(op)
        versionDict = {}

        versionDict['vem_version'] = re.search('VEM Version:\s+(.*)',op).group(1)
        versionDict['sdk_version'] = re.search('OpFlex SDK Version:\s+(.*)',op).group(1)
        versionDict['vmware_version'] = re.search('System Version: VMware AVEi\s+(\d+\.\d+\.\d+)',op).group(1)

        return versionDict
