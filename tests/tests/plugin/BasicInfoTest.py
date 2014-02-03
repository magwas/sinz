import unittest
import os
import sinz.cli
from sinz.cli.CLI import CLI
from tests.TestProject import TestProject
from tests.ReloadedTestCase import ReloadedTestCase

class BasicInfoTest(ReloadedTestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.cli.__file__, __file__])
        os.chdir(packetroot)

    def test_getVersion_returns_the_version_string(self):
        package = CLI().main(["test","getVersion"])
        self.assertEquals(package,"0.1")
        
    def test_getVersion_uses_autoconf_version_by_default(self):
        with TestProject("sed -i 's/0.1/autoversion/' configure.ac") as project:
            version = project.cli.main(["called from test","getVersion"])
            self.assertEqual(version,"autoversion")

    def test_getVersion_uses_debian_if_no_autoconf(self):
        with TestProject("rm -f configure.ac; sed -i 's/0.1/debversion/' debian/changelog") as project:
            version = project.cli.main(["called from test","getVersion"])
            self.assertEqual(version,"debversion")

    def test_getVersion_fails_if_no_autoconf_nor_debian(self):
        with TestProject("rm -rf configure.ac debian") as project:
            self.assertRaises(SystemExit,project.cli.main,(["called from test","getVersion"],))

if __name__ == "__main__":
    unittest.main()