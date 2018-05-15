import time
import re
import datetime

class ApicTriggers():

    def __init__(self):

        self.log.info("Intializing API's for triggering operations on Apic") 
   
    def reboot(self,wait_time=360,poll_interval=10):
        ''' 
            Reboots Apic using 'reboot' command as root
            arg1 - wait_time specifies how long the script should wait for Apic to come up
                   default is 360 secs
            arg2 - poll_interval specifies how often the script should poll to see if Apic has come back up
                   default is 10 sec interval
        '''
        cmd = 'reboot'
        self.log.info("Rebooting Apic {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute_root(cmd)

        flag = False
        counter = wait_time
        elapsed = 0
        while counter>0:
            try:
                if not self.connect():
                    raise
                self.log.info("Apic {} came up in {} secs" .format(self.ip, elapsed))
                flag = True
                break
            except:
                self.log.error("Apic {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

        return flag

    def clean_reboot(self,wait_time=360,poll_interval=10):
        ''' 
            Clean Reboots Apic using 'touch /data/.clean;sync;reboot' command as root
            arg1 - wait_time specifies how long the script should wait for Apic to come up
                   default is 360 secs
            arg2 - poll_interval specifies how often the script should poll to see if Apic has come back up
                   default is 10 sec interval
        '''
        cmd = 'touch /data/.clean;sync;reboot'
        self.log.info("Clean Rebooting Apic {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute_root(cmd)

        flag = False
        counter = wait_time
        elapsed = 0
        while counter>0:
            try:
                if not self.connect():
                    raise
                self.log.info("Apic {} came up in {} secs" .format(self.ip, elapsed))
                flag = True
                break
            except:
                self.log.error("Apic {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

        return flag
