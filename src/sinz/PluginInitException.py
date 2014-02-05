class PluginInitException(Exception):
    def __init__(self,instance):
        self.instance = instance
    def __call__(self,*args):
        raise self
