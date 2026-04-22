# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
from datetime import datetime

from telethon.tl import functions, types

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"

LOGS = logging.getLogger(__name__)

# Temporary in-memory cache for messages that should be deleted
# (Persistent deletion across restarts is complex, so we keep this in-memory)
LAST_AFK_MESSAGE = {}

def get_afk_time(start_time):
    if not start_time:
        return "Unknown"
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.now().replace(microsecond=0)
        total_afk_time = end - start
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        res = ""
        if d > 0: res += f"{d}d {h}h {m}m {s}s"
        elif h > 0: res += f"{h}h {m}m {s}s"
        else: res += f"{m}m {s}s" if m > 0 else f"{s}s"
        return res
    except Exception:
        return "Unknown"

@catub.cat_cmd(outgoing=True, edited=False)
async def set_not_afk(event):
    if not gvarstatus("afk_on"):
        return
    
    msg_text = event.message.message.lower()
    # Don't turn off AFK if message is the AFK command itself or contains #afk
    if msg_text.startswith(f"{Config.COMMAND_HAND_LER}afk") or \
       msg_text.startswith(f"{Config.COMMAND_HAND_LER}mafk") or \
       "#afk" in msg_text:
        return

    endtime = get_afk_time(gvarstatus("afk_start"))
    
    # Clear AFK status from DB
    delgvar("afk_on")
    delgvar("afk_start")
    delgvar("afk_reason")
    delgvar("afk_type")
    delgvar("afk_media")

    back_msg = await event.client.send_message(
        event.chat_id,
        f"`Back alive! No Longer afk.\nWas afk for {endtime}`",
    )
    
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#AFKFALSE \n`Set AFK mode to False\nBack alive! No Longer afk.\nWas afk for {endtime}`",
        )
    
    await asyncio.sleep(5)
    await back_msg.delete()

@catub.cat_cmd(
    incoming=True, func=lambda e: bool(e.mentioned or e.is_private), edited=False
)
async def on_afk(event):
    if not gvarstatus("afk_on"):
        return
    
    if event.sender_id == catub.uid:
        return

    msg_text = event.message.message.lower()
    if "#afk" in msg_text:
        return

    sender = await event.get_sender()
    if not sender or sender.bot:
        return

    endtime = get_afk_time(gvarstatus("afk_start"))
    reason = gvarstatus("afk_reason") or "Not Mentioned ( ಠ ʖ̯ ಠ)"
    afk_type = gvarstatus("afk_type")
    
    if afk_type == "media":
        media_link = gvarstatus("afk_media")
        message_to_reply = f"`I am AFK .\n\nAFK Since {endtime}\nReason : {reason}`"
        msg = await event.reply(message_to_reply, file=media_link)
    else:
        message_to_reply = f"`I am AFK .\n\nAFK Since {endtime}\nReason : {reason}`"
        msg = await event.reply(message_to_reply)

    # Clean up previous reply in this chat
    if event.chat_id in LAST_AFK_MESSAGE:
        try:
            await LAST_AFK_MESSAGE[event.chat_id].delete()
        except Exception:
            pass
    LAST_AFK_MESSAGE[event.chat_id] = msg

    # Log tags to PM_LOGGER_GROUP if configured
    if not event.is_private and Config.PM_LOGGER_GROUP_ID != 0:
        chat = await event.get_chat()
        m_type = await media_type(event)
        resalt = f"#AFK_TAGS \n<b>Group : </b><code>{chat.title}</code>"
        resalt += f"\n<b>From : </b> 👤{_format.htmlmentionuser(sender.first_name , sender.id)}"
        if m_type:
            resalt += f"\n<b>Message type : </b><code>{m_type}</code>"
        else:
            resalt += f"\n<b>Message : </b>{event.message.message[:200]}"
        resalt += f"\n<b>Message link: </b><a href='https://t.me/c/{chat.id}/{event.message.id}'> link</a>"
        
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )

@catub.cat_cmd(
    pattern="afk(?:\s|$)([\s\S]*)",
    command=("afk", plugin_category),
    info={
        "header": "Enables afk for your account",
        "description": "Mark yourself as Away From Keyboard. The bot will automatically reply to mentions and PMs.",
        "usage": "{tr}afk <reason>",
    },
)
async def set_afk(event):
    reason = event.pattern_match.group(1)
    
    addgvar("afk_on", True)
    addgvar("afk_start", datetime.now().isoformat())
    addgvar("afk_reason", reason)
    addgvar("afk_type", "text")
    
    await edit_delete(event, f"`I shall be Going afk! {'Reason: ' + reason if reason else ''}`", 5)
    
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#AFKTRUE \nSet AFK mode to True. Alasan: {reason if reason else 'None'}",
        )

@catub.cat_cmd(
    pattern="mafk(?:\s|$)([\s\S]*)",
    command=("mafk", plugin_category),
    info={
        "header": "Enables media afk for your account",
        "description": "Mark yourself as AFK with a media reply (photo/video/gif). Reply to the media.",
        "usage": "{tr}mafk <reason> (reply to media)",
    },
)
async def set_mafk(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await edit_or_reply(event, "`Reply to media to activate media AFK!`")
        
    if not BOTLOG:
        return await edit_or_reply(event, "`BOTLOG needs to be enabled for media AFK!`")

    reason = event.pattern_match.group(1)
    
    # Forward media to botlog to get a permanent link/id
    media_msg = await reply.forward_to(BOTLOG_CHATID)
    
    addgvar("afk_on", True)
    addgvar("afk_start", datetime.now().isoformat())
    addgvar("afk_reason", reason)
    addgvar("afk_type", "media")
    # Store the link to the forwarded media in botlog
    media_link = f"https://t.me/c/{str(BOTLOG_CHATID)[4:]}/{media_msg.id}"
    addgvar("afk_media", media_link)
    
    await edit_delete(event, f"`I shall be Going afk (Media)! {'Reason: ' + reason if reason else ''}`", 5)
    
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#AFKTRUE (MEDIA) \nSet AFK mode to True. Alasan: {reason if reason else 'None'}",
        )
