
import unittest
from sinz.cli.Registry import Registry
from tests.TestProject import TestProject

class Test(unittest.TestCase):

    def testRegistry(self):
        with TestProject():
            registry = Registry.getInstance()
            self.assertTrue(registry.commands.has_key("deb"))
            self.assertTrue(registry.commands["deb"].has_key("getPackage"))

if __name__ == "__main__":
    unittest.main()