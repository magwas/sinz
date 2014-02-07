from sinz.cli.CLI import CLI

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
                ["travis", "getBranch"],
                ["git", "getBranch"],
            ])
    @CLI.climethod
    def getCommit(self):
        return CLI().firstUseable([
                ["travis", "getCommit"],
                ["git", "getCommit"],
            ])
    @CLI.climethod
    def getBuildId(self):
        return CLI().firstUseable([
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
