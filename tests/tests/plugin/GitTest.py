import unittest
from sinz.cli.CLI import CLI
from sinz.Util import Util
from tests.TestProject import TestProject

class GitTest(unittest.TestCase):

    def test_git_getBranch_gives_the_actual_branch_name(self):
        branch=CLI().call(["test","git","getBranch"])
        cmd = "git branch|grep '^\*'|sed 's/..//'"
        branchfromgit = Util.cmdOutput(cmd)
        self.assertEquals(branch,branchfromgit)

    def test_git_getBranch_gives_the_last_tag_of_branch_name(self):
        with TestProject("git checkout -b 'foo/bar'"):
            branch=CLI().call(["test","git","getBranch"])
            self.assertEquals(branch,"bar")
        
    def test_git_getCommit_gives_the_current_commit_id(self):
        branch=CLI().call(["test","git","getCommit"])
        cmd = "git log |head -1|awk '{print $2}'"
        branchfromgit = Util.cmdOutput(cmd)
        self.assertEquals(branch,branchfromgit)
        
    def test_git_getNewTestCases_lists_new_testcases(self):
        with TestProject("cp tests/tests/plugin/GitTest.py tests/tests/plugin/Othertest.py; git add tests/tests/plugin/Othertest.py"):
            cases = CLI().call(["test","git","getNewTestCases"])
            thecases = """git getBranch gives the actual branch name
git getBranch gives the last tag of branch name
git getCommit gives the current commit id
git getNewTestCases lists new testcases"""
            self.assertEquals(thecases,cases.strip())


if __name__ == "__main__":
    unittest.main()