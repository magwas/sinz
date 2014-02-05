from sinz.cli.CLI import CLI
import git
from sinz.Util import Util
import os

@CLI.mixin
class Git(object):
    cliName = ["git"]
    def __init__(self):
        self.repo=git.Repo(".")
    
    @CLI.climethod
    def getBranch(self):
        return self.repo.active_branch.name.split("/")[-1]
    
    @CLI.climethod
    def getCommit(self):
        return self.repo.active_branch.commit.hexsha
    
    @CLI.climethod
    def getNewTestCases(self):
        cmd = "git diff HEAD |grep '^+ *def test_' |sed 's/^.*test_//;s/_/ /g;s/(.*//'"
        return Util.cmdOutput(cmd)
        