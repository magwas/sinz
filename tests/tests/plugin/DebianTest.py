
import unittest
import os
import sinz.cli
from sinz.plugins.Debian import Debian
from tests.TestProject import TestProject
import re

class DebianTest(unittest.TestCase):
    
    def setUp(self):
        packetroot = os.path.commonprefix([sinz.cli.__file__, __file__])
        os.chdir(packetroot)
        self.debian=Debian()

    def test_Debian_getPackage_returns_the_package_name(self):
        self.assertEqual("sinz", self.debian.getPackage())
    
    def test_Debian_getFullVersion_returns_full_package_version(self):
        self.assertEqual("0.1", self.debian.getFullVersion())

    def test_The_deb_command_do_work_in_a_debianized_package(self):
        a=os.system("./src/sinz.py deb getPackage")
        self.assertEquals(a, 0)
        
    def test_Other_functions_do_work_in_a_non_debianized_package(self):
        with TestProject("rm -rf debian") as project:
            helpstring = project.cli.main(["called from test","help","help"])
            self.assertTrue(re.search("^help :", helpstring, re.MULTILINE))
            self.assertTrue(re.search("^deb :", helpstring, re.MULTILINE))
        
    def test_The_deb_command_do_not_work_in_a_non_debianized_package(self):
        with TestProject("rm -rf debian") as project:
            self.assertExceptionName("NonDebianPackageError",project.cli.runCmd,(["called from test","deb","getPackage"],))

    def assertExceptionName(self,name,runnable,args):
            try:
                runnable(*args)
                self.fai()
            except Exception as e:
                self.assertEquals(name, e.__class__.__name__)

        
if __name__ == "__main__":
    unittest.main()