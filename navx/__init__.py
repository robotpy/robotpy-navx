try:
    from .version import __version__
except ImportError:
    __version__ == "master"

from .ahrs import AHRS
from .pins import *
