import os
import BeautifulSoup

class Password():

    def __init__(self):
        self.log.info("Initializing password object for {} {}" .format(self.devtype,self.ip))

    def get_dbgtoken(self):

        cmd = 'acidiag dbgtoken'
        self.token = self.execute(cmd).strip()
        self.log.info("Debug Token was {}" .format(self.token))

        return self.token

    def get_rootpasswd(self):
 
        self.token = self.get_dbgtoken() 
        contents = os.popen('curl http://git.insieme.local/cgi-bin/generateRootPassword.py?key=%s' %(self.token)).read()
        soup = BeautifulSoup.BeautifulSoup(contents)
        self.root_passwd = str(soup.find('code').text)
        self.log.info("Root password is {}" .format(self.root_passwd))
        return self.root_passwd
