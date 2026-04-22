# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .json_db import locks_db as ldb

class Locks:
    def __init__(self, chat_id, bots=False, commands=False, email=False, forward=False, url=False):
        self.chat_id = str(chat_id)
        self.bots = bots
        self.commands = commands
        self.email = email
        self.forward = forward
        self.url = url

def init_locks(chat_id, reset=False):
    chat_id = str(chat_id)
    if reset:
        ldb.delete(chat_id)
    new_lock = {"bots": False, "commands": False, "email": False, "forward": False, "url": False}
    ldb.set(chat_id, new_lock)
    return Locks(chat_id)

def update_lock(chat_id, lock_type, locked):
    chat_id = str(chat_id)
    curr_perm = ldb.get(chat_id)
    if not curr_perm:
        curr_perm = {"bots": False, "commands": False, "email": False, "forward": False, "url": False}
    
    if lock_type in curr_perm:
        curr_perm[lock_type] = locked
        ldb.set(chat_id, curr_perm)
    return True

def is_locked(chat_id, lock_type):
    curr_perm = ldb.get(str(chat_id))
    if not curr_perm:
        return False
    return curr_perm.get(lock_type, False)

def get_locks(chat_id):
    res = ldb.get(str(chat_id))
    if res:
        return Locks(chat_id, **res)
    return None
