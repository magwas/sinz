import unittest
import os
from tests.TestProject import TestProject

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

if __name__ == "__main__":
    unittest.main()