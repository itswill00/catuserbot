# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging
import asyncio
import traceback

class TelegramLogHandler(logging.Handler):
    def __init__(self, chat_id=None):
        super().__init__()
        self.chat_id = chat_id
        self.client = None
        self.buffer = []
        self.loop = None
        self.is_flushing = False

    def set_client(self, client, chat_id):
        self.client = client
        self.chat_id = chat_id
        self.loop = asyncio.get_event_loop()
        # Flush existing buffer
        if self.buffer:
            self.loop.create_task(self.flush_buffer())

    def emit(self, record):
        # AVOID FEEDBACK LOOP: Do not log messages from telethon or the logger itself
        if record.name.startswith(("telethon", "urllib3", "aiohttp")):
            return

        log_entry = self.format(record)
        
        # Add emoji based on level
        if record.levelno >= logging.ERROR:
            log_entry = f"🔴 **ERROR**\n{log_entry}"
            if record.exc_info:
                log_entry += f"\n\n**Traceback:**\n`{traceback.format_exc()}`"
        elif record.levelno >= logging.WARNING:
            log_entry = f"⚠️ **WARNING**\n{log_entry}"
        else:
            log_entry = f"ℹ️ **INFO**\n{log_entry}"

        if self.client and self.chat_id and self.loop:
            self.loop.create_task(self.send_log(log_entry))
        else:
            self.buffer.append(log_entry)

    async def send_log(self, message):
        try:
            if self.client and self.chat_id:
                # Truncate if too long for Telegram
                if len(message) > 4000:
                    message = message[:3900] + "\n... (truncated)"
                await self.client.send_message(self.chat_id, message)
        except Exception:
            # Fallback to console if telegram fails
            pass

    async def flush_buffer(self):
        if self.is_flushing or not self.buffer:
            return
        self.is_flushing = True
        try:
            # Combine multiple logs if possible to avoid flood
            while self.buffer:
                chunk = []
                current_len = 0
                while self.buffer and current_len + len(self.buffer[0]) < 4000:
                    msg = self.buffer.pop(0)
                    chunk.append(msg)
                    current_len += len(msg) + 2
                
                if chunk:
                    await self.send_log("\n\n---\n\n".join(chunk))
                    await asyncio.sleep(2) # Delay to avoid flood
        finally:
            self.is_flushing = False

# Global handler instance
tg_handler = TelegramLogHandler()
tg_handler.setLevel(logging.WARNING) # ONLY send Warnings and Errors to Telegram

# Base Logging to File and Console ONLY
logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    handlers=[logging.FileHandler("catub.log"), logging.StreamHandler()],
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

# Attach TG Handler ONLY to CatUserbot specific loggers to avoid library spam/loops
cat_logger = logging.getLogger("CatUserbot")
cat_logger.addHandler(tg_handler)

# Suppress library logs
logging.getLogger("telethon.client.updates").setLevel(logging.WARNING)
logging.getLogger("telethon.network").setLevel(logging.WARNING)
