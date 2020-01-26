import glob
import ntpath
import os.path
import importlib
#not sure why this file is being called twice
#from modules.debug import main as debug

moduleBlacklist = ["__init__"]
__all__ = glob.glob("modules/*.py")
__all__ = [ntpath.basename(m) for m in __all__]
__all__ = [os.path.splitext(m)[0] for m in __all__]
__all__ = [m for m in __all__ if m not in moduleBlacklist]