# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import blacklist_db as bdb

class BLACKLIST_SQL:
    def __init__(self):
        # Load from JSON and convert lists to sets for performance
        raw_data = bdb.get_all()
        self.CHAT_BLACKLISTS = {str(k): set(v) for k, v in raw_data.items()}

BLACKLIST_SQL_ = BLACKLIST_SQL()

def add_to_blacklist(chat_id, trigger):
    chat_id = str(chat_id)
    if chat_id not in BLACKLIST_SQL_.CHAT_BLACKLISTS:
        BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id] = set()
    
    BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id].add(trigger)
    # Save as list to JSON
    bdb.set(chat_id, list(BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id]))

def rm_from_blacklist(chat_id, trigger):
    chat_id = str(chat_id)
    if chat_id in BLACKLIST_SQL_.CHAT_BLACKLISTS and trigger in BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id]:
        BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id].remove(trigger)
        if not BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id]:
            bdb.delete(chat_id)
        else:
            bdb.set(chat_id, list(BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id]))
        return True
    return False

def get_chat_blacklist(chat_id):
    return BLACKLIST_SQL_.CHAT_BLACKLISTS.get(str(chat_id), set())

def num_blacklist_filters():
    return sum(len(v) for v in BLACKLIST_SQL_.CHAT_BLACKLISTS.values())

def num_blacklist_chat_filters(chat_id):
    return len(BLACKLIST_SQL_.CHAT_BLACKLISTS.get(str(chat_id), set()))

def num_blacklist_filter_chats():
    return len(BLACKLIST_SQL_.CHAT_BLACKLISTS)
