import glob
import re
#import sys
#sys.path.append('../')
#from Logger import Logger

class Utilities:

    def __init__(self):
        #self.log = Logger(path='/auto/AVS1/niranjan/scripts/framework/logs/')
        self.log.info('Initializing Apic Utilities Class')

    def get_apic_image(self,path):

        try:
            apic_img = glob.glob(path+'/*.iso')[0]
            self.log.info('Found Apic image {}' .format(apic_img))
        except:
            self.log.info('Unable to find Apic image in {}' .format(path))
            self.log.info('Trying in {}/final/' .format(path))
            try:
                apic_img = glob.glob(path+'/final/*.iso')[0]
                self.log.info('Found Apic image {}' .format(apic_img))
            except:
                self.log.info('Unable to find Apic image in {}/final/' .format(path))
                self.log.info('Trying in {}/gdb/' .format(path))
                try:
                    apic_img = glob.glob(path+'/gdb/*.iso')[0]
                    self.log.info('Found Apic image {}' .format(apic_img))
                except:
                    self.log.info('Unable to find Apic image in {}/gdb/' .format(path))
                    self.log.info('Apic Image was not found in regular paths.' .format(path))
                    return False

        return apic_img

    def get_switch_image(self,path):

        try:
            switch_img = (glob.glob('{}/*.bin' .format(path)) or glob.glob('{}/*.gbin' .format(path)))[0]
            self.log.info('Found Switch image {}' .format(switch_img))
        except:
            self.log.info('Unable to find Switch image in {}' .format(path))
            self.log.info('Trying in {}/final/' .format(path))
            try:
                switch_img = (glob.glob('{}/final/aci-n9000-dk9.bin' .format(path)) or glob.glob('{}/final/aci-n9000-dk9.gbin' .format(path)))[0]
                self.log.info('Found Switch image {}' .format(switch_img))
            except:
                self.log.info('Unable to find Switch image in {}/final/' .format(path))
                self.log.info('Trying in {}/gdb/' .format(path))
                try:
                    switch_img = (glob.glob('{}/gdb/aci-n9000-dk9.bin' .format(path)) or glob.glob('{}/gdb/aci-n9000-dk9.gbin' .format(path)))[0]
                    self.log.info('Found Switch image {}' .format(switch_img))
                except:
                    self.log.info('Unable to find Switch image in {}/gdb/' .format(path))
                    self.log.info('Switch Image was not found in regular paths.' .format(path))
                    return False

        return switch_img

    def uploadACIImages(self,path,host,username,password):
        '''
            Given a build directory, pick up the Apic/Leaf images and upload it to the current Apic
            arg1 - path to build directory
            arg2 - host ip or hostname
            arg3 - host username
            arg4 - host password
        '''

        apicImg = 'Apic-' + path[-6:]
        switchImg = 'Switch-' + path[-6:]

        self.uploadApicImage(path,host,username,password,apicImg)
        self.uploadSwitchImage(path,host,username,password,switchImg)
        return True

    def moquery(self,moobject):
        '''
            returns the result of moquery in a dictionary in {dn:contents} format
            arg1 : moobject, for example fvAEPg
        '''

        cmd = 'moquery -c {}' .format(moobject)
        contents = self.execute(cmd)
        op = re.split('#',contents)

        moDict = {}

        try:
            self.log.info(contents)
            for entry in op[1:]:
                objName = re.search('dn\s+:\s+(.*)',entry).group(1)
                moDict[objName] = entry
        except:
            self.log.info('Hit Exception while trying to MoQuery. Please check')
            return False

        return moDict

    def check_cores(self):
        '''
            returns apic/switch core files
        '''
        
        cmd = 'show cores'
        contents = self.execute(cmd)
        split = re.split(' Ctrlr-Id',contents)
        switch_cores,apic_cores = split[0],split[1]
        switch_cores_list = re.findall('(\d+)\s+\S+\s+\S+\s+(\d+)\s+(\w+)\s+(\d+)\s+(\S+)',switch_cores)
        #apic_cores_list = re.findall('',apic_cores)

        print switch_cores_list
        
