# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import warns_db as wdb

# Data format: 
# warns: { "chat_id": { "user_id": { "num": int, "reasons": str } } }
# settings: { "chat_id": { "limit": int, "soft": bool } }

def warn_user(user_id, chat_id, reason=None):
    user_id = str(user_id)
    chat_id = str(chat_id)
    all_data = wdb.get_all()
    warns = all_data.get("warns", {})
    
    if chat_id not in warns:
        warns[chat_id] = {}
    if user_id not in warns[chat_id]:
        warns[chat_id][user_id] = {"num": 0, "reasons": ""}
    
    warns[chat_id][user_id]["num"] += 1
    if reason:
        warns[chat_id][user_id]["reasons"] += "\r\n\r\n" + reason
    
    all_data["warns"] = warns
    wdb.set("warns", warns)
    return warns[chat_id][user_id]["num"], warns[chat_id][user_id]["reasons"]

def remove_warn(user_id, chat_id):
    user_id = str(user_id)
    chat_id = str(chat_id)
    all_data = wdb.get_all()
    warns = all_data.get("warns", {})
    
    if chat_id in warns and user_id in warns[chat_id]:
        if warns[chat_id][user_id]["num"] > 0:
            warns[chat_id][user_id]["num"] -= 1
            wdb.set("warns", warns)
            return True
    return False

def reset_warns(user_id, chat_id):
    user_id = str(user_id)
    chat_id = str(chat_id)
    all_data = wdb.get_all()
    warns = all_data.get("warns", {})
    
    if chat_id in warns and user_id in warns[chat_id]:
        warns[chat_id][user_id] = {"num": 0, "reasons": ""}
        wdb.set("warns", warns)

def get_warns(user_id, chat_id):
    user_id = str(user_id)
    chat_id = str(chat_id)
    warns = wdb.get("warns", {})
    if chat_id in warns and user_id in warns[chat_id]:
        return warns[chat_id][user_id]["num"], warns[chat_id][user_id]["reasons"]
    return None

def set_warn_limit(chat_id, warn_limit):
    chat_id = str(chat_id)
    settings = wdb.get("settings", {})
    if chat_id not in settings:
        settings[chat_id] = {"limit": warn_limit, "soft": False}
    else:
        settings[chat_id]["limit"] = warn_limit
    wdb.set("settings", settings)

def set_warn_strength(chat_id, soft_warn):
    chat_id = str(chat_id)
    settings = wdb.get("settings", {})
    if chat_id not in settings:
        settings[chat_id] = {"limit": 3, "soft": soft_warn}
    else:
        settings[chat_id]["soft"] = soft_warn
    wdb.set("settings", settings)

def get_warn_setting(chat_id):
    settings = wdb.get("settings", {})
    if res := settings.get(str(chat_id)):
        return res["limit"], res["soft"]
    return 3, False

def num_warns():
    warns = wdb.get("warns", {})
    total = 0
    for chat in warns.values():
        for user in chat.values():
            total += user["num"]
    return total

def num_warn_chats():
    warns = wdb.get("warns", {})
    return len(warns)
