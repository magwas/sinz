import tempfile
import os
from sinz.Util import Util
from sinz.cli.PluginManager import PluginManager
from sinz.cli.Registry import Registry
from sinz.cli.CLI import CLI

class TestProject(object):
    def __init__(self,initCmd = None):
        self.basepath = tempfile.mkdtemp()
        self.projectpath = os.path.join(self.basepath,"project")
        Util.runCmd("git clone . %s"%(self.projectpath,))
        self.initCmd = initCmd
        self.keep = False

    def reloadPlugins(self):
        PluginManager.setForceReload(True)
        Registry.INSTANCE = None
        self.cli = CLI()

    def __enter__(self):
        self.oldcwd = os.getcwd()
        os.chdir(self.projectpath)
        if self.initCmd:
            Util.runCmd(self.initCmd)
        self.reloadPlugins()
        return self
    
    def __exit__(self, tipe, value, traceback):
        os.chdir(self.oldcwd)
        self.reloadPlugins()
        PluginManager.setForceReload(False)
        if self.keep:
            print("keeping %s"%(self.projectpath,))
        else:
            Util.runCmd("rm -rf %s"%(self.projectpath,))
