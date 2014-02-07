
class InTreeIdentity(object):
    @classmethod
    def setup(cls,instance):
        instance.rebase(cls)
        return True

    def bring(self,filename):
        pass
