# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# We are now using Local JSON DB.
# Dummy BASE and SESSION to prevent crashes in SQL-based models
class DummyBase:
    __table__ = type('Table', (), {'create': lambda *a, **k: None})()
    def __init__(self, *args, **kwargs):
        pass

BASE = DummyBase

class DummySession:
    def execute(self, *args, **kwargs): return None
    def merge(self, *args, **kwargs): return None
    def commit(self, *args, **kwargs): return None
    def query(self, *args, **kwargs): return self
    def get(self, *args, **kwargs): return None
    def filter(self, *args, **kwargs): return self
    def delete(self, *args, **kwargs): return None
    def all(self, *args, **kwargs): return []
    def first(self, *args, **kwargs): return None
    def distinct(self, *args, **kwargs): return self
    def scalar(self, *args, **kwargs): return 0
    def count(self, *args, **kwargs): return 0
    def close(self, *args, **kwargs): return None

SESSION = DummySession()

LOGS.info("Database system: LOCAL JSON DB (Self-contained)")
