from sinz.plugins.identity.GitRepoIdentity import GitRepoIdentity
from sinz.plugins.identity.GitBranchIdentity import GitBranchIdentity
from sinz.plugins.identity.InTreeIdentity import InTreeIdentity
from sinz.plugins.identity.SshIdentity import SshIdentity

class dummy(object):
    pass
class Identity(dummy):
    def __init__(self):
        GitRepoIdentity.setup(self) or \
        GitBranchIdentity.setup(self) or \
        SshIdentity.setup(self) or \
        InTreeIdentity.setup(self)
        
    def rebase(self, klass):
        self.__class__.__bases__ = (klass,)

        