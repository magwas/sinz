import unittest
import os
import sinz.cli
from sinz.cli.CLI import CLI
from tests.TestProject import TestProject
from tests.ReloadedTestCase import ReloadedTestCase
from sinz.Util import Util

class BasicInfoTest(ReloadedTestCase):

    def setUp(self):
        packetroot = os.path.commonprefix([sinz.cli.__file__, __file__])
        os.chdir(packetroot)

    def test_getVersion_returns_the_version_string(self):
        package = CLI().call(["test","getVersion"])
        self.assertEquals(package,"0.1")
        
    def test_getVersion_uses_autoconf_version_by_default(self):
        with TestProject("sed -i 's/0.1/autoversion/' configure.ac") as project:
            version = project.cli.call(["called from test","getVersion"])
            self.assertEqual(version,"autoversion")

    def test_getVersion_uses_debian_if_no_autoconf(self):
        with TestProject("rm -f configure.ac; sed -i 's/0.1/debversion/' debian/changelog") as project:
            version = project.cli.call(["called from test","getVersion"])
            self.assertEqual(version,"debversion")

    def test_getVersion_fails_if_no_autoconf_nor_debian(self):
        with TestProject("rm -rf configure.ac debian") as project:
            self.assertRaises(SystemExit,project.cli.call,(["called from test","getVersion"],))
            
    def test_getBranch_uses_drone_before_travis_envvar(self):
        os.environ["DRONE_BRANCH"]="/foo/bar/drone"
        os.environ["DRONE"]="true"
        os.environ["TRAVIS_BRANCH"]="/foo/bar/travis"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            helpstring = project.cli.call(["called from test","getBranch"])
            self.assertEqual(helpstring, "drone")
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS"]
        del os.environ["DRONE_BRANCH"]
        del os.environ["DRONE"]

    def test_getBranch_uses_travis_envvar(self):
        os.environ["TRAVIS_BRANCH"]="/foo/bar/travis"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            helpstring = project.cli.call(["called from test","getBranch"])
            self.assertEqual(helpstring, "travis")
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS"]

    def test_getBranch_uses_git_if_no_travis(self):
        with TestProject("git checkout -b gitbranch") as project:
            helpstring = project.cli.call(["called from test","getBranch"])
            self.assertEqual(helpstring, "gitbranch")

    def test_getCommit_uses_drone_before_travis_envvar(self):
        os.environ["DRONE_COMMIT"]="/foo/bar/drone"
        os.environ["DRONE"]="true"
        os.environ["TRAVIS_COMMIT"]="thisisthefakecommitid"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            retstring = project.cli.call(["called from test","getCommit"])
            self.assertEqual(retstring, "/foo/bar/drone")
        del os.environ["TRAVIS_COMMIT"]
        del os.environ["TRAVIS"]
        del os.environ["DRONE_COMMIT"]
        del os.environ["DRONE"]
        
    def test_getCommit_uses_travis_envvar(self):
        os.environ["TRAVIS_COMMIT"]="thisisthefakecommitid"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            retstring = project.cli.call(["called from test","getCommit"])
            self.assertEqual(retstring, "thisisthefakecommitid")
        del os.environ["TRAVIS_COMMIT"]
        del os.environ["TRAVIS"]

    def test_getCommit_uses_git_if_no_travis(self):
        with TestProject("git checkout -b gitbranch") as project:
            helpstring = project.cli.call(["called from test","getCommit"])
            commitid = Util.cmdOutput("git log|head -1 |awk '{print $2}'")
            self.assertEqual(helpstring, commitid)

    def test_getBuildId_uses_drone_before_travis_envvar(self):
        os.environ["DRONE_BUILD_NUMBER"]="42"
        os.environ["DRONE"]="true"
        os.environ["TRAVIS_BUILD_NUMBER"]="40"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            helpstring = project.cli.call(["called from test","getBuildId"])
            self.assertEqual(helpstring, "42")
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS"]
        del os.environ["DRONE_BUILD_NUMBER"]
        del os.environ["DRONE"]
        
    def test_getBuildId_uses_travis_envvar(self):
        os.environ["TRAVIS_BUILD_NUMBER"]="40"
        os.environ["TRAVIS"]="true"
        with TestProject() as project:
            helpstring = project.cli.call(["called from test","getBuildId"])
            self.assertEqual(helpstring, "40")
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS"]

    def test_complete_returns_completions_for_incomplete_words(self):
        completions = CLI().call(["complete test","complete", "2", "sinz", "deb", "get"])
        self.assertEquals(completions, 'getUpstreamVersion\ngetDebEmail\ngetPackage\ngetFullVersion')

    def test_complete_returns_completions_for_complete_words(self):
        completions = CLI().call(["complete test","complete", "2", "sinz", "deb"])
        self.assertEquals(completions, 'getUpstreamVersion\naddChangelogEntry\nsubmit\ngetDebEmail\ngetPackage\ngetFullVersion\nbuildAndDput\nsourceBuild')

if __name__ == "__main__":
    unittest.main()