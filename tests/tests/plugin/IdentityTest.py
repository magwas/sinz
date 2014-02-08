import unittest
from tests.TestProject import TestProject
from sinz.plugins.Identity import Identity
import os

class IdentityYest(unittest.TestCase):

    def test_if_IDENTITY_ACCOUNT_envvar_is_defined_then_ssh_identity_used(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["IDENTITY_ACCOUNT"] = "testidentity@magwas.rulez.org"
        os.environ["SFTP_ARGS"] = "-i testidentity.key"
        with TestProject("chmod 500 testidentity.key"):
            self.assertEqual("-i testidentity.key", os.environ["SFTP_ARGS"])
            self.assertEqual("test", os.environ["PGPASSWORD"])
        del os.environ["IDENTITY_ACCOUNT"]
        del os.environ["SFTP_ARGS"]
            
    def test_identity_brings_file_from_tree_as_fallback(self):
        with TestProject("sed -i 's/changelog/treemarker/' NEWS"):
            Identity().bring("NEWS")  # @UndefinedVariable
            news = open("NEWS")
            self.assertEquals("see debian/treemarker\n",news.read())
            news.close()
            
    def test_gpg_works_with_identity_defined_envvars(self):
        if os.environ.get("skip_long_tests",False):
            self.skipTest("skipping long test")
        os.environ["IDENTITY_ACCOUNT"] = "testidentity@magwas.rulez.org"
        os.environ["SFTP_ARGS"] = "-i testidentity.key"
        os.environ["PGPKEY"]="97421C66"
        with TestProject("chmod 500 testidentity.key;rm .gpg.key") as project:
            project.cli.call(["called from test","gpg","sign", "configure.ac"])
            self.assertTrue(os.path.isfile("configure.ac.asc"))
        del os.environ["IDENTITY_ACCOUNT"]
        del os.environ["SFTP_ARGS"]
        del os.environ["PGPKEY"]

if __name__ == "__main__":
    unittest.main()