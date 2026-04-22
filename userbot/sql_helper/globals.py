# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import global_db as gdb

def gvarstatus(variable):
    """Get global variable value from JSON database."""
    return gdb.get(str(variable))

def addgvar(variable, value):
    """Add or update global variable in JSON database."""
    gdb.set(str(variable), value)

def delgvar(variable):
    """Delete global variable from JSON database."""
    gdb.delete(str(variable))
