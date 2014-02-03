from sinz.cli.CLI import CLI
import git

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
        