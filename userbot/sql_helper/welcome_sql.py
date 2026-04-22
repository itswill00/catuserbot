# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import welcome_db as wdb

class Welcome:
    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id

def get_welcome(chat_id):
    if res := wdb.get(str(chat_id)):
        return Welcome(chat_id, res["previous_welcome"], res["reply"], res["f_mesg_id"])
    return None

def get_current_welcome_settings(chat_id):
    return get_welcome(chat_id)

def add_welcome_setting(chat_id, previous_welcome, reply, f_mesg_id):
    is_new = not wdb.get(str(chat_id))
    wdb.set(str(chat_id), {
        "previous_welcome": previous_welcome,
        "reply": reply,
        "f_mesg_id": f_mesg_id
    })
    return is_new

def rm_welcome_setting(chat_id):
    if wdb.get(str(chat_id)):
        wdb.delete(str(chat_id))
        return True
    return False

def update_previous_welcome(chat_id, previous_welcome):
    data = wdb.get(str(chat_id))
    if data:
        data["previous_welcome"] = previous_welcome
        wdb.set(str(chat_id), data)
