
import unittest
from sinz.cli.CLI import CLI
import re
import os
import sinz.Plugin

class Test(unittest.TestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.Plugin.__file__, __file__])
        os.chdir(packetroot)

    def test_help_returns_a_help(self):
        helpstring = CLI().help()
        self.assertTrue(re.search("^help :", helpstring, re.MULTILINE))
        self.assertTrue(re.search("^getPackage :", helpstring, re.MULTILINE))
        self.assertTrue(re.search("^getFullVersion :", helpstring, re.MULTILINE))
        
    def test_command_can_be_run_through_main(self):
        answer = CLI().main(["called from test","getPackage"])
        self.assertEquals("sinz", answer)
        
    def test_with_no_command_we_get_help(self):
        helpstring = CLI().main(["called from test","help"])
        self.assertTrue(re.search("^help :", helpstring, re.MULTILINE))

if __name__ == "__main__":
    unittest.main()