import unittest
import os
from tests.TestProject import TestProject
from tests.ReloadedTestCase import ReloadedTestCase

class TravisTest(ReloadedTestCase):

    def test_travis_module_not_works_if_envvar_Travis_is_not_yes(self):
        self.assertFalse(os.environ.get("TRAVIS")=="yes")
        os.environ["TRAVIS_BRANCH"]="/foo/bar/travisbranch"
        with TestProject() as project:
            self.assertExceptionName("NotInTravisBuild",project.cli.runCmd,(["called from test","travis","getBranch"],))
        del os.environ["TRAVIS_BRANCH"]

    def test_travis_getBranch_returns_value_of_TRAVIS_BRANCH_envvar(self):
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_BRANCH"]="/foo/bar/tb"
        with TestProject() as project:
            self.assertEquals("tb",project.cli.runCmd(["called from test","travis","getBranch"]))
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS"]

    def test_travis_getCommit_returns_value_of_TRAVIS_COMMIT_envvar(self):
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_COMMIT"]="1234567"
        with TestProject() as project:
            self.assertEquals("1234567",project.cli.runCmd(["called from test","travis","getCommit"]))
        del os.environ["TRAVIS_COMMIT"]
        del os.environ["TRAVIS"]

    def test_travis_getBuildId_returns_value_of_TRAVIS_BUILD_NUMBER_envvar(self):
        os.environ["TRAVIS"]="yes"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        with TestProject() as project:
            self.assertEquals("42",project.cli.runCmd(["called from test","travis","getBuildId"]))
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS"]

if __name__ == "__main__":
    unittest.main()