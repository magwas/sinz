import types
from sinz.cli.Registry import Registry
from sinz.cli.PluginManager import PluginManager
import traceback

class CLI(object):
    def __init__(self):
        PluginManager().getPlugins()
        Registry.getInstance().addAliases([
            (["help"],["help","help"])
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
            print(e)
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
        registry = Registry.getInstance()
        if(2 > len(argv)):
            self.run(registry.getCommand(["help"]))
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
            return cmd()
    

