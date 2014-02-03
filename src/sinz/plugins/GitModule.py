from sinz.cli.CLI import CLI
import git
from sinz.Util import Util

@CLI.mixin
class GitModule(object):
    cliName = ["git"]
    def __init__(self):
        self.repo=git.Repo(".")
    
    @CLI.climethod
    def getBranch(self):
        return self.repo.active_branch.name
    
    @CLI.climethod
    def getCommit(self):
        return self.repo.active_branch.commit.hexsha
    
    @CLI.climethod
    def getCommitIdentifier(self):
        return "branch %s commit %s"%(self.getBranch(),self.getCommit())

    @CLI.climethod
    def getNewTestCases(self):
        cmd = "git diff HEAD |grep '^+ *def test_' |sed 's/^.*test_//;s/_/ /g;s/(.*//'"
        return Util.cmdOutput(cmd)
        