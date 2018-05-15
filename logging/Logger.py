import logging
from logging.handlers import RotatingFileHandler
import os
import stat
import sys
import re
import inspect

'''
Author : Niranjan Raamanujan

Logger Levels
    1 DEBUG    : Detailed info
    2 INFO     : Confirmation that things are going according to plan
    3 WARNING  : Something unexpected has occured
    4 ERROR    : Some function failed
    5 CRITICAL : something failed, application must close
'''

if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class Logger():

    '''
    Constructor
        loggername : The logger name to isolate logger info between Modules.
        filename   : The filename onto which logs are written to.
        screen     : Enabling this flag will print Logs to screen.
        level      : This attribute will set the debug level. 
                           logging.DEBUG will print all logs.
    '''

    def __init__(self,loggername='App',filename='logfile.log',path ='/tmp/', screen=True,level=logging.WARNING):

        level = logging.DEBUG
        try:
            #path = '/home/app/log'
            filepath = path + '/' + filename

            #Make sure file path is accessible
            pathAccess = self.path_accessibility(path)
            if not pathAccess:
                raise('Given path was not accessible')

            #Make sure file path has enough space to log messages, default is 90% usage
            pathSpace = self.space_constraints(path)
            if not pathSpace:
                raise('Given path did not have enough space to log information')

            #Make sure file exists in the path
            fileExistance = self.file_existance(filepath)

            #If file doesn't exist, try creating it and assign it necessary permissions
            if not fileExistance:
                createFile = self.create_file(filepath)
                if not createFile:
                    raise('Unable to create file. Please check if directory has write permissions')
                fileExistance = self.file_existance(filepath)

            #Make sure file has the right permissions
            filePermissions = self.file_permissions(filepath)

            #Logger starts here
            if pathAccess and fileExistance and filePermissions:
  
                self.screen = screen
                
                #This step is used to display the file/method/line that called logger methods
                #func = inspect.currentframe().f_back.f_code
                #format = '%(thread)d||%(asctime)s||%(levelname)s||%(message)s||' + '{}||{}||{}' .format(func.co_filename,func.co_name,func.co_firstlineno)
                #format = '%(thread)d||%(asctime)s||%(levelname)s||%(message)s||'
                format = '%(thread)d||%(asctime)s||%(levelname)s||%(message)s||%(filename)s||%(funcName)s||%(lineno)d'

                self.logger = logging.getLogger(loggername)
                self.logger.name = loggername

                #Makes sure Logger instance is called only once.
                if not getattr(self.logger, 'handler_set', None):

                    # add a rotating handler
                    handler = RotatingFileHandler(filepath, maxBytes=2000000,
                                  backupCount=10)
                    formatter = logging.Formatter(format)

                    handler.setFormatter(formatter)
                    self.logger.addHandler(handler) 
                    self.logger.setLevel(level)
                    self.logger.handler_set = True

            else:

                print "CRITICAL :: Please fix errors and try running again"
                sys.exit(0)

        except:

            print "CRITICAL :: Please fix errors and try running again"
            sys.exit(0)
            
    #Debug level logs
    def debug(self,msg, *args, **kwargs):

        #if self.logger.isEnabledFor(DEBUG):
        self._log(logging.DEBUG, msg, *args, **kwargs)
        #self.logger.debug(msg)
        if self.screen:
            print msg

    #Info level logs
    def info(self,msg, *args, **kwargs):

        #if self.logger.isEnabledFor(INFO):
        self._log(logging.INFO, msg, args, **kwargs)
        #self.logger.info(msg)
        if self.screen:
            print msg

    #Warning level logs 
    def warning(self,msg, *args, **kwargs):

        #if self.logger.isEnabledFor(WARNING):
        self._log(logging.WARNING, msg, args, **kwargs)
        #self.logger.warning(msg)
        if self.screen:
            print msg

    #Error Level logs
    def error(self,msg, *args, **kwargs):
   
        #if self.logger.isEnabledFor(ERROR):
        self._log(logging.ERROR, msg, args, **kwargs)
        #self.logger.error(msg)
        if self.screen:
            print msg

    #Critical Level logs
    def critical(self,msg, *args, **kwargs):
 
        #if self.logger.isEnabledFor(CRITICAL):
        self._log(logging.CRITICAL, msg, args, **kwargs)
        #self.logger.critical(msg)
        if self.screen:
            print msg

    #Check if the given path is accessible
    def path_accessibility(self,path):
    
        if os.path.exists(path):
            return True
        else:
            print "CRITICAL :: Given path {} is inaccessible" .format(path)
            return False

    #Check if file exists in the specified path
    def file_existance(self,filepath):

        if os.path.exists(filepath):
            return True
        else:
            print "CRITICAL :: File {} does not exist" .format(filepath)
            return False

    #Create file 
    def create_file(self,filepath):

        print "INFO :: Attempting to create {} " .format(filepath)
        try:
            hd = open(filepath,'w+')
            hd.close()
            os.chmod(filepath,0o777)
            if os.path.exists(filepath):
                print "SUCCESS :: File {} was created successfully" .format(filepath)
            return True
        except:
            print "CRITICAL :: Create file {} failed" .format(filepath)
            return False

    #Check if there is anough space to log information
    def space_constraints(self,path,threshold=90):

        op = os.popen('df -h ' + path).read()
        usage = int(re.search('\s+(\d+)%.*',op).group(1))
        if usage > threshold:
            print "CRITICAL :: Given path {} does NOT have enough space to log information" .format(path)
            return False
        return True

    #Check if the file has write permissions
    def file_permissions(self,filepath):

        if os.access(filepath,os.W_OK):
            return True
        else:
            print "CRITICAL :: Given file {} does not have write permissions" .format(filepath)
            return False

    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.logger.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)


    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        # Add wrapping functionality here.
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller throws an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.logger.makeRecord(
            self.logger.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.logger.handle(record)


    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = logging.currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

#def main():

#    Log = Logger()
#    Log.debug('Sample Debug Line')
#    Log.info('Sample Info Line')
#    Log.warning('Sample Warning Line')
#    Log.error('Sample Error Line')
#    Log.critical('Sample Critical Line')

#if __name__ == '__main__':
#    main()


