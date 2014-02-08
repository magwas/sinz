from sinz.cli.CLI import CLI
from sinz.cli.Registry import Registry
import sys

@CLI.mixin
class BasicInfo(object):
    cliName = []

    @CLI.climethod
    def getVersion(self):
        return CLI().firstUseable([
                ["autoconf", "getVersion"],
                ["deb", "getUpstreamVersion"],
            ])
    @CLI.climethod
    def getBranch(self):
        return CLI().firstUseable([
                ["drone", "getBranch"],
                ["travis", "getBranch"],
                ["git", "getBranch"],
            ])
    @CLI.climethod
    def getCommit(self):
        return CLI().firstUseable([
                ["drone", "getCommit"],
                ["travis", "getCommit"],
                ["git", "getCommit"],
            ])
    @CLI.climethod
    def getBuildId(self):
        return CLI().firstUseable([
                ["drone", "getBuildId"],
                ["travis", "getBuildId"],
            ])
    @CLI.climethod
    def getCommitIdentifier(self):
        return "branch %s commit %s"%(self.getBranch(),self.getCommit())
    
    @CLI.climethod
    def getPackage(self):
        return CLI().firstUseable([
                ["autoconf", "getPackage"],
                ["deb", "getPackage"],
            ])
    @CLI.climethod
    def complete(self,*args):
        argc = int(args[0]) + 1
        fullwords = args[2:argc]
        if argc < len(args):
            fragment = args[-1]
        else:
            fragment = ""
        ret = []
        entries = Registry().getEntry(fullwords)
        for entry in entries:
            if entry.startswith(fragment):
                ret.append(entry)
        retval = "\n".join(ret)
        return retval
