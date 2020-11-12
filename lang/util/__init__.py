### IMPORTS                         ###
from os import chdir as cd
from typing import AnyStr
### IMPORTS                         ###
class ContextManagerObject(object):
    def __init__(self, dest): self.__dest = dest
    def __enter__(self): cd(self.__dest); return self
    def __exit__(self, *argz, **kwargz): cd('..')
def cd_back(dest: AnyStr) -> ContextManagerObject: return ContextManagerObject(dest)