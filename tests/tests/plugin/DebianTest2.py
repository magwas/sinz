import unittest
import os
from tests.TestProject import TestProject
import sys
from StringIO import StringIO
import re
from sinz.Util import Util

class DebianTest2(unittest.TestCase):

    def test_deb_sourceBuild_results_in_dsc_and_targz(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        os.environ["TRAVIS_BRANCH"]="travis-Branch"
        os.environ["TRAVIS_COMMIT"]="ebadadeadbeef"
        os.environ["DEBEMAIL"]="Test Builder <builder@example.com>"
        if os.environ.get("DEBFULLNAME", False):
            del os.environ["DEBFULLNAME"]
        with TestProject() as project:
            project.cli.call(["called from test","deb","addChangelogEntry"])
            project.cli.call(["called from test","deb","sourceBuild"])
            self.assertTrue(os.path.isfile("../sinz_0.1-42travis-Branch.dsc"))
            self.assertTrue(os.path.isfile("../sinz_0.1-42travis-Branch.tar.gz"))
            self.assertTrue(os.path.isfile("../sinz_0.1-42travis-Branch_source.changes"))
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS_COMMIT"]

    def test_deb_submit_submits_the_package_with_dput_using_provided_dput_dot_cf(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_BUILD_NUMBER"]="0"
        os.environ["TRAVIS_BRANCH"]="testoutput"
        os.environ["TRAVIS_COMMIT"]="ebadadeadbeef"
        os.environ["DEBEMAIL"]="Sinz Test (This is a test key, do not trust it!) <mag+sinz@magwas.rulez.org>"
        os.environ["PGPASSWORD"]="test"
        os.environ["PGPKEY"]="97421C66"
        if os.environ.get("DEBFULLNAME", False):
            del os.environ["DEBFULLNAME"]
        with TestProject() as project:
            project.cli.call(["called from test","deb","addChangelogEntry"])
            project.cli.call(["called from test","deb","sourceBuild"])
            project.cli.call(["called from test", "gpg", "debSign"])
            project.cli.call(["called from test","deb","submit"])
            self.assertTrue(os.path.isfile("../sinz_0.1-0testoutput_source.nonmaster.upload"))
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS_COMMIT"]

    def test_deb_buildAndDput_builds_and_submits_for_debian_builder(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_BUILD_NUMBER"]="1"
        os.environ["TRAVIS_BRANCH"]="testoutputbranch"
        os.environ["TRAVIS_COMMIT"]="ebadadeadbeef"
        os.environ["DEBEMAIL"]="Sinz Test (This is a test key, do not trust it!) <mag+sinz@magwas.rulez.org>"
        os.environ["PGPASSWORD"]="test"
        os.environ["PGPKEY"]="97421C66"
        if os.environ.get("DEBFULLNAME", False):
            del os.environ["DEBFULLNAME"]
        with TestProject() as project:
            project.cli.call(["called from test","deb","buildAndDput"])
            self.assertTrue(os.path.isfile("../sinz_0.1-1testoutputbranch_source.nonmaster.upload"))
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS_COMMIT"]

if __name__ == "__main__":
    unittest.main()