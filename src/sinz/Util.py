import subprocess
class CmdRunException(Exception):
    pass

class Util(object):
    @staticmethod
    def cmdOutput(cmd):
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if (0 != proc.returncode):
            raise CmdRunException((cmd,proc.stderr.read()))
        output = proc.stdout.read().strip()
        return output

    
    @classmethod
    def runCmd(cls, cmdline):
        p = subprocess.call(cmdline, shell=True)
        if (0 != p):
            raise CmdRunException(cmdline)
    
    

        