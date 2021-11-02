#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) New-dev0 2021
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from bot import AUTH_CHANNEL, COMMM_AND_PRE_FIX, BROADCAST_COMMAND
from bot.bot import Bot
from bot.hf.flifi import uszkhvis_chats_ahndler
from bot.sql.users_sql import get_chats

@Bot.on_message(
    filters.command('users')
    & uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def num_start_users(client: Bot, message: Message):
    await message.reply(f'<code>{len(get_chats())}</code> users are using this bot')

@Bot.on_message(
    filters.command(BROADCAST_COMMAND, COMMM_AND_PRE_FIX)
    & uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def num_start_message(client: Bot, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to Message..", quote=True)
    reply = message.reply_to_message
    All = get_chats()
    TTL = len(All)
    SUCCESS = 0
    FAILED = 0
    sts = await message.reply('<i>Please Wait..</i>')
    for chat in All:
        try:
            await reply.copy(chat)
            SUCCESS += 1
        except FloodWait as a:
            time.sleep(a.x)
            await reply.copy(chat)
            SUCCESS += 1
        except Exception as e:
            print(e, chat)
            FAILED += 1
        try:
            text = f"""<b><u>Broadcast Progress..</u>

Total Users: {len(All)}
Success: {SUCCESS}
Failed: {FAILED}"""
            await sts.edit(text)
        except:
            pass

    MSG = f"""<b><u>BroadCast Completed</u>

Total Users: {len(All)}
Success: {SUCCESS}
Failed: {FAILED}"""
    try:
        await sts.edit(MSG)
    except FloodWait as a:
        time.sleep(a.x)
        await sts.edit(MSG)
