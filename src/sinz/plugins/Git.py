from sinz.cli.CLI import CLI
import git
from sinz.Util import Util
from sinz.PluginInitException import PluginInitException
import traceback


class CannotSetUpGit(PluginInitException):
    def __str__(self):
        return "We are not in a git repo"

@CLI.mixin
class Git(object):
    cliName = ["git"]
    def __init__(self):
        self.setUpGitInstance()

    def setUpGitInstance(self):
        try:
            self.repo = git.Repo(".")
            if isinstance(self.repo.active_branch, str):
                self.branch = self.repo.active_branch
                self.commit = self.repo.commits[0].id
            self.branch = self.repo.active_branch.name.split("/")[-1]
            self.commit = self.repo.active_branch.commit.hexsha
        except:
            traceback.print_exc()
            raise(CannotSetUpGit(self))

    
    @CLI.climethod
    def getBranch(self):
        return self.branch
    
    @CLI.climethod
    def getCommit(self):
        return self.commit
    
    @CLI.climethod
    def getNewTestCases(self):
        cmd = "git diff HEAD |grep '^+ *def test_' |sed 's/^.*test_//;s/_/ /g;s/(.*//'"
        return Util.cmdOutput(cmd)
        