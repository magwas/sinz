# -*- coding: UTF-8 -*-
import unittest
import os
import sinz.cli
from sinz.plugins.Debian import Debian
from tests.TestProject import TestProject
import re
from tests.ReloadedTestCase import ReloadedTestCase

class DebianTest(ReloadedTestCase):
    
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

    def test_deb_getDebEmail_uses_DEBEMAIL_environment_variable(self):
        os.environ["DEBEMAIL"]="Test User <test@example.com>"
        with TestProject() as project:
            helpstring = project.cli.main(["called from test","deb","getDebEmail"])
            self.assertEqual(helpstring, "Test User <test@example.com>")
        del os.environ["DEBEMAIL"]

    def test_if_no_DEBEMAIL_environment_variable_deb_getDebEmail_uses_the_changelog(self):
        self.assertEquals(None, os.environ.get("DEBEMAIL"))
        with TestProject() as project:
            helpstring = project.cli.main(["called from test","deb","getDebEmail"])
            self.assertEqual(helpstring, "Árpád Magosányi <mag@balabit.hu>")
            
    def test_deb_addChangelogEntry_adds_a_changelog_entry(self):
        os.environ["TRAVIS"]="true"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        with TestProject() as project:
            cmdline = project.cli.main(["called from test","deb","addChangelogEntry"])
            self.assertEquals("",cmdline)
            clf = open("debian/changelog")
            changelog = clf.read()
            clf.close()
            self.assertEquals(changelog, "")
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]

if __name__ == "__main__":
    unittest.main()