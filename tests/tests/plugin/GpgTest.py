import unittest
from tests.TestProject import TestProject
import os
from sinz.cli.CLI import CLI

class GpgTest(unittest.TestCase):
    def test_gpg_sign_signes_file(self):
        os.environ["PGPASSWORD"]="test"
        os.environ["PGPKEY"]="97421C66"
        with TestProject("cp tests/test.key .gpg.key") as project:
            project.cli.call(["called from test","gpg","sign", "configure.ac"])
            self.assertTrue(os.path.isfile("configure.ac.asc"))

    def test_gpg_debSign_signes_source_package_upload(self):
        if os.environ.get("skip_long_tests"):
            self.skipTest("skipping long test")
        os.environ["PGPASSWORD"]="test"
        os.environ["PGPKEY"]="97421C66"
        os.environ["TRAVIS"]="true"
        os.environ["TRAVIS_BUILD_NUMBER"]="42"
        os.environ["TRAVIS_BRANCH"]="travis-Branch"
        os.environ["TRAVIS_COMMIT"]="ebadadeadbeef"
        os.environ["DEBEMAIL"]="Sinz Test (This is a test key, do not trust it!) <mag+sinz@magwas.rulez.org>"
        if os.environ.get("DEBFULLNAME", False):
            del os.environ["DEBFULLNAME"]
        with TestProject("cp tests/test.key .gpg.key") as project:
            project.cli.call(["called from test","deb","addChangelogEntry"])
            project.cli.call(["called from test","deb","sourceBuild"])
            project.cli.call(["called from test", "gpg", "debSign"])
            
            pkgname = CLI().call(["debSign", "getPackage"])
            fullversion = CLI().call(["debSign", "deb", "getFullVersion"])
            changesfilename = "../%s_%s_source.changes"%(pkgname, fullversion)

            cf2 = open(changesfilename)
            changes = cf2.read()
            cf2.close()
            self.assertTrue(len(changes.split("BEGIN PGP SIGNATURE")) > 1)
        del os.environ["TRAVIS"]
        del os.environ["TRAVIS_BUILD_NUMBER"]
        del os.environ["TRAVIS_BRANCH"]
        del os.environ["TRAVIS_COMMIT"]


if __name__ == "__main__":
    unittest.main()