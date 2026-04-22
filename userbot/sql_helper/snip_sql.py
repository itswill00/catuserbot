# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import notes_db as ndb

class Note:
    def __init__(self, keyword, reply, f_mesg_id):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

def get_note(keyword):
    if res := ndb.get(str(keyword)):
        return Note(keyword, res["reply"], res["f_mesg_id"])
    return None

def get_notes():
    raw_data = ndb.get_all()
    return [Note(kw, data["reply"], data["f_mesg_id"]) for kw, data in raw_data.items()]

def add_note(keyword, reply, f_mesg_id):
    is_new = not ndb.get(str(keyword))
    ndb.set(str(keyword), {"reply": reply, "f_mesg_id": f_mesg_id})
    return is_new

def rm_note(keyword):
    if ndb.get(str(keyword)):
        ndb.delete(str(keyword))
        return True
    return False
