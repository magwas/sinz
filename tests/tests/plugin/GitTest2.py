import unittest
from tests.TestProject import TestProject
import os
from sinz.cli.CLI import CLI
import subprocess

class GitTest2(unittest.TestCase):

    def test_sinz_works_in_non_git_tree(self):
        os.environ["TRAVIS"]="true"
        os.environ["TRAVIS_BRANCH"]="travis-Branch"
        os.environ["TRAVIS_COMMIT"]="travis-commit"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        with TestProject():
            os.chdir("..")
            self.assertEqual(128,subprocess.call("git branch",shell=True))
            commit=CLI().call(["test","getCommit"])
            self.assertEquals(commit,"travis-commit")
            branch=CLI().call(["test","getBranch"])
            self.assertEquals(branch,"travis-Branch")
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_COMMIT"]
        del os.environ["TRAVIS_BRANCH"]

    def test_sinz_works_in_detached_git_tree(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["TRAVIS"]="true"
        os.environ["TRAVIS_BRANCH"]="travis-Branch"
        os.environ["TRAVIS_COMMIT"]="travis-commit"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        with TestProject():
            os.chdir("..")
            self.assertEqual(0,subprocess.call("git clone --depth=50 --branch=master git://github.com/magwas/sinz.git sinz",shell=True))
            os.chdir("sinz")
            self.assertEqual(0,subprocess.call("git checkout -qf a63285b389f9a0f7684fec2525c9904b430fad3b",shell=True))
            commit=CLI().call(["test","getCommit"])
            self.assertEquals(commit,"travis-commit")
            branch=CLI().call(["test","getBranch"])
            self.assertEquals(branch,"travis-Branch")
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_COMMIT"]
        del os.environ["TRAVIS_BRANCH"]

if __name__ == "__main__":
    unittest.main()