import unittest
import traceback

class ReloadedTestCase(unittest.TestCase):
    def assertExceptionName(self,name,runnable,args):
            try:
                runnable(*args)
            except Exception as e:
                if name != e.__class__.__name__:
                    traceback.print_exc()
                    self.fail("Unexpected exception: %s"%(e,))
                return
            self.fail("did not get exception %s\n"%(name,))

