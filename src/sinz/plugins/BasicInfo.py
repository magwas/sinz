from sinz.cli.CLI import CLI

@CLI.mixin
class BasicInfo(object):
    cliName = []

    @CLI.climethod
    def getVersion(self):
        return CLI().firstUseable([
                ["autoconf", "getVersion"],
                ["deb", "getUpstreamVersion"],
            ])