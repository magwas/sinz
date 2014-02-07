from sinz.cli.CLI import CLI
import os
from sinz.PluginInitException import PluginInitException
from sinz.Util import Util
from sinz.plugins.Identity import Identity

class CannotSetUpGpg(PluginInitException):
    def __str__(self):
        return "you have to set up the PGPASSWORD environment variable and provide a gpg key"

@CLI.mixin
class Gpg(object):
    cliName=["gpg"]
    def __init__(self):
        self.pgpassword=os.environ.get("PGPASSWORD")
        self.pgpkey=os.environ.get("PGPKEY")
        if (self.pgpassword is None) or (self.pgpkey is None):
            raise(CannotSetUpGpg(self))
        Identity().bring(".gpg.key")  # @UndefinedVariable
        Util.runCmd('gpg --import .gpg.key||echo ""')

    @CLI.climethod
    def debSign(self):
        pgkname = CLI().call(["debSign", "getPackage"])
        fullversion = CLI().call(["debSign", "deb", "getFullVersion"])
        cmd = 'debsign -p"gpg --batch --passphrase %s" ../%s_%s_source.changes'%(
                        self.pgpassword, pgkname, fullversion)
        Util.runCmd(cmd, havepassword=True)

    @CLI.climethod
    def sign(self,filename):
        cmd = 'gpg --batch --default-key %s -a --passphrase %s --sign %s'%(
                        self.pgpkey, self.pgpassword, filename)
        Util.runCmd(cmd, havepassword=True)
