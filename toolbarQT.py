from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib import cbook
import functools
from PySide6 import QtCore, QtGui

class NavigationToolbar(NavigationToolbar2QT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)