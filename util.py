#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle, os
from PyQt5 import QtGui

CONFIG_FILE = "info.cfg"
ENCRYPTION_KEY = b"qfkdsgnbaug[i398f*&GF&^]v 2414*&O*F(&)"

_all_icons = {
    "appicon": "appicon.png",
    "car": "car.png",
    "cardetails": "cardetails.png",
    "customer": "customer.png",
    "detail": "detail.png",
    "employee": "employee.png",
    "order": "order.png",
    "shop": "shop.png",
    "warehouse": "warehouse.png"
}

_icons = {}

def get_icon(name):
    if not _icons:
        _init_icons()
    return _icons.get(name, None)

def _init_icons():
    for name, path in _all_icons.items():
        _icons[name] = QtGui.QIcon(os.path.join("res", *path.split("/")))


def save_data(login, password, dbname):
    data = crypt(pickle.dumps([login, password, dbname]), ENCRYPTION_KEY)
    with open(CONFIG_FILE, "wb") as f:
        f.write(data)

def load_data():
    try:
        with open(CONFIG_FILE, "rb") as f:
            text = f.read()
    except FileNotFoundError:
        return [""] * 3
    try:
        return pickle.loads(crypt(text, ENCRYPTION_KEY))
    except:
        return [""] * 3

def crypt(s, key):
    # Наивное шифрование побитовым XOR
    key = key * (len(s)//len(key) + 1)
    return bytes(c1^c2 for c1, c2 in zip(s, key))
