from sinz.cli.CLI import CLI
from sinz.PluginInitException import PluginInitException
from sinz.Util import Util

class NonDebianPackageError(PluginInitException):
    def __str__(self):
        return "No correct debian/changelog found"

@CLI.mixin
class Debian(object):
    cliName=["deb"]
    def __init__(self):
        try:
            self.parseChangeLog()
        except IOError:
            raise NonDebianPackageError(self)
        
    def parseChangeLog(self):
        changelog = open("debian/changelog")
        changelogline = changelog.readline()
        self.package, fullversion, rest = changelogline.split(" ", 2)  # @UnusedVariable
        self.fullVersion = fullversion.replace("(","").replace(")","") 

    @CLI.climethod
    def getPackage(self):
        return self.package
    
    @CLI.climethod
    def getFullVersion(self):
        return self.fullVersion

    @CLI.climethod
    def getUpstreamVersion(self):
        return self.fullVersion.split("-")[0]
    
    @CLI.climethod
    def addChangelogEntry(self):
        cmdline = 'DEBEMAIL="%s" dch -v %s -b -D %s --force-distribution "automated build for %s %s"'%(
                self.debemail,
                self.version,
                self.distroname,
                self.commitid
                )
        Util.runCmd(cmdline)
    