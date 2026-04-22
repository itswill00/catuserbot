# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import gban_db as gdb

class GBan:
    def __init__(self, chat_id, reason=""):
        self.chat_id = str(chat_id)
        self.reason = str(reason)

def is_gbanned(chat_id):
    res = gdb.get(str(chat_id))
    if res:
        return GBan(str(chat_id), res)
    return None

def get_gbanuser(chat_id):
    res = gdb.get(str(chat_id))
    if res:
        return GBan(str(chat_id), res)
    return None

def catgban(chat_id, reason):
    gdb.set(str(chat_id), str(reason))

def catungban(chat_id):
    gdb.delete(str(chat_id))

def get_all_gbanned():
    raw_data = gdb.get_all()
    return [GBan(chat_id, reason) for chat_id, reason in raw_data.items()]
