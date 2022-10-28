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
import logging

logger = logging.getLogger(__name__)


@loader.tds
class TelethonChatManager(loader.Module):
    """Basic Telethon Chat Manager"""

    strings = {
        "name": "TelethonChatManager",
    }

    def list_to_str(self, a = None):
        if (a is None) or (len(a) < 1):
            return ""

        return ' '.join(str(b) for b in a)

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delete_cmds",
                True,
                lambda: "Delete the messages TelethonChat-Manager sends?",
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def __telethoncommand(self, command: str, message: Message, force_reply=None, delete_result=True, use_args=True):
        reply = await message.get_reply_message() or force_reply
        if use_args:
            args = self.list_to_str(utils.get_args(message))
        else:
            args = ""
        if reply:
            result = await reply.reply(f"{command} {args}")
        else:
            result = await message.respond(f"{command} {args}")
        await message.delete()
        if delete_result and self.config["delete_cmds"]:
            await result.delete()
        #return result

    async def truscmd(self, message: Message):
        """- Подсказать пользователю что русский чат существует"""
        await self.__telethoncommand("Just so you know, there is a Russian Telethon Chat\n@TelethonRussian", message, delete_result=False)

    async def tengcmd(self, message: Message):
        """- Уведомить пользователя что в этом чате нужно общатся только на английском"""
        await self.__telethoncommand("Please speak English!", message, delete_result=False)

    async def taskcmd(self, message: Message):
        """- Уведомить пользователя о том что его вопрос хуета"""
        await self.__telethoncommand("#ask", message)

    async def tlearncmd(self, message: Message):
        """- Уведомить пользователя о том что он нихуя не шарит в пайтоне"""
        await self.__telethoncommand("#learn", message)

    async def tofftopcmd(self, message: Message):
        """- Уведомить пользователя о том что он тут нельзя оффтопить"""
        await self.__telethoncommand("#ot", message)

    async def tlogscmd(self, message: Message):
        """- Уведомить пользователя о том что ему нужно включить логгинг"""
        await self.__telethoncommand("#logs", message)

    async def trtdcmd(self, message: Message):
        """- Уведомить пользователя о том что ему нужно прочитать документацию"""
        await self.__telethoncommand("#rtd", message)

    async def treportcmd(self, message: Message):
        """<user OR reply> - Пожаловаться на пользователя"""
        await self.__telethoncommand("#report", message)

    async def tv1cmd(self, message: Message):
        """- Уведомить пользователя о том что то что ему нужно нету в V1"""
        await self.__telethoncommand("#v1", message)

    async def tspamcmd(self, message: Message):
        """- Уведомить пользователя о том что спамерам тут не рады"""
        await self.__telethoncommand("#spam", message)

        