import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot import LOGS

from ..Config import Config

PING_URL = Config.UPTIME_PING_URL


def ping():
    try:
        r = requests.get(PING_URL, timeout=10)
        LOGS.info(f"[UPTIME PINGER] Pinged {PING_URL} - Status {r.status_code}")
    except Exception as e:
        LOGS.info(f"[UPTIME PINGER] Failed: {e}")


def start_uptime_pinger():
    if not PING_URL:
        LOGS.info("No PING URL set, skipping uptime pinger")
        return

    scheduler = AsyncIOScheduler()
    scheduler.add_job(ping, "interval", minutes=1, next_run_time=None)
    scheduler.start()
