# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import JsonDB

listdb = JsonDB("cat_lists")

class GLOBALLIST_SQL:
    def __init__(self):
        raw_data = listdb.get_all()
        self.GLOBALLIST_VALUES = {str(k): set(v) for k, v in raw_data.items()}

GLOBALLIST_SQL_ = GLOBALLIST_SQL()

def add_to_list(keywoard, group_id):
    keywoard = str(keywoard)
    group_id = str(group_id)
    if keywoard not in GLOBALLIST_SQL_.GLOBALLIST_VALUES:
        GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard] = set()
    GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard].add(group_id)
    listdb.set(keywoard, list(GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]))

def rm_from_list(keywoard, group_id):
    keywoard = str(keywoard)
    group_id = str(group_id)
    if keywoard in GLOBALLIST_SQL_.GLOBALLIST_VALUES and group_id in GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]:
        GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard].remove(group_id)
        if not GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]:
            listdb.delete(keywoard)
            del GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]
        else:
            listdb.set(keywoard, list(GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]))
        return True
    return False

def is_in_list(keywoard, group_id):
    return str(group_id) in GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(str(keywoard), set())

def del_keyword_list(keywoard):
    keywoard = str(keywoard)
    if keywoard in GLOBALLIST_SQL_.GLOBALLIST_VALUES:
        listdb.delete(keywoard)
        del GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard]

def get_collection_list(keywoard):
    return GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(str(keywoard), set())

def get_list_keywords():
    return list(GLOBALLIST_SQL_.GLOBALLIST_VALUES.keys())

def num_list():
    return sum(len(v) for v in GLOBALLIST_SQL_.GLOBALLIST_VALUES.values())

def num_list_keyword(keywoard):
    return len(GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(str(keywoard), set()))

def num_list_keywords():
    return len(GLOBALLIST_SQL_.GLOBALLIST_VALUES)
