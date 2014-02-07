import unittest
from sinz.Util import Util, CmdRunException


class UtilTest(unittest.TestCase):

    def test_Bad_command_raises_exception(self):
        self.assertRaises(CmdRunException,Util.runCmd,"ls /nosuchfile")

    def test_Bad_command_with_password_does_not_return_password(self):
        try:
            Util.runCmd("ls /nosuchfile", havepassword = True)
        except CmdRunException as e:
            self.assertEquals('<command containing password>', e.message)
            return
        self.fail()

    def test_Bad_command_output_is_gathered(self):
        try:
            Util.cmdOutput("echo foo;ls /nosuchfile")
        except CmdRunException as e:
            self.assertEquals(('echo foo;ls /nosuchfile', 'foo\n', 'ls: cannot access /nosuchfile: No such file or directory\n'), e.message)
            return
        self.fail()

    def test_Bad_command_with_password_does_not_return_password2(self):
        try:
            Util.cmdOutput("echo foo; ls /nosuchfile", havepassword = True)
        except CmdRunException as e:
            self.assertEquals(('<command containing password>', 'foo\n', 'ls: cannot access /nosuchfile: No such file or directory\n'), e.message)
            return
        self.fail()

if __name__ == "__main__":
    unittest.main()