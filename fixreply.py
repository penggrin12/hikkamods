# The MIT License (MIT)
#
# Copyright (c) 2022 penggrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# meta developer: @penggrin
# scope: hikka_only

from telethon.tl.types import Message
from .. import loader, utils
import logging, asyncio

logger = logging.getLogger(__name__)


@loader.tds
class FixReplyMod(loader.Module):
    """Fixes ya replies""" # ❎✅

    strings = {
        "name": "FixReply",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.lastMessage = None

    @loader.watcher(out=True, only_messages=True, no_commands=True)
    async def newMessage(self, message: Message):
        self.lastMessage = message

    async def fixreplycmd(self, message: Message):
        """Respond to a message to fix your last message reply"""
        reply = await message.get_reply_message()

        if not self.lastMessage:
            await utils.answer(message, "❎ чел ты ничего не писал")
            return

        if not reply:
            await utils.answer(message, "❎ чел ты забыл ответить на нужное сообщение")
            return

        await utils.answer(message, self.lastMessage.raw_text)
        await self.lastMessage.delete()
