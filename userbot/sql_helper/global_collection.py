# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import threading
from .json_db import JsonDB

# Use JSON DB instead of SQL
gcoldb = JsonDB("cat_collections")
CAT_GLOBALCOLLECTION = threading.RLock()

# Dummy class for compatibility if needed, but we store data as dicts
class Cat_GlobalCollection:
    def __init__(self, keywoard, contents):
        self.keywoard = keywoard
        self.contents = tuple(contents)

def add_to_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        data = gcoldb.get(str(keywoard), [])
        item = list(contents)
        if item not in data:
            data.append(item)
            gcoldb.set(str(keywoard), data)

def rm_from_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        data = gcoldb.get(str(keywoard), [])
        item = list(contents)
        if item in data:
            data.remove(item)
            gcoldb.set(str(keywoard), data)
            return True
        return False

def is_in_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        data = gcoldb.get(str(keywoard), [])
        return list(contents) in data

def del_keyword_collectionlist(keywoard):
    with CAT_GLOBALCOLLECTION:
        gcoldb.delete(str(keywoard))

def get_item_collectionlist(keywoard):
    return set(tuple(x) for x in gcoldb.get(str(keywoard), []))

def get_collectionlist_items():
    return list(gcoldb.get_all().keys())

def num_collectionlist():
    total = 0
    for v in gcoldb.get_all().values():
        total += len(v)
    return total

def num_collectionlist_item(keywoard):
    return len(gcoldb.get(str(keywoard), []))

def num_collectionlist_items():
    return len(gcoldb.get_all())
