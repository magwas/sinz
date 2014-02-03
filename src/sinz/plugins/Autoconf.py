from sinz.cli.CLI import CLI
import re
from sinz.PluginInitException import PluginInitException

class NonAutoconfPackageError(PluginInitException):
    def __str__(self):
        return "No correct configure.ac found"

@CLI.mixin
class Autoconf(object):
    cliName = ["autoconf"]

    def getAutoConfig(self):
        f = open("configure.ac")
        configure_ac = f.read()
        f.close()
        acinitline=re.search("AC_INIT.*\( *(?P<package>[^,]*), *(?P<version>[^,)]*)[^)]*\)", configure_ac)
        gd = acinitline.groupdict()
        self.version = self.unQuote(gd["version"])
        self.package = self.unQuote(gd["package"])
        return acinitline

    def __init__(self):
        try:
            self.getAutoConfig()
        except Exception as e:
            raise NonAutoconfPackageError(e)
    
    @CLI.climethod
    def getPackage(self):
        return self.unQuote(self.package)
    
    @CLI.climethod
    def getVersion(self):
        return self.unQuote(self.version)
    
    def unQuote(self,string):
        return re.sub("^\[|\]$","",string.strip())
        