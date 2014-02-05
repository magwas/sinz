import unittest
from tests.TestProject import TestProject
from sinz.plugins.Identity import Identity

class IdentityYest(unittest.TestCase):
    def test_identity_brings_file_from_tree_as_fallback(self):
        with TestProject("sed -i 's/changelog/treemarker/' NEWS"):
            Identity().bring("NEWS")  # @UndefinedVariable
            news = open("NEWS")
            self.assertEquals("see debian/treemarker\n",news.read())
            news.close()

if __name__ == "__main__":
    unittest.main()