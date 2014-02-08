from sinz.cli.CLI import CLI
from sinz.PluginInitException import PluginInitException
from sinz.Util import Util
import os
from sinz.plugins.Identity import Identity

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
        if os.environ.has_key("DEB_REPO_FOR_EACH_BRANCH"):
            self.repoForEachBranch = True
        else:
            self.repoForEachBranch = False
        
    def parseChangeLog(self):
        changelog = open("debian/changelog")
        changelogline = changelog.readline()
        self.package, fullversion, distro, rest = changelogline.split(" ", 3)  # @UnusedVariable
        self.fullVersion = fullversion.replace("(","").replace(")","")
        self.changelogEmail = self.getDebEmailFromChangelog()
        self.distro = distro.strip()[:-1]
        
    def getDebEmailFromChangelog(self):
        cmd = """cat debian/changelog |grep "^ -- "|head -1 |sed 's/^ -- //;s/  .*//'"""
        return Util.cmdOutput(cmd)
   
    @CLI.climethod
    def submit(self):
        cli = CLI()
        Identity().bring("dput.cf")
        branch = cli.call(["addChangelogEntry", "getBranch"])
        if branch == "master" or self.repoForEachBranch:
            repo = branch
        else:
            repo = "nonmaster"
            
        pkgname = "%s_%s"%(self.package,self.fullVersion)
        cmd = "dput -c dput.cf %s ../%s_source.changes"%(repo, pkgname)
        return Util.runCmd(cmd)

    @CLI.climethod
    def getPackage(self):
        return self.package
    
    @CLI.climethod
    def sourceBuild(self):
        cmd = "echo y |debuild -us -uc -S"
        return Util.runCmd(cmd)
    
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
    def addChangelogEntry(self, *args):
        cli = CLI()
        version = cli.call(["addChangelogEntry", "getVersion"])
        branch = cli.call(["addChangelogEntry", "getBranch"])
        if(len(args)):
            distro = args[0] 
        else:
            distro = branch
        commitid = cli.call(["addChangelogEntry", "getCommitIdentifier"])
        buildid = cli.call(["addChangelogEntry", "getBuildId"])
        fullversion="%s-%s%s"%(version,buildid,branch)
        cmdline = 'DEBEMAIL="%s" dch -v %s -b -D %s --force-distribution "automated build for commit %s"'%(
                self.getDebEmail(),
                fullversion,
                distro,
                commitid,
                )
        Util.runCmd(cmdline)
        self.parseChangeLog()
        return cmdline
    
    @CLI.climethod
    def buildAndDput(self, *args):
        cli = CLI()
        cli.call(["deb buildAndOutput","deb","addChangelogEntry"]+list(args))
        cli.call(["deb buildAndOutput","deb","sourceBuild"])
        cli.call(["deb buildAndOutput", "gpg", "debSign"])
        cli.call(["deb buildAndOutput","deb","submit"])
