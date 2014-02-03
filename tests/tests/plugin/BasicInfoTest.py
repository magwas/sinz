import unittest
import os
import sinz.cli
from sinz.cli.CLI import CLI

class BasicInfoTest(unittest.TestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.cli.__file__, __file__])
        os.chdir(packetroot)

    def test_getVersion_returns_the_version_string(self):
        package = CLI().main(["test","getVersion"])
        self.assertEquals(package,"0.1")

if __name__ == "__main__":
    unittest.main()