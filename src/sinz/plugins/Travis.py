from sinz.cli.CLI import CLI
from sinz.PluginInitException import PluginInitException
import os

class NotInTravisBuild(PluginInitException):
    def __str__(self):
        return "no TRAVIS/TRAVIS_BRANCH/TRAVIS_BUILD_NUMBER/TRAVIS_COMMIT environment variable"

@CLI.mixin
class Travis(object):
    def __init__(self):
        if not os.environ.get("TRAVIS",False):
            raise NotInTravisBuild(self)
        self.branch = os.environ.get("TRAVIS_BRANCH")
        self.buildNumber = os.environ.get("TRAVIS_BUILD_NUMBER")
        self.commit = os.environ.get("TRAVIS_COMMIT")
    @CLI.climethod
    def getBranch(self):
        return self.branch
    @CLI.climethod
    def getCommit(self):
        return self.commit
    @CLI.climethod
    def getBuildId(self):
        return self.buildNumber
        