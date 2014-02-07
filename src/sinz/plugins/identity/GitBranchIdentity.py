import os

class GitBranchIdentity(object):
    @classmethod
    def setup(cls,instance):
        gitbranch = os.environ.get("IDENTITY_BRANCH")
        if gitbranch is not None:
            instance.gitbranch = gitbranch
            instance.rebase(cls)
            return True
        return False
