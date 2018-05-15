import os,re,sys,time
import BeautifulSoup
from Logger import Logger

class Topology():

    def __init__(self,setup_name,path='/auto/AVS1/AVS_TOPOS/'):

        self.log = Logger()
        self.setup_name = setup_name
        self.populate_infra(path)

    def __repr__(self):
        return '<topo-{}>' .format(self.setup_name)

    def __call__(self):
        self.log.info(self.apics)
        self.log.info(self.leaves)
        self.log.info(self.spines)

    def populate_infra(self,path):

        self.contents = self.read_topology_file(path)
        self.apics = self.get_apic_info()
        self.leaves = self.get_leaf_info()
        self.spines = self.get_spine_info()

        self.multiprint('=',50)
        self.log.info("Populated the following info from Topology File")
        self.multiprint('=',50)
        self.log.info("Primary Apic Info: \n {}" .format(self.primaryApic))
        self.multiprint('=',50)
        self.log.info("All Apic Info: \n {}" .format(self.apics))
        self.multiprint('=',50)
        self.log.info("All Leaf Info: \n {}" .format(self.leaves))
        self.multiprint('=',50)
        self.log.info("All Spine Info: \n {}" .format(self.spines))
        self.multiprint('=',50)

    def read_topology_file(self,path):
        
        try:
            #path = '/auto/AVS1/AVS_TOPOS/'
            file = path + self.setup_name + '-topology.xml'
            try:
                file_desc = open(file,'r')
            except:
                path = '/local/nraamanu/'
                file = path + self.setup_name + '-topology.xml'
                file_desc = open(file,'r')

            file_contents = file_desc.read()
            soup = BeautifulSoup.BeautifulSoup(file_contents)
            return soup
        except:
            self.log.info("Issue accessing Setup {} topology file." .format(self.setup_name))

    def get_apic_info(self):

        apicDict = {}
        self.primaryApic = {}

        hw_devices = self.contents.findAll("hw_device")
        for device in hw_devices:
            try:
                re.search('ifc1|apic1',str(device.get('name'))).group()
                ip = re.search("(\d+\.\d+\.\d+\.\d+)",str(device.get("ip"))).group(1)
                dname = str(device.get("name"))
                apicDict[dname]=(ip)
                self.primaryApic[dname]=(ip)
            except:
                try:
                    re.search('ifc|apic',str(device.get('name'))).group()
                    ip = re.search("(\d+\.\d+\.\d+\.\d+)",str(device.get("ip"))).group(1)
                    dname = str(device.get("name"))
                    apicDict[dname]=(ip)
                except:
                    continue

        return apicDict 

    def get_leaf_info(self):

        leafDict = {}

        hw_devices = self.contents.findAll("hw_device")
        for device in hw_devices:
            try:
                re.search('leaf',str(device.get('name'))).group()
                ip = re.search("(\d+\.\d+\.\d+\.\d+)",str(device.get("ip"))).group(1)
                dname = str(device.get("name"))
                s_no = str(device.get('serial-num'))
                if s_no == 'None':
                    raise
                leafDict[dname]=(ip,s_no)
            except:
                continue

        return leafDict

    def get_spine_info(self):

        spineDict = {}

        hw_devices = self.contents.findAll("hw_device")
        for device in hw_devices:
            try:
                re.search('spine',str(device.get('name'))).group()
                ip = re.search("(\d+\.\d+\.\d+\.\d+)",str(device.get("ip"))).group(1)
                dname = str(device.get("name"))
                s_no = str(device.get('serial-num'))
                if s_no == 'None':
                    raise
                spineDict[dname]=(ip,s_no)
            except:
                continue

        return spineDict

    def multiprint(self,pattern,repetitions):

        self.log.info(pattern * repetitions)


def main():
    setup = Testbed_Topology('orion4')

if __name__ == '__main__':
    main()
