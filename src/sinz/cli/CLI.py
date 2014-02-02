import sys
from sinz.Singleton import Singleton
from sinz.cli.Registry import Registry
from sinz.Plugin import Plugin

class CLI(Plugin):
    @Registry.climethod
    def help(self):
        ret = []
        for (name,func) in Registry.getInstance().commands.items():
            ret.append("%s : %s"%(name,func))
        return "\n".join(ret)
    
    def run(self,func):
        ret = func(self)
        if None is not ret:
            print(ret)
        return ret
    
    @classmethod
    def mixin(cls,klass):
        cls.__bases__=(klass,) + (cls.__bases__)
        return klass
        
    def main(self,argv):
        if(2 > len(argv)):
            self.run(self.help)
            sys.exit(1)
        return self.run(Registry.getInstance().commands[argv[1]])
        
if __name__ == '__main__':
    CLI.main(sys.argv)