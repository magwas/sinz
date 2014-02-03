import unittest

class ReloadedTestCase(unittest.TestCase):
    def assertExceptionName(self,name,runnable,args):
            try:
                runnable(*args)
                self.fai()
            except Exception as e:
                self.assertEquals(name, e.__class__.__name__)

