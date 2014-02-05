import sys
import imp
import os

class PluginManager(object):
    forceReload = False
    __instance = None

    def __new__(cls):
        if PluginManager.__instance is None or PluginManager.forceReload is True:
            PluginManager.__instance = object.__new__(cls)
            PluginManager.__instance.__init()
        return PluginManager.__instance
        
    @classmethod
    def setForceReload(cls,doForce):
        cls.forceReload = doForce

    def getModuleNamed(self, name):
        if self.forceReload:
            raise KeyError
        return sys.modules[name]

    def importModule(self,name,path):
        try:
            module = self.getModuleNamed(name)
            return module
        except KeyError:
            pass
        fp, pathname, description = imp.find_module(name, path)
        try:
            return imp.load_module(name, fp, pathname, description)
        finally:
            if fp:
                fp.close()
    
    def __init(self):
        sinzdir = os.path.dirname(os.path.dirname(__file__))
        PluginFolder=os.path.join(sinzdir,"plugins")
        possibleplugins = os.listdir(PluginFolder)
        for i in possibleplugins:
            if not i.endswith(".py") or i == "__init__.py":
                continue
            name = i[:-3]
            self.importModule(name, [PluginFolder])
        