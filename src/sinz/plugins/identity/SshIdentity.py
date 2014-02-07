import os
import subprocess
from sinz.Util import Util
class SshIdentity(object):

    @classmethod
    def testConnect(cls, identityaccount):
        proc = subprocess.Popen("ssh %s" % identityaccount, stdout=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            return True
        return False

    @classmethod
    def setup(cls,instance):
        identityaccount = os.environ.get("IDENTITY_ACCOUNT")
        if identityaccount and cls.testConnect(cls, identityaccount):
            instance.rebase(cls)
            cls.identityaccount = identityaccount
        return False

    def bring(self,filename):
        Util.runCmd("scp %s:%s %s"%(self.identityaccount, filename, filename))
