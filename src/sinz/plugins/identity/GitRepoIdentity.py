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
