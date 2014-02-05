from sinz.cli.CLI import CLI
from sinz.cli.Registry import Registry

@CLI.mixin
class Help(object):
    cliName =["help"]
    @CLI.climethod
    def help(self):
        ret = []
        for (name,func) in Registry().commands.items():
            ret.append("%s : %s"%(name,func))
        return "\n".join(ret)
