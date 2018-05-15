import time
import re
import datetime

class AVETriggers():

    def __init__(self):
        self.log.info("Intializing API's for triggering operations on AVE host")


    def reboot(self,wait_time=360,poll_interval=10):
        ''' 
            Reboots esx using 'reboot -f' command
            arg1 - wait_time specifies how long the script should wait for AVE to come up
                   default is 360 secs
            arg2 - poll_interval specifies how often the script should poll to see if AVE has come back up
                   default is 10 sec interval
        ''' 
        cmd = 'reboot -f'
        self.log.info("Rebooting AVE {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute(cmd) 

        counter = wait_time
        elapsed = 0
        while counter:
            try:
                if not self.connect():
                    raise
                self.log.info("AVE {} came up in {} secs" .format(self.ip, elapsed))
                break
            except:
                self.log.error("AVE {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

    def vem_restart(self,wait_time=30,poll_interval=5):
        ''' 
            Restarts VEM on AVE using 'vem restart' command
            arg1 - wait_time specifies how long the script should wait for AVE to come up
                   default is 30 secs
            arg2 - poll_interval specifies how often the script should poll to see if AVE has come back up
                   default is 5 sec interval
        '''
        cmd = 'vem restart'
        self.log.info("Restarting VEM on AVE {} at {}" .format(self.ip,datetime.datetime.now()))
        self.contents = self.execute(cmd)

        counter = wait_time
        elapsed = 0
        while counter:
            try:
                if not self.connect():
                    raise
                self.log.info("AVE {} came up in {} secs" .format(self.ip, elapsed))
                break
            except:
                self.log.error("AVE {} did not come up in {} secs" .format(self.ip, elapsed))
                self.log.info("Sleeping for {} secs" .format(poll_interval))
                time.sleep(poll_interval)
                elapsed += poll_interval
                counter -= poll_interval

