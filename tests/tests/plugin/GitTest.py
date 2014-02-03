import unittest
from sinz.cli.CLI import CLI
from sinz.Util import Util

class GitTest(unittest.TestCase):

    def test_git_getBranch_gives_the_actual_branch_name(self):
        branch=CLI().main(["test","git","getBranch"])
        cmd = "git branch|grep '^\*'|sed 's/..//'"
        branchfromgit = Util.cmdOutput(cmd)
        self.assertEquals(branch,branchfromgit)
        
    def test_git_getCommit_gives_the_current_commit_id(self):
        branch=CLI().main(["test","git","getCommit"])
        cmd = "git log |head -1|awk '{print $2}'"
        branchfromgit = Util.cmdOutput(cmd)
        self.assertEquals(branch,branchfromgit)

if __name__ == "__main__":
    unittest.main()