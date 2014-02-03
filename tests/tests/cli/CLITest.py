
import unittest
import re
import os
import sinz.PluginInitException
from sinz.cli.CLI import CLI
import sys
from StringIO import StringIO

class Test(unittest.TestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.PluginInitException.__file__, __file__])
        os.chdir(packetroot)
        self.cli=CLI()

    def test_The_help_command_gives_a_help(self):
        helpstring = self.cli.main(["called from test","help","help"])
        self.assertTrue(re.search("^help :", helpstring, re.MULTILINE))
        self.assertTrue(re.search("^deb :", helpstring, re.MULTILINE))
        
    def test_Command_can_be_run_through_main(self):
        answer = self.cli.main(["called from test","deb","getPackage"])
        self.assertEquals("sinz", answer)
        
    def test_With_no_command_we_get_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test"])
        self.assertTrue(re.search("^help :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout
        
    def test_Nonsense_commands_give_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test", "foo", "bar"])
        self.assertTrue(re.search("^help :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout

if __name__ == "__main__":
    unittest.main()