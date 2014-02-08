import os
import subprocess
from sinz.Util import Util
import tempfile
import sys
class SshIdentity(object):

    @classmethod
    def testConnect(cls, identityaccount, instance):
        tempdir= tempfile.mkdtemp()
        envfile = "%s/environment"%(tempdir,)
        cls.sftp_args = os.environ.get("SFTP_ARGS", "")
        proc = subprocess.Popen("sftp -v %s %s:environment %s" % (cls.sftp_args, identityaccount, envfile), shell=True, stdout=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            instance.rebase(cls)
            #instance.env={}
            with open(envfile) as envfile:
                for line in envfile:
                    if "=" in line:
                        k,v = line.split("=")
                        os.environ[k.strip()] = v.strip()
            return True
        return False

    @classmethod
    def setup(cls,instance):
        identityaccount = os.environ.get("IDENTITY_ACCOUNT")
        if identityaccount and cls.testConnect(identityaccount,instance):
            cls.identityaccount = identityaccount
            return True
        return False

    def bring(self,filename):
        Util.runCmd("sftp %s:%s %s"%(self.identityaccount, filename, filename))
