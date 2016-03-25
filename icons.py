# -*- coding: utf-8 -*-

import os
from PyQt5 import QtGui

_all_icons = {
    "appicon": "appicon.png"
}

def init_icons():
    global icons
    icons = {}
    for name, path in _all_icons.items():
        icons[name] = QtGui.QIcon(os.path.join(*path.split("/")))