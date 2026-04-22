# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import os
import sys
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import UPSTREAM_REPO_URL, catub
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "tools"
cmdhd = Config.COMMAND_HAND_LER
LOGS = logging.getLogger(__name__)

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)

async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )

async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True

async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

async def update_bot(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    
    await update_requirements()
    sandy = await event.edit(
        "`Successfully Updated!\n" "Bot is restarting... Wait for a minute!`"
    )
    
    # Reload codebase for VPS
    if os.path.exists("config.py"):
        from userbot.plugins.vps import reload_codebase
        await reload_codebase()
        
    await event.client.reload(sandy)

@catub.cat_cmd(
    pattern="update(| now)?$",
    command=("update", plugin_category),
    info={
        "header": "To update userbot.",
        "description": "Checks for updates or updates the bot.",
        "options": {
            "now": "Will pull updates and restart the bot.",
        },
        "usage": [
            "{tr}update",
            "{tr}update now",
        ],
    },
)
async def upstream(event):
    "To check if the bot is up to date and update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`Checking for updates, please wait....`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    
    try:
        txt = "`Oops.. Updater cannot continue due to some problems occured`"
        repo = Repo()
    except NoSuchPathError as error:
        return await event.edit(f"{txt}\n`directory {error} is not found`")
    except GitCommandError as error:
        return await event.edit(f"{txt}\n`Early failure! {error}`")
    except InvalidGitRepositoryError:
        if conf != "now":
            return await event.edit(
                "`The current directory is not a git repository. Use .update now to force sync.`"
            )

        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
        
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        return await event.edit(f"`Custom branch detected ({ac_br}). Please switch to the official branch to update.`")
        
    try:
        repo.create_remote("upstream", off_repo)
    except Exception:
        pass
        
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    
    if changelog == "" and not force_update:
        return await event.edit(f"\n`CATUSERBOT is up-to-date with {UPSTREAM_REPO_BRANCH}`\n")
        
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        return await event.respond(f"Do `{cmdhd}update now` to update the catuserbot")

    if conf == "now" or force_update:
        await event.edit("`Updating userbot, please wait....`")
        await update_bot(event, repo, ups_rem, ac_br)
