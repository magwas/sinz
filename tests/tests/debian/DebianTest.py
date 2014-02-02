
import unittest
import os
import sinz.debian.Debian
from sinz.debian.Debian import Debian, NonDebianPackageError

class DebianTest(unittest.TestCase):
    
    def setUp(self):
        packetroot = os.path.commonprefix([sinz.debian.Debian.__file__, __file__])
        os.chdir(packetroot)

    def test_Debian_getPackage_returns_the_package_name(self):
        self.assertEqual("sinz", Debian().getPackage())
    
    def test_Debian_getFullVersion_returns_full_package_version(self):
        self.assertEqual("0.1", Debian().getFullVersion())
        
    def test_The_Debian_class_do_not_work_in_a_non_debianized_package(self):
        os.chdir("tests")
        self.assertRaises(NonDebianPackageError, Debian)
        try:
            Debian()
        except NonDebianPackageError as e:
            self.assertEquals("This operation needs a Debian package", str(e))
        
if __name__ == "__main__":
    unittest.main()