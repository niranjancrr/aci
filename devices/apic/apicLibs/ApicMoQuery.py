import re

class MoQuery():

    def __init__(self):
        self.log.info('Initializing MoQuery Class')

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
            
            
        
        
