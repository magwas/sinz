
import unittest
from sinz.cli.PluginManager import PluginManager
from sinz.cli.Registry import Registry

class Test(unittest.TestCase):

    def testRegistry(self):
        PluginManager.getPlugins()
        registry = Registry.getInstance()
        self.assertTrue(registry.commands.has_key("deb"))
        self.assertTrue(registry.commands["deb"].has_key("getPackage"))

if __name__ == "__main__":
    unittest.main()