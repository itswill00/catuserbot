# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import signal
import sys
import time

import heroku3

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .helpers.functions.converter import Convert
from .helpers.functions.musictool import *
from .helpers.utils.utils import runasync
from .sql_helper.globals import addgvar, delgvar, gvarstatus

__version__ = "3.3.0"
__license__ = "GNU Affero General Public License v3.0"
__author__ = "CatUserBot <https://github.com/TgCatUB/catuserbot>"
__copyright__ = f"Copyright (C) 2020 - 2023  {__author__}"

catub.version = __version__
catub.tgbot.version = __version__
LOGS = logging.getLogger("CatUserbot")
bot = catub

StartTime = time.time()
catversion = "3.3.0"


def close_connection(*_):
    print("Closing Userbot connection.")
    runasync(catub.disconnect())
    sys.exit(143)


signal.signal(signal.SIGTERM, close_connection)

UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

def _validate_chat_id(chat_id_val, db_key, is_botlog=False):
    """
    Safely validate and convert chat ID from config or database.
    Returns tuple of (chat_id, is_valid)
    """
    try:
        if isinstance(chat_id_val, str):
            chat_id_val = int(chat_id_val)
        
        if not chat_id_val or chat_id_val == 0:
            db_value = gvarstatus(db_key)
            if db_value is None:
                if is_botlog:
                    LOGS.warning(f"{db_key} not configured, logging disabled")
                return (-100, False) if not is_botlog else ("me", False)
            try:
                chat_id_val = int(db_value)
            except (ValueError, TypeError):
                LOGS.error(f"Invalid {db_key} format in database: {db_value}")
                return (-100, False) if not is_botlog else ("me", False)
        
        # Convert positive channel IDs to negative format
        if isinstance(chat_id_val, int) and chat_id_val > 0 and is_botlog:
            chat_id_val = -chat_id_val
        
        return (chat_id_val, True)
    except (ValueError, TypeError) as e:
        LOGS.error(f"Failed to validate {db_key}: {e}")
        return (-100, False) if not is_botlog else ("me", False)

# Validate BOTLOG settings with better error handling
if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    db_value = gvarstatus("PRIVATE_GROUP_BOT_API_ID")
    if db_value is None:
        Config.BOTLOG = False
        Config.BOTLOG_CHATID = "me"
        LOGS.warning("BOTLOG disabled: PRIVATE_GROUP_BOT_API_ID not configured")
    else:
        Config.BOTLOG_CHATID, is_valid = _validate_chat_id(db_value, "PRIVATE_GROUP_BOT_API_ID", True)
        if is_valid:
            Config.PRIVATE_GROUP_BOT_API_ID = Config.BOTLOG_CHATID
            Config.BOTLOG = True
            LOGS.info(f"BOTLOG enabled for chat {Config.BOTLOG_CHATID}")
        else:
            Config.BOTLOG = False
            Config.BOTLOG_CHATID = "me"
else:
    Config.BOTLOG_CHATID, is_valid = _validate_chat_id(Config.PRIVATE_GROUP_BOT_API_ID, "PRIVATE_GROUP_BOT_API_ID", True)
    if is_valid:
        Config.BOTLOG = True
        LOGS.info(f"BOTLOG enabled for chat {Config.BOTLOG_CHATID}")
    else:
        Config.BOTLOG = False
        Config.BOTLOG_CHATID = "me"

# Validate PM_LOGGER settings
if Config.PM_LOGGER_GROUP_ID == 0:
    db_value = gvarstatus("PM_LOGGER_GROUP_ID") or gvarstatus("PM_LOGGR_BOT_API_ID")
    if db_value:
        Config.PM_LOGGER_GROUP_ID, _ = _validate_chat_id(db_value, "PM_LOGGER_GROUP_ID")
    else:
        Config.PM_LOGGER_GROUP_ID = -100
else:
    Config.PM_LOGGER_GROUP_ID, _ = _validate_chat_id(Config.PM_LOGGER_GROUP_ID, "PM_LOGGER_GROUP_ID")

try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# Global Configiables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}

# Variables
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
PM_LOGGER_GROUP_ID = Config.PM_LOGGER_GROUP_ID
