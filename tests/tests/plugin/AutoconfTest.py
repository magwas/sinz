import unittest
from sinz.cli.CLI import CLI
import os
import sinz.cli

class AutoconfTest(unittest.TestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.cli.__file__, __file__])
        os.chdir(packetroot)

    def test_autoconf_getPackage_returns_the_package_name(self):
        package = CLI().call(["test","autoconf","getPackage"])
        self.assertEquals(package,"sinz")

    def test_autoconf_getVersion_returns_the_package_version(self):
        package = CLI().call(["test","autoconf","getVersion"])
        self.assertEquals(package,"0.1")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()