import time
import re
import datetime

class SpineTriggers():

    def __init__(self):

        self.log.info("Intializing API's for triggering operations on Spine") 
   
    def reboot(self,wait_time=360,poll_interval=10):
        ''' 
            Reboots Spine using 'reboot' command as root
            arg1 - wait_time specifies how long the script should wait for Spine to come up
                   default is 360 secs
            arg2 - poll_interval specifies how often the script should poll to see if Spine has come back up
                   default is 10 sec interval
        '''
        cmd = 'vsh -c "reload"'
        self.log.info("Rebooting Spine {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute_root_pexpect(cmd,delay=20)

        flag = False
        counter = wait_time
        elapsed = 0
        while counter>0:
            try:
                if not self.connect():
                    raise
                self.log.info("Spine {} came up in {} secs" .format(self.ip, elapsed))
                flag = True
                break
            except:
                self.log.error("Spine {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

        self.log.info('Sleeping for 150 secs after TOR is back from reboot')
        time.sleep(150)
        return flag

    def clean_reboot(self,wait_time=360,poll_interval=10):
        ''' 
            Clean Reboots Spine using 'touch /mnt/pss/.clean;sync;vsh -c "reload"' command as root
            arg1 - wait_time specifies how long the script should wait for Spine to come up
                   default is 360 secs
            arg2 - poll_interval specifies how often the script should poll to see if Spine has come back up
                   default is 10 sec interval
        '''
        cmd = 'touch /mnt/pss/.clean;sync;vsh -c "reload"'
        self.log.info("Clean Rebooting Spine {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute_root_pexpect(cmd)

        flag = False
        counter = wait_time
        elapsed = 0
        while counter>0:
            try:
                if not self.connect():
                    raise
                self.log.info("Spine {} came up in {} secs" .format(self.ip, elapsed))
                flag = True
                break
            except:
                self.log.error("Spine {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

        return flag
