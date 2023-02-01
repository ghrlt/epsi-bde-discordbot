from __main__ import bot, slash

import os

def getAbsolutePath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

