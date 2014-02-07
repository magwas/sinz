import subprocess
class CmdRunException(Exception):
    pass

class Util(object):
    verbose = False
    @classmethod
    def cmdOutput(cls, cmd, havepassword = False):
        if cls.verbose and not havepassword:
            print(cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if (0 != proc.returncode):
            raise CmdRunException((cmd,proc.stderr.read()))
        output = proc.stdout.read().strip()
        return output

    
    @classmethod
    def runCmd(cls, cmd,  havepassword = False):
        if cls.verbose and not havepassword:
            print(cmd)
        p = subprocess.call(cmd, shell=True)
        if (0 != p):
            raise CmdRunException(cmd)

    
    @classmethod
    def setVerbose(cls):
        cls.verbose = True
    
    
    
    

        