from sinz.cli.CLI import CLI
from sinz.cli.Registry import Registry
from sinz.Plugin import Plugin

class NonDebianPackageError(Exception):
    def __str__(self):
        return "This operation needs a Debian package"

@CLI.mixin
class Debian(Plugin):
    def __init__(self):
        try:
            self.parseChangeLog()
        except IOError:
            raise NonDebianPackageError
        
    def parseChangeLog(self):
        changelog = open("debian/changelog")
        changelogline = changelog.readline()
        self.package, fullversion, rest = changelogline.split(" ", 2)  # @UnusedVariable
        self.fullVersion = fullversion.replace("(","").replace(")","") 

    @Registry.climethod
    def getPackage(self):
        return self.package
    
    @Registry.climethod
    def getFullVersion(self):
        return self.fullVersion
