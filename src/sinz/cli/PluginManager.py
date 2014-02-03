import sys
import imp
import os

class PluginManager(object):
    forceReload = False
    @classmethod
    def setForceReload(cls,doForce):
        cls.forceReload = doForce
    def getModuleNamed(self, name):
        if self.forceReload:
            raise KeyError
        return sys.modules[name]

    def importModule(self,name,path):
        try:
            return self.getModuleNamed(name)
        except KeyError:
            pass
        fp, pathname, description = imp.find_module(name, path)
        try:
            return imp.load_module(name, fp, pathname, description)
        finally:
            if fp:
                fp.close()
                
    def getPlugins(self):
        sinzdir = os.path.dirname(os.path.dirname(__file__))
        PluginFolder=os.path.join(sinzdir,"plugins")
        possibleplugins = os.listdir(PluginFolder)
        for i in possibleplugins:
            if not i.endswith(".py") or i == "__init__.py":
                continue
            name = i[:-3]
            self.importModule(name, [PluginFolder])
        