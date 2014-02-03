import sys
import imp
import os

class PluginManager(object):
    @staticmethod
    def importModule(name,path):
        try:
            return sys.modules[name]
        except KeyError:
            pass
        fp, pathname, description = imp.find_module(name, path)
        try:
            return imp.load_module(name, fp, pathname, description)
        finally:
            if fp:
                fp.close()
                
    @classmethod
    def getPlugins(cls):
        sinzdir = os.path.dirname(os.path.dirname(__file__))
        PluginFolder=os.path.join(sinzdir,"plugins")
        possibleplugins = os.listdir(PluginFolder)
        for i in possibleplugins:
            if not i.endswith(".py") or i == "__init__.py":
                continue
            name = i[:-3]
            cls.importModule(name, [PluginFolder])
        