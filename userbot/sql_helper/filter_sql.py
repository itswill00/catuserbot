# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import filters_db as fdb

class Filter:
    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

def get_filter(chat_id, keyword):
    chat_filters = fdb.get(str(chat_id), {})
    if res := chat_filters.get(keyword):
        return Filter(chat_id, keyword, res["reply"], res["f_mesg_id"])
    return None

def get_filters(chat_id):
    chat_filters = fdb.get(str(chat_id), {})
    return [Filter(chat_id, kw, data["reply"], data["f_mesg_id"]) for kw, data in chat_filters.items()]

def add_filter(chat_id, keyword, reply, f_mesg_id):
    chat_id = str(chat_id)
    chat_filters = fdb.get(chat_id, {})
    is_new = keyword not in chat_filters
    chat_filters[keyword] = {"reply": reply, "f_mesg_id": f_mesg_id}
    fdb.set(chat_id, chat_filters)
    return is_new

def remove_filter(chat_id, keyword):
    chat_id = str(chat_id)
    chat_filters = fdb.get(chat_id, {})
    if keyword in chat_filters:
        del chat_filters[keyword]
        if not chat_filters:
            fdb.delete(chat_id)
        else:
            fdb.set(chat_id, chat_filters)
        return True
    return False

def remove_all_filters(chat_id):
    fdb.delete(str(chat_id))
