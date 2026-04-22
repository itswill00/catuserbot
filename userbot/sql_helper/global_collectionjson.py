# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import JsonDB

gcoldb = JsonDB("cat_collections")

class Cat_GlobalCollection_Json:
    def __init__(self, keywoard, json, njson):
        self.keywoard = keywoard
        self.json = json
        self.njson = njson

def get_collection(keywoard):
    res = gcoldb.get(str(keywoard))
    if res:
        return Cat_GlobalCollection_Json(keywoard, res["json"], res["njson"])
    return None

def add_collection(keywoard, json, njson=None):
    if njson is None:
        njson = {}
    gcoldb.set(str(keywoard), {"json": json, "njson": njson})
    return True

def del_collection(keywoard):
    if gcoldb.get(str(keywoard)):
        gcoldb.delete(str(keywoard))
        return True
    return False

def get_collections():
    raw_data = gcoldb.get_all()
    return [Cat_GlobalCollection_Json(k, v["json"], v["njson"]) for k, v in raw_data.items()]
