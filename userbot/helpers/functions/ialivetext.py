import math
import time

import heroku3
import requests

from ...Config import Config
from .utils import get_readable_time

# Heroku is optional for local deployments
Heroku = None
if Config.HEROKU_API_KEY:
    try:
        Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
    except Exception:
        Heroku = None
heroku_api = "https://api.heroku.com"

# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg

def check_data_base_heal_th():
    # Check for Local JSON DB
    from ... import sql_helper
    if sql_helper.SESSION is None:
        return True, "Functioning (Local JSON DB)"
    
    # Check for SQL DB
    if not Config.DB_URI:
        return False, "No Database set"

    try:
        sql_helper.SESSION.execute("SELECT 1")
        return True, "Functioning (SQL)"
    except Exception as e:
        return False, f"❌ {e}"


async def catalive(StartTime):
    _, check_sgnirts = check_data_base_heal_th()
    sudo = "Enabled" if Config.SUDO_USERS else "Disabled"
    uptime = await get_readable_time((time.time() - StartTime))
    dyno = "N/A (Local)"
    
    if Heroku and Config.HEROKU_API_KEY and Config.HEROKU_APP_NAME:
        try:
            useragent = (
                "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/80.0.3987.149 Mobile Safari/537.36"
            )
            user_id = Heroku.account().id
            headers = {
                "User-Agent": useragent,
                "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
                "Accept": "application/vnd.heroku+json; version=3.account-quotas",
            }
            path = f"/accounts/{user_id}/actions/get-quota"
            r = requests.get(heroku_api + path, headers=headers)
            result = r.json()
            quota = result["account_quota"]
            quota_used = result["quota_used"]

            # Used
            remaining_quota = quota - quota_used
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)
            # Current
            App = result["apps"]
            try:
                AppQuotaUsed = App[0]["quota_used"] / 60
            except (IndexError, KeyError):
                AppQuotaUsed = 0
                
            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)
            dyno = f"{AppHours}h {AppMinutes}m/{hours}h {minutes}m"
        except Exception as e:
            dyno = f"Error: {e}"

    return f"🖤༄ Catuserbot Stats ༄🖤\
                 \n\nღ Database : {check_sgnirts}\
                  \nღ Sudo : {sudo}\
                  \nღ Uptime : {uptime}\
                  \nღ Dyno : {dyno}\
                  "
