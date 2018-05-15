import re
import time

class TorValidate:

    def __init__(self):
        self.log.info("Intializing API's for TOR show command Validations")

    def get_vtep_endpoint_pairs(self):
        cmd = "show system internal epm endpoint all vtep"
        op = self.execute(cmd)
        macs = re.findall('MAC : (.*) :::',op)
        ips = re.findall('IP# 0 : (\d+.\d+.\d+.\d+) :::',op)
        endpoint_pairs = zip(macs,ips) 
        return endpoint_pairs

    def get_tunnel_ips(self):
        cmd = '''vsh_lc -c "show system internal eltmc info interface brief tunnel" | grep " vxlan" | awk '{print $5}' '''
        op = self.execute(cmd)
        ips = op.strip().split('\n')
        return ips
       
    def get_endpoint_ips(self):
        cmd = '''show system internal epm endpoint all | grep "IP# 0 :" ''' 
        op = self.execute(cmd)
        ips = re.findall('(\d+\.\d+\.\d+\.\d+)',op)
        return ips
