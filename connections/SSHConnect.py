from misc import *
import paramiko
import datetime

class SSHConnect(Password):

    def __init__(self):
        self.log.info("creating new SSH Connection Object for {} {}" .format(self.devtype, self.ip))
        Password.__init__(self)

    def connect(self, override=False):
        '''
            Connects to current device 
            Returns if the connection was a success or failure
        '''
      
        if override:
            username = 'root'
            password = self.get_rootpasswd()
        else:
            username = self.username
            password = self.password
         
        try:
            self.connection_handle = paramiko.SSHClient()
            self.connection_handle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection_handle.connect(self.ip, username=username,password=password,key_filename='/dev/null',timeout=10)
            self.lastlogin = datetime.datetime.now()
            self.log.info("Successfully Established connection to {} {} at {}" .format(self.devtype,self.ip,self.lastlogin))
            return True
        except:
            self.log.error("Issue Establishing connection to {} {} at {}" .format(self.devtype,self.ip,datetime.datetime.now()))
            return False

    def disconnect(self):
        '''
            Disconnects from current device 
        '''
        try:
            self.connection_handle.close()
            self.lastlogout = datetime.datetime.now()
            self.log.info("Successfully disconnected SSH session to {} {} at {}" .format(self.devtype,self.ip,self.lastlogout))
            return True
        except:
            self.log.info("Issue encountered while trying to disconnect from {} {}" .format(self.devtype,self.ip))
            return False

    def execute(self,command,override=False):
        '''
            Connects to the device
            Executes the specified commmand
            Disconnects from the device
            arg1 - Specify the command to be executed on the device
            arg2 - Set override to True if you want to execute as root. Defaut is False
            Returns the output from command execution
        '''
        self.connect(override)
        self.log.info('Executing {} on {} at {}' .format(command,self.ip,datetime.datetime.now()))
        si,so,se = self.connection_handle.exec_command(command)
        contents = so.read()
        self.disconnect()
        self.log.info(contents)
        return contents

    def execute_root(self,cmd):
        '''
            Executes the given command as root user
        '''
        op = self.execute(cmd,override=True)
        return op
