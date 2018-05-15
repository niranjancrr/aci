import pexpect
import datetime
import time
from misc import *

class SSHConnectPExpect(Password):

    promptList = [
                'yes\/no\)\? $',
                'password:$',
                'Password:$',
                'Password: $',
                '# $',
                '#$',
                'no route',
                'not resolve',
                '# ',
                'assword:',
                '#'
            ]

    def __init__(self):
        self.log.info("creating new PExpect SSH Connection Object for {} {}" .format(self.devtype, self.ip))

    def pexpect_connect(self, override=False):
        '''
            Connect to current device using pexpect
        '''

        if override:
            username = 'root'
            password = self.get_rootpasswd()
        else:
            username = self.username
            password = self.password

        try:

            cmd='ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {0}@{1}'.format(username, self.ip)
            self.connection_handle=pexpect.spawn(cmd, timeout=10)
            time.sleep(2)

            done = False
            while not done:
                i=self.connection_handle.expect(self.promptList)
                if i == 0:
                    # RSA Key update prompt
                    #print 'sending "yes"'
                    self.connection_handle.sendline('yes')
                    output = self.connection_handle.before
                if i == 1 or i == 2 or i == 3 or i == 9:
                    # In Password prompt
                    #print 'sending %s' % password
                    self.connection_handle.sendline(password)
                    output = self.connection_handle.before
                if i == 4 or i == 8 or i == 10:
                    # Login to device success
                    self.connection_handle.sendline()
                    self.connection_handle.expect(['# $', '#$' , '()# ', '# ', '#'])
                    output = self.connection_handle.before
                    done = True
                if i == 5 :
                    self.log.error('No Route to Host')
                    return None 
                if i == 6:
                    self.log.error('Cannot resolve hostname')
                    return None

            self.log.info("Successfully Established connection to {} {} at {}" .format(self.devtype,self.ip,self.lastlogin))
            return True
        except:
            self.log.error("Issue Establishing connection to {} {} at {}" .format(self.devtype,self.ip,datetime.datetime.now()))
            return False

    def pexpect_disconnect(self):
        '''
            Disconnect from current device
        '''
        try:
            self.connection_handle.close()
            self.lastlogout = datetime.datetime.now()
            self.log.info("Successfully disconnected SSH session to {} {} at {}" .format(self.devtype,self.ip,self.lastlogout))
            return True
        except:
            return False

    '''
    def pexpect_execute(self,command):
        # 
        #    Execute Specified Command
        #
        output = ''
        self.connection_handle.sendline(command)
        done = False
        while not done:
            i= self.connection_handle.expect(self.promptList, 10)
            if i == 0:
                self.connection_handle.sendline('R')
                output = output + self.connection_handle.before
            else:
                output = output + self.connection_handle.before
                done = True

        self.log.info(output)
        return output
    '''

    def pexpect_execute(self,command,override=False,delay=0):
        '''
            Connect to Device using pexpect
            Execute Specified Command
            Disconnect from Device
            arg1 - Specify the command to be executed on the device
            arg2 - Set override to True if you want to execute as root. Defaut is False
        '''
        output = ''
        self.pexpect_connect(override)
        self.log.info('Executing {} on {} at {}' .format(command,self.ip,datetime.datetime.now()))
        self.connection_handle.sendline(command)
        if delay > 0:
            self.log.info('Sleeping for {} secs after command execution' .format(delay))
            time.sleep(delay)
        done = False
        while not done:
            try:
                i= self.connection_handle.expect(self.promptList, 10)
            except:
                self.log.info('Unable to connect to device {} after executing {}' .format(self.ip,command))
                self.pexpect_disconnect()
                return True
            if i == 0:
                self.connection_handle.sendline('R')
                output = output + self.connection_handle.before
            else:
                output = output + self.connection_handle.before
                output = output + self.connection_handle.after
                done = True
        self.pexpect_disconnect()
        self.log.info(output)
        return output

    def pexpect_execute_only(self,command,override=False):
        '''
            Connect to Device using pexpect
            Execute Specified Command
            Disconnect from Device
            arg1 - Specify the command to be executed on the device
            arg2 - Set override to True if you want to execute as root. Defaut is False
        '''
        output = ''
        self.log.info('Executing {} on {} at {}' .format(command,self.ip,datetime.datetime.now()))
        self.pexpect_connect(override)
        self.connection_handle.sendline(command)
        self.pexpect_disconnect()
        return True

    def execute_root_pexpect(self,cmd,delay=0):
        '''
            Executes the given command as root using pexpect
            arg1 - Specify the command which has to be executed on the device
        '''
        op = self.pexpect_execute(cmd,override=True,delay=delay)
        return op
