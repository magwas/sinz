
import unittest
import re
import os
import sinz.PluginInitException
from sinz.cli.CLI import CLI
import sys
from StringIO import StringIO
from tests.TestProject import TestProject

class CLITest(unittest.TestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.PluginInitException.__file__, __file__])
        os.chdir(packetroot)
        self.cli=CLI()

    def test_The_help_command_gives_a_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test", "help", "help"])
        self.assertTrue(re.search("^getCommitIdentifier :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout
        
    def test_Command_can_be_run_through_call(self):
        answer = self.cli.call(["called from test","deb","getPackage"])
        self.assertEquals("sinz", answer)
        
    def test_With_no_command_we_get_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test"])
        self.assertTrue(re.search("^getCommitIdentifier :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout
        
    def test_help_gives_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test", "help"])
        self.assertTrue(re.search("^getCommitIdentifier :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout

    def test_help_help_gives_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test", "help", "help"])
        self.assertTrue(re.search("^getCommitIdentifier :", sys.stdout.getvalue(), re.MULTILINE))
        sys.stdout = oldstdout
        
    def test_Nonsense_commands_give_help(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        self.assertRaises(SystemExit,self.cli.main,["called from test", "foo", "bar"])
        ret = sys.stdout.getvalue()
        sys.stdout = oldstdout
        print(ret)
        self.assertTrue(re.search("^getCommitIdentifier :", ret, re.MULTILINE))
        
    def test_with_SINZ_DEBUG_envvar_sinz_prints_commands(self):
        if os.environ.get("skip_long_tests"):
            self.skipTest("skipping long test")

        oldstdout = sys.stdout
        sys.stdout = StringIO()
        os.environ["SINZ_DEBUG"]="yes"
        with TestProject():
            self.cli.main(["called from test","deb","sourceBuild"])
            self.assertEquals('echo y |debuild -us -uc -S\nNone\n', sys.stdout.getvalue())
            sys.stdout = oldstdout
        del os.environ["SINZ_DEBUG"]

if __name__ == "__main__":
    unittest.main()