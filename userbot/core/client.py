# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import datetime
import inspect
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Union

from telethon import TelegramClient, events
from telethon.errors import (
    AlreadyInConversationError,
    BotInlineDisabledError,
    BotResponseTimeoutError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

from ..Config import Config
from ..helpers.utils.events import checking
from ..helpers.utils.format import paste_message
from ..helpers.utils.utils import runcmd
from ..sql_helper.globals import gvarstatus
from . import BOT_INFO, CMD_INFO, GRP_INFO, LOADED_CMDS, PLG_INFO
from .cmdinfo import _format_about
from .data import (
    _sudousers_list,
    _vcusers_list,
    blacklist_chats_list,
    sudo_enabled_cmds,
)
from .events import MessageEdited, NewMessage, edit_message, send_file, send_message
from .fasttelethon import download_file, upload_file
from .logger import logging
from .managers import edit_delete
from .pluginManager import get_message_link, restart_script

LOGS = logging.getLogger(__name__)


class REGEX:
    def __init__(self):
        self.regex = ""
        self.regex1 = ""
        self.regex2 = ""


REGEX_ = REGEX()
sudo_enabledcmds = sudo_enabled_cmds()


class CatUserBotClient(TelegramClient):
    def cat_cmd(
        self: TelegramClient,
        pattern: Union[str, tuple] = None,
        info: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]], tuple] = None,
        groups_only: bool = False,
        private_only: bool = False,
        allow_sudo: bool = True,
        edited: bool = True,
        forword=False,
        disable_errors: bool = False,
        command: Union[str, tuple] = None,
        public: bool = False,
        **kwargs,
    ) -> callable:
        """Enhanced CatUserBot command decorator."""
        if not public:
            kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", forword)
        
        if gvarstatus("blacklist_chats") is not None:
            kwargs["blacklist_chats"] = True
            kwargs["chats"] = blacklist_chats_list()
            
        stack = inspect.stack()
        file_test = Path(stack[1].filename).stem.replace(".py", "")
        
        if command is not None:
            cmd_name, category = command[0], command[1]
            if category not in BOT_INFO:
                BOT_INFO.append(category)
            if file_test not in GRP_INFO.get(category, []):
                GRP_INFO.setdefault(category, []).append(file_test)
            PLG_INFO.setdefault(file_test, []).append(cmd_name)
            if cmd_name not in CMD_INFO:
                CMD_INFO[cmd_name] = [_format_about(info)]

        if pattern is not None:
            if pattern.startswith((r"\#", r"^")):
                REGEX_.regex1 = REGEX_.regex2 = re.compile(pattern)
            else:
                handler = re.escape(Config.COMMAND_HAND_LER)
                sudo_handler = re.escape(Config.SUDO_COMMAND_HAND_LER)
                REGEX_.regex1 = re.compile(f"^{handler}{pattern}")
                REGEX_.regex2 = re.compile(f"^{sudo_handler}{pattern}")

        def decorator(func):  # sourcery no-metrics
            async def wrapper(check):  # sourcery no-metrics
                # sourcery skip: low-code-quality
                if groups_only and not check.is_group:
                    return await edit_delete(check, "`I don't think this is a group.`")
                if private_only and not check.is_private:
                    return await edit_delete(
                        check, "`I don't think this is a personal Chat.`"
                    )
                try:
                    await func(check)
                except events.StopPropagation as e:
                    raise events.StopPropagation from e
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("Message was same as previous message")
                except MessageIdInvalidError:
                    LOGS.error("Message was deleted or cant be found")
                except BotInlineDisabledError:
                    await edit_delete(check, "`Turn on Inline mode for our bot`")
                except ChatSendStickersForbiddenError:
                    await edit_delete(
                        check, "`I guess i can't send stickers in this chat`"
                    )
                except BotResponseTimeoutError:
                    await edit_delete(
                        check, "`The bot didnt answer to your query in time`"
                    )
                except ChatSendMediaForbiddenError:
                    await edit_delete(check, "`You can't send media in this chat`")
                except AlreadyInConversationError:
                    return await edit_delete(
                        check,
                        "`A conversation is already happening with the given chat. try again after some time.`",
                    )
                except ChatSendInlineForbiddenError:
                    await edit_delete(
                        check, "`You can't send inline messages in this chat.`"
                    )
                except FloodWaitError as e:
                    LOGS.error(
                        f"A flood wait of {e.seconds} occured. "
                        f"wait for {e.seconds} seconds and try"
                    )
                    await check.delete()
                    await asyncio.sleep(e.seconds + 5)
                except ConnectionError as e:
                    LOGS.error(f"Connection error: {e}")
                    await edit_delete(check, "`Connection error occurred. Retrying...`")
                except TimeoutError as e:
                    LOGS.error(f"Request timeout: {e}")
                    await edit_delete(check, "`Request timed out. Please try again.`")
                except PermissionError as e:
                    LOGS.error(f"Permission denied: {e}")
                    await edit_delete(check, "`I don't have permission to do that.`")
                except Exception as e:
                    # Log the error with metadata; the native TelegramLogHandler will handle the rest
                    msg_link = await check.client.get_msg_link(check) if hasattr(check.client, 'get_msg_link') else "N/A"
                    error_metadata = (
                        f"Plugin: {func.__name__}\n"
                        f"Chat: {check.chat_id}\n"
                        f"Sender: {check.sender_id}\n"
                        f"Link: {msg_link}\n"
                        f"Event: {check.text[:100]}"
                    )
                    LOGS.exception(f"Plugin error in {func.__name__}\n{error_metadata}")

            from .session import catub

            if func.__doc__ is not None:
                CMD_INFO[command[0]].append((func.__doc__).strip())
            if pattern is not None:
                if command is not None:
                    if command[0] in LOADED_CMDS and wrapper in LOADED_CMDS[command[0]]:
                        return None
                    try:
                        LOADED_CMDS[command[0]].append(wrapper)
                    except BaseException:
                        LOADED_CMDS.update({command[0]: [wrapper]})
                if edited:
                    catub.add_event_handler(
                        wrapper,
                        MessageEdited(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
                catub.add_event_handler(
                    wrapper,
                    NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                )
                if public:
                    if edited:
                        catub.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex2,
                                from_users=_vcusers_list(),
                                **kwargs,
                            ),
                        )
                    catub.add_event_handler(
                        wrapper,
                        NewMessage(
                            pattern=REGEX_.regex2, from_users=_vcusers_list(), **kwargs
                        ),
                    )
                if (
                    allow_sudo
                    and gvarstatus("sudoenable") is not None
                    and (command is None or command[0] in sudo_enabledcmds)
                ):
                    if edited:
                        catub.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex2,
                                from_users=_sudousers_list(),
                                **kwargs,
                            ),
                        )
                    catub.add_event_handler(
                        wrapper,
                        NewMessage(
                            pattern=REGEX_.regex2,
                            from_users=_sudousers_list(),
                            **kwargs,
                        ),
                    )
            else:
                if file_test in LOADED_CMDS and func in LOADED_CMDS[file_test]:
                    return None
                try:
                    LOADED_CMDS[file_test].append(func)
                except BaseException:
                    LOADED_CMDS.update({file_test: [func]})
                if edited:
                    catub.add_event_handler(func, events.MessageEdited(**kwargs))
                catub.add_event_handler(func, events.NewMessage(**kwargs))
            return wrapper

        return decorator

    def bot_cmd(
        self: TelegramClient,
        disable_errors: bool = False,
        edited: bool = False,
        forword=False,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", forword)

        def decorator(func):
            async def wrapper(check):
                try:
                    await func(check)
                except events.StopPropagation as e:
                    raise events.StopPropagation from e
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("Message was same as previous message")
                except MessageIdInvalidError:
                    LOGS.error("Message was deleted or cant be found")
                except BaseException as e:
                    # Check if we have to disable error logging.
                    LOGS.exception(e)  # Log the error in console
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = f"\nDisclaimer:\nThis file is pasted only here ONLY here,\
                                    \nwe logged only fact of error and date,\nwe respect your privacy,\
                                    \nyou may not report this error if you've\
                                    \nany confidential data here, no one will see your data\
                                    \n\n--------BEGIN USERBOT TRACEBACK LOG--------\
                                    \nDate: {date}\nGroup ID: {str(check.chat_id)}\
                                    \nSender ID: {str(check.sender_id)}\
                                    \nMessage Link: {await check.client.get_msg_link(check)}\
                                    \n\nEvent Trigger:\n{str(check.text)}\
                                    \n\nTraceback info:\n{str(traceback.format_exc())}\
                                    \n\nError text:\n{str(sys.exc_info()[1])}"
                        new = {
                            "error": str(sys.exc_info()[1]),
                            "date": datetime.datetime.now(),
                        }
                        ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"
                        command = 'git log --pretty=format:"%an: %s" -5'
                        ftext += "\n\n\nLast 5 commits:\n"
                        output = (await runcmd(command))[:2]
                        result = output[0] + output[1]
                        ftext += result
                        pastelink = await paste_message(
                            ftext, pastetype="s", markdown=False
                        )
                        link = "[here](https://t.me/catuserbot_support)"
                        text = (
                            "**CatUserbot Error report**\n\n"
                            + "If you wanna you can report it"
                        )
                        text += f"- just forward this message {link}.\n"
                        text += (
                            "Nothing is logged except the fact of error and date\n\n"
                        )
                        text += f"**Error report : ** [{new['error']}]({pastelink})"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                        )

            from .session import catub

            if edited:
                catub.tgbot.add_event_handler(func, events.MessageEdited(**kwargs))
            else:
                catub.tgbot.add_event_handler(func, events.NewMessage(**kwargs))

            return wrapper

        return decorator

    async def get_traceback(self, exc: Exception) -> str:
        return "".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )

    def _kill_running_processes(self) -> None:
        """Kill all the running asyncio subprocessess"""
        for _, process in self.running_processes.items():
            try:
                process.kill()
                LOGS.debug("Killed %d which was still running.", process.pid)
            except Exception as e:
                LOGS.debug(e)
        self.running_processes.clear()


CatUserBotClient.fast_download_file = download_file
CatUserBotClient.fast_upload_file = upload_file
CatUserBotClient.reload = restart_script
CatUserBotClient.get_msg_link = get_message_link
CatUserBotClient.check_testcases = checking
try:
    send_message_check = TelegramClient.send_message
except AttributeError:
    CatUserBotClient.send_message = send_message
    CatUserBotClient.send_file = send_file
    CatUserBotClient.edit_message = edit_message
