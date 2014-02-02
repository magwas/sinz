from sinz.Singleton import Singleton

class Registry(Singleton):
    INSTANCE = None
    def __init__(self):
        self.commands = {}
    @classmethod
    def climethod(cls,fn):
        cls.getInstance().commands[fn.__name__] = fn
        return fn
    
    
        