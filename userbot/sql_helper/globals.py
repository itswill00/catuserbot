# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import global_db as gdb

def gvarstatus(variable):
    """Mendapatkan nilai variabel dari database JSON."""
    return gdb.get(str(variable))

def addgvar(variable, value):
    """Menambah atau memperbarui variabel di database JSON."""
    gdb.set(str(variable), value)

def delgvar(variable):
    """Menghapus variabel dari database JSON."""
    gdb.delete(str(variable))
