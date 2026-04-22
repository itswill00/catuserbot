import time
from ...Config import Config
from .utils import get_readable_time

def check_data_base_heal_th():
    # CatUserbot now uses Local JSON DB by default
    return True, "Functioning (Local JSON DB)"

async def catalive(StartTime):
    _, check_sgnirts = check_data_base_heal_th()
    sudo = "Enabled" if Config.SUDO_USERS else "Disabled"
    uptime = await get_readable_time((time.time() - StartTime))
    
    return f"🖤༄ Catuserbot Stats ༄🖤\
                 \n\nღ Database : {check_sgnirts}\
                  \nღ Sudo : {sudo}\
                  \nღ Uptime : {uptime}\
                  "
