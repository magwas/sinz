import types
from sinz.cli.Registry import Registry
from sinz.cli.PluginManager import PluginManager
import traceback
import os
from sinz.Util import Util

class CLI(object):
    def __init__(self):
        self.printcmd = os.environ.get("SINZ_DEBUG")
        PluginManager()
        if self.printcmd:
            Util.setVerbose()

    @classmethod
    def climethod(cls,fn):
        fn.cliMethod = True
        return fn
    
    @classmethod
    def mixin(cls,klass):
        registry = Registry()
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
    
    def runCmd(self, argv):
        registry = Registry()
        if self.printcmd:
            print(argv)
        return registry.runCommand(argv[1:])

    def call(self,argv):
        if(2 > len(argv)):
            self.runCmd([argv[0],"help"])
            raise SystemExit(1)
        try:
            return self.runCmd(argv)
        except Exception:
            traceback.print_exc()
            self.runCmd([argv[0],"help"])
            raise SystemExit(1)

    def main(self,argv):
        if(2 > len(argv)):
            print(self.runCmd([argv[0],"help"]))
            raise SystemExit(1)
        try:
            print(self.runCmd(argv))
        except Exception:
            traceback.print_exc()
            print(self.runCmd([argv[0],"help"]))
            raise SystemExit(1)

    def firstUseable(self,cmds):
        registry = Registry()
        for path in cmds:
            (cmd,args) = registry.getCommand(path)
            if isinstance(cmd,Exception):
                continue
            if self.printcmd:
                print(cmd, args)
            return cmd(*args)
        print("no useable module found for %s"%(cmds,))
        raise SystemExit(1)
