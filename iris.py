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
class IrisManagerMod(loader.Module):
    """Iris Bot Wrapper"""

    strings = {
        "name": "IrisManager",
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
                lambda: "Delete the messages IrisManager sends?",
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client

    async def __iriscommand(self, command: str, message: Message, force_reply = None, delete_result = True, use_args = True):
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

    async def idcmd(self, message: Message):
        """[id] - Возвращает данные о пользователе с помощью его айди, либо с помощью ответа"""
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        target = None

        try:
            if reply:
                target = await self.client.get_input_entity(reply.from_id)
                target = await self.client.get_entity(target)
            else:
                try:
                    target = await self.client.get_input_entity(int(args[0]))
                except:
                    target = await self.client.get_input_entity(args[0])
                target = await self.client.get_entity(target)

            await utils.answer(message, f"{'🤖 Bot' if target.bot else '👨‍🦰 User'}:\n`{target.first_name}` {f'`{target.last_name}`' if target.last_name else ''}\n`{target.id}` {f'(`{target.username}`)' if target.username else ''}", parse_mode = "Markdown")
        except Exception as e:
            logger.warning(f"Cant get information about the user (called by 'id' command)\n{e}")
            await utils.answer(message, f"🚫 Не удалось получить информацию о пользователе\n\n❓ {e}")

    async def idkcmd(self, message: Message):
        """.дк [anything]"""
        await self.__iriscommand(".дк", message)

    async def imdkcmd(self, message: Message):
        """.дк [anything]"""
        await self.__iriscommand(".мдк", message)

    async def itopcmd(self, message: Message):
        """.топ"""
        await self.__iriscommand(".топ", message)

    async def itopacmd(self, message: Message):
        """.топ <count> вся"""
        args = utils.get_args(message)
        await self.__iriscommand(f".топ {args[0] or 15} вся", message, use_args = False)

    async def ipingcmd(self, message: Message):
        """Пинг"""
        await self.__iriscommand(f"Пинг", message, use_args = False)

    async def ibotcmd(self, message: Message):
        """Бот"""
        await self.__iriscommand(f"Бот", message, use_args = False)

    async def istatuscmd(self, message: Message):
        """.актив ириса"""
        await self.__iriscommand(f".актив ириса", message, use_args = False)

    async def iadminscmd(self, message: Message):
        """.админы"""
        await self.__iriscommand(f".админы", message, use_args = False)

    async def ifarmcmd(self, message: Message):
        """ферма"""
        await self.__iriscommand(f"ферма", message, use_args = False)

    async def imeshokcmd(self, message: Message):
        """мешок"""
        await self.__iriscommand(f"мешок", message, use_args = False)

    async def ipcmd(self, message: Message):
        """+ [user]"""
        args = utils.get_args(message)
        last = await self.client.get_messages(message.peer_id, limit=2)
        await self.__iriscommand(f"+", message, force_reply = last[1], delete_result = True, use_args = False)

    async def imcmd(self, message: Message):
        """- [user]"""
        args = utils.get_args(message)
        last = await self.client.get_messages(message.peer_id, limit=2)
        await self.__iriscommand(f"+", message, force_reply = last[1], delete_result = True, use_args = False)

    async def usemecmd(self, message: Message):
        """[anything]"""
        args = utils.get_args(message)
        last = await self.client.get_messages(message.peer_id, limit=2)
        await self.__iriscommand("", message, force_reply = last[1])

    async def iwarncmd(self, message: Message):
        """Варн <user> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Варн {args[0]}\n", message)

    async def iwarntcmd(self, message: Message):
        """Варн <user> <time> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Варн {args[0]} {args[1]}\n", message)

    async def imutecmd(self, message: Message):
        """Мут <user> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Мут {args[0]}\n", message)

    async def imutetcmd(self, message: Message):
        """Мут <user> <time> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Мут {args[0]} {args[1]}\n", message)

    async def ibancmd(self, message: Message):
        """Бан <user> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Бан 267 дней {args[0]}\n", message)

    async def ibantcmd(self, message: Message):
        """Бан <user> <time> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Бан {args[0]} {args[1]}\n", message)

    async def ikickcmd(self, message: Message):
        """Кик <user> [reason]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Кик {args[0]}\n", message)

    async def ireasoncmd(self, message: Message):
        """Причина <user>"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Причина {args[0]}", message, use_args = False)

    async def dmcmd(self, message: Message):
        """-смс"""
        args = utils.get_args(message)
        last = await self.client.get_messages(message.peer_id, limit=2)
        await self.__iriscommand(f"-смс", message, force_reply = last[1], delete_result = False, use_args = False)

        