class RegistryRecord(dict):
    def __init__(self,fn=None):
        if None is fn:
            fn=self.listMyself
        self.fn = fn
    def listMyself(self,*args):
        return "\n".join(self.keys())
        
class Registry(object):
    __instance = None
    def __new__(cls):
        if Registry.__instance is None:
            Registry.__instance = object.__new__(cls)
            Registry.__instance.commands = RegistryRecord()
        return Registry.__instance

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

    def runCommand(self,argv):
        (cmd,args) = self.getCommand(argv)
        return cmd(*args)

    def getCommand(self,argv):
        curr = self.commands
        for i in range(len(argv)):
            key = argv[i]
            if not curr.has_key(key):
                return (curr.fn,argv[i:])
            curr = curr[key]
        return (curr.fn,[])
