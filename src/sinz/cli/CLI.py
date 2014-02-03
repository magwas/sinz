import types
from sinz.cli.Registry import Registry
from sinz.cli.PluginManager import PluginManager
import traceback

class CLI(object):
    def __init__(self):
        PluginManager().getPlugins()
        Registry.getInstance().addAliases([
            (["help"],["help","help"]),
            (["getBranch"],["git", "getBranch"]),
            (["getCommitIdentifier"],["git", "getCommitIdentifier"]),
            ])
    @classmethod
    def climethod(cls,fn):
        fn.cliMethod = True
        return fn
    
    @classmethod
    def mixin(cls,klass):
        registry = Registry.getInstance()
        try:
            currInstance = klass()
            initError = None
        except Exception as e:
            if not getattr(e,"instance",False):
                traceback.print_exc()
                raise(e)
            currInstance = e.instance
            initError = e
        for name in dir(currInstance):
            fn = getattr(currInstance,name)
            if isinstance(fn, types.MethodType) and getattr(fn,"cliMethod",False):
                registry.registerFunction(klass, initError, fn)
        return klass
    
    def run(self,func):
        ret = func()
        if None is not ret:
            print(ret)
        return ret
    

    def runCmd(self, argv):
        registry = Registry.getInstance()
        return self.run(registry.getCommand(argv[1:]))

    def main(self,argv):
        if(2 > len(argv)):
            self.runCmd([argv[0],"help"])
            raise SystemExit(1)
        try:
            return self.runCmd(argv)
        except Exception:
            traceback.print_exc()
            self.runCmd([argv[0],"help"])
            raise SystemExit(1)

    def firstUseable(self,cmds):
        registry = Registry.getInstance()
        for path in cmds:
            cmd = registry.getCommand(path)
            if isinstance(cmd,Exception):
                continue
            return cmd()
        print("no useable module found for %s"%(cmds,))
        raise SystemExit(1)
