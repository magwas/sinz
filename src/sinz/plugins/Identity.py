import os

class GitRepoIdentity(object):
    @classmethod
    def setup(cls,instance):
        gitrepo = os.environ.get("IDENTITY_REPO")
        if gitrepo is not None:
            instance.gitrepo = gitrepo
            instance.rebase(cls)
            return True
        return False

class GitBranchIdentity(object):
    @classmethod
    def setup(cls,instance):
        gitbranch = os.environ.get("IDENTITY_BRANCH")
        if gitbranch is not None:
            instance.gitbranch = gitbranch
            instance.rebase(cls)
            return True
        return False

class InTreeIdentity(object):
    @classmethod
    def setup(cls,instance):
        instance.rebase(cls)
        return True

    def bring(self,filename):
        pass

class dummy(object):
    pass
class Identity(dummy):
    def __init__(self):
        GitRepoIdentity.setup(self) or \
        GitBranchIdentity.setup(self) or \
        InTreeIdentity.setup(self)
        
    def rebase(self, klass):
        self.__class__.__bases__ = (klass,)

        