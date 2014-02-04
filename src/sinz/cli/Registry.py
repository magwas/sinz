class RegistryRecord(dict):
    def __init__(self,fn=None):
        if None is fn:
            fn=self.listMyself
        self.fn = fn
    def listMyself(self):
        return "\n".join(self.keys())
        
class Registry(object):
    INSTANCE = None
    def __init__(self):
        self.commands = RegistryRecord()
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls()
        return cls.INSTANCE
    
    def registerFunction(self, klass, initError, fn):
        cmdpath = getattr(klass,"cliName",[klass.__name__])
        group = self.getEntry(cmdpath, True)
        cmdname = fn.__name__
        if initError:
            group[cmdname] = RegistryRecord(initError)
        else:
            group[cmdname] = RegistryRecord(fn)

    def getEntry(self, argv, create=False):
        curr = self.commands
        for i in argv:
            if not curr.has_key(i) and create:
                curr[i] = RegistryRecord()
            curr = curr[i]
        return curr

    def getCommand(self,argv):
        curr = self.getEntry(argv)
        return curr.fn
