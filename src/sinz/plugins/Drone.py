from sinz.cli.CLI import CLI
from sinz.PluginInitException import PluginInitException
import os

class NotInDroneBuild(PluginInitException):
    def __str__(self):
        return "no DRONE/DRONE_BRANCH/DRONE_BUILD_NUMBER/DRONE_COMMIT environment variable"

@CLI.mixin
class DRONE(object):
    cliName = ["drone"]
    def __init__(self):
        if not "true" == os.environ.get("DRONE",False):
            raise NotInDroneBuild(self)
        self.branch = os.environ.get("DRONE_BRANCH")
        self.buildNumber = os.environ.get("DRONE_BUILD_NUMBER")
        self.commit = os.environ.get("DRONE_COMMIT")
    @CLI.climethod
    def getBranch(self):
        return self.branch.split("/")[-1]
    @CLI.climethod
    def getCommit(self):
        return self.commit
    @CLI.climethod
    def getBuildId(self):
        return self.buildNumber
        