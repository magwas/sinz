
import unittest
import os
import sinz.cli
import subprocess
from sinz.plugins.Debian import Debian

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
        os.chdir("src")
        a=subprocess.call("./sinz.py help",shell=True)
        self.assertEquals(a, 0)
        
    def test_The_deb_command_do_not_work_in_a_non_debianized_package(self):
        os.chdir("src")
        a=subprocess.call("./sinz.py Debian.getPackage",shell=True)
        self.assertEquals(a, 1)
        
if __name__ == "__main__":
    unittest.main()