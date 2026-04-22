# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import JsonDB

pmdb = JsonDB("cat_pmpermit")

class PmPermit_Sql:
    def __init__(self, user_id, first_name, date, username, reason):
        self.user_id = str(user_id)
        self.first_name = first_name
        self.date = date
        self.username = username
        self.reason = reason

def approve(user_id, first_name, date, username, reason):
    user_data = {
        "user_id": str(user_id),
        "first_name": first_name,
        "date": date,
        "username": username,
        "reason": reason
    }
    pmdb.set(str(user_id), user_data)
    return True

def disapprove(user_id):
    if pmdb.get(str(user_id)):
        pmdb.delete(str(user_id))
        return True
    return False

def is_approved(user_id):
    res = pmdb.get(str(user_id))
    if res:
        return PmPermit_Sql(**res)
    return None

def get_all_approved():
    all_users = pmdb.get_all()
    return [PmPermit_Sql(**data) for data in all_users.values()]

def disapprove_all():
    pmdb.clear()
    return True
