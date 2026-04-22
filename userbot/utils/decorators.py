# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import datetime
import inspect
import re
import sys
import traceback
from pathlib import Path

from .. import CMD_LIST, LOAD_PLUG, SUDO_LIST
from ..Config import Config
from ..core.data import _sudousers_list, blacklist_chats_list
from ..core.events import MessageEdited, NewMessage
from ..core.logger import logging
from ..core.session import catub
from ..helpers.utils.format import paste_message
from ..helpers.utils.utils import runcmd
from ..sql_helper.globals import gvarstatus

LOGS = logging.getLogger(__name__)


def admin_cmd(pattern=None, command=None, **args):  # sourcery no-metrics
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            if len(Config.COMMAND_HAND_LER) == 2:
                catreg = f"^{Config.COMMAND_HAND_LER}"
                reg = Config.COMMAND_HAND_LER[1]
            elif len(Config.COMMAND_HAND_LER) == 1:
                catreg = f"^\\{Config.COMMAND_HAND_LER}"
                reg = Config.COMMAND_HAND_LER
            args["pattern"] = re.compile(catreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        del args["allow_sudo"]
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    if gvarstatus("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return NewMessage(**args)


def sudo_cmd(pattern=None, command=None, **args):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            if len(Config.SUDO_COMMAND_HAND_LER) == 2:
                catreg = f"^{Config.SUDO_COMMAND_HAND_LER}"
                reg = Config.SUDO_COMMAND_HAND_LER[1]
            elif len(Config.SUDO_COMMAND_HAND_LER) == 1:
                catreg = f"^\\{Config.SUDO_COMMAND_HAND_LER}"
                reg = Config.COMMAND_HAND_LER
            args["pattern"] = re.compile(catreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(_sudousers_list())
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]
    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    # add blacklist chats, UB should not respond in these chats
    if gvarstatus("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()
    # add blacklist chats, UB should not respond in these chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    # check if the plugin should listen for outgoing 'messages'
    if gvarstatus("sudoenable") is not None:
        return NewMessage(**args)


def errors_handler(func):
    async def wrapper(event):
        try:
            await func(event)
        except Exception as e:
            # Only report errors if BOTLOG is enabled
            if Config.PRIVATE_GROUP_BOT_API_ID == 0 or not Config.BOTLOG:
                LOGS.error(f"Error in {func.__name__}: {e}", exc_info=True)
                return
            
            try:
                date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                ftext = (
                    f"\nDisclaimer:\n"
                    f"This file is pasted only here ONLY here,\n"
                    f"we logged only fact of error and date,\n"
                    f"we respect your privacy,\n"
                    f"you may not report this error if you've\n"
                    f"any confidential data here, no one will see your data\n\n"
                    f"--------BEGIN USERBOT TRACEBACK LOG--------\n"
                    f"Date: {date}\n"
                    f"Plugin: {func.__name__}\n"
                    f"Group ID: {str(event.chat_id)}\n"
                    f"Sender ID: {str(event.sender_id)}\n\n"
                    f"Event Trigger:\n{str(event.text)}\n\n"
                    f"Traceback info:\n{str(traceback.format_exc())}\n\n"
                    f"Error text:\n{str(sys.exc_info()[1])}"
                )
                
                ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"
                
                try:
                    command = 'git log --pretty=format:"%an: %s" -5'
                    output = (await runcmd(command))[:2]
                    result = output[0] + output[1]
                    ftext += f"\n\nLast 5 commits:\n{result}"
                except Exception as git_err:
                    LOGS.warning(f"Could not append git log: {git_err}")
                
                pastelink = await paste_message(ftext)
                link = "[here](https://t.me/catuserbot_support)"
                text = (
                    "**CatUserbot Error report**\n\n"
                    f"If you wanna, you can report it {link}.\n"
                    "Nothing is logged except the fact of error and date\n\n"
                    f"**Error report:** [{sys.exc_info()[1]}]({pastelink})"
                )
                await event.client.send_message(
                    Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                )
            except Exception as report_err:
                LOGS.error(f"Failed to send error report: {report_err}", exc_info=True)

    return wrapper


def register(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", True)
    allow_sudo = args.get("allow_sudo", False)

    # Make pattern case-insensitive if not already
    if pattern is not None and not pattern.startswith("(?i)"):
        try:
            args["pattern"] = f"(?i){pattern}"
        except (TypeError, AttributeError) as e:
            LOGS.warning(f"Invalid pattern: {e}")

    if "disable_edited" in args:
        del args["disable_edited"]

    reg = re.compile("(.*)")
    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            if cmd:
                cmd = cmd[1].replace("$", "").replace("\\", "").replace("^", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except KeyError:
                CMD_LIST.update({file_test: [cmd]})
        except (TypeError, AttributeError) as e:
            LOGS.debug(f"Could not process pattern: {e}")
    
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    if gvarstatus("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()

    def decorator(func):
        if not disable_edited:
            catub.add_event_handler(func, MessageEdited(**args))
        catub.add_event_handler(func, NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except KeyError:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def command(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", None)
    allow_edited_updates = args.get("allow_edited_updates", False)
    args["incoming"] = args.get("incoming", False)
    args["outgoing"] = True
    if bool(args["incoming"]):
        args["outgoing"] = False
    # Make pattern case-insensitive if not already
    try:
        if pattern is not None and not pattern.startswith("(?i)"):
            args["pattern"] = f"(?i){pattern}"
    except (TypeError, AttributeError) as e:
        LOGS.warning(f"Invalid pattern format: {e}")
    
    reg = re.compile("(.*)")
    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            if cmd:
                cmd = cmd[1].replace("$", "").replace("\\", "").replace("^", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except KeyError:
                CMD_LIST.update({file_test: [cmd]})
        except (TypeError, AttributeError) as e:
            LOGS.debug(f"Could not process command pattern: {e}")
    
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
    del allow_sudo
    try:
        del args["allow_sudo"]
    except KeyError:
        pass
    
    if gvarstatus("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()

    def decorator(func):
        if allow_edited_updates:
            catub.add_event_handler(func, MessageEdited(**args))
        catub.add_event_handler(func, NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except KeyError:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator
