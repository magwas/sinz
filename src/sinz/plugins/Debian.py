from sinz.cli.CLI import CLI
from sinz.PluginInitException import PluginInitException
from sinz.Util import Util
import os

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
        if os.environ.has_key("DEBEMAIL"):
            self.changelogEmail = os.environ["DEBEMAIL"]
        
    def parseChangeLog(self):
        changelog = open("debian/changelog")
        changelogline = changelog.readline()
        self.package, fullversion, rest = changelogline.split(" ", 2)  # @UnusedVariable
        self.fullVersion = fullversion.replace("(","").replace(")","")
        self.changelogEmail = self.getDebEmailFromChangelog()
        
    def getDebEmailFromChangelog(self):
        cmd = """cat debian/changelog |grep "^ -- "|head -1 |sed 's/^ -- //;s/  .*//'"""
        return Util.cmdOutput(cmd)
    
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
    def getDebEmail(self):
        return self.changelogEmail
    
    @CLI.climethod
    def addChangelogEntry(self):
        cli = CLI()
        version = cli.main(["addChangelogEntry", "getVersion"])
        branch = cli.main(["addChangelogEntry", "getBranch"])
        commitid = cli.main(["addChangelogEntry", "getCommitIdentifier"])
        buildid = cli.main(["addChangelogEntry", "getBuildId"])
        fullversion="%s-%s%s"%(version,buildid,branch)
        cmdline = 'DEBEMAIL="%s" dch -v %s -b -D %s --force-distribution "automated build for commit %s"'%(
                self.getDebEmail(),
                fullversion,
                branch,
                commitid,
                )
        print(cmdline)
        #Util.runCmd(cmdline)
        return cmdline
    