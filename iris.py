# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
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
        "config_delete_cmds": "Delete the messages IrisManager sends?",
        "bot": "🤖 Bot",
        "user": "👨‍🦰 User",
        "cant_get_user_info": "🚫 Cant get information about that user!"
    }
    strings_ru = {
        "config_delete_cmds": "Удалять сообщения которые отправляет IrisManager?",
        "bot": "🤖 Бот",
        "user": "👨‍🦰 Юзер",
        "cant_get_user_info": "🚫 Не могу получить информацию об этом пользователе!"
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
                lambda: self.strings("config_delete_cmds"),
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

    @loader.command(ru_doc="[id:str OR int] - Возвращает данные о пользователе с помощью его айди / юзернейма, либо с помощью ответа")
    async def idcmd(self, message: Message):
        """[id:str OR int] - Returns information about the user from their id / username, or with an reply"""
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

            await utils.answer(message, f"{self.strings('bot') if target.bot else self.strings('user')}:\n`{target.first_name}` {f'`{target.last_name}`' if target.last_name else ''}\n`{target.id}` {f'(`{target.username}`)' if target.username else ''}", parse_mode = "Markdown")
        except Exception as e:
            logger.warning(f"Cant get information about the user (called by 'id' command)\n{e}")
            await utils.answer(message, f"{self.strings('cant_get_user_info')}\n\n❓ {e}")

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
        """.топ <count:int> вся"""
        args = utils.get_args(message)
        amount = 10
        if len(args) > 0:
            amount = args[0]
        await self.__iriscommand(f".топ {amount} вся", message, use_args = False)

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
        """Варн <user> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Варн {args[0]}\n", message)

    async def iwarntcmd(self, message: Message):
        """Варн <user> <time:int> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Варн {args[0]} {args[1]}\n", message)

    async def imutecmd(self, message: Message):
        """Мут <user> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Мут {args[0]}\n", message)

    async def imutetcmd(self, message: Message):
        """Мут <user> <time:int> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Мут {args[0]} {args[1]}\n", message)

    async def ibancmd(self, message: Message):
        """Бан <user> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Бан 267 дней {args[0]}\n", message)

    async def ibantcmd(self, message: Message):
        """Бан <user> <time:int> [reason:str]"""
        args = utils.get_args(message)
        await self.__iriscommand(f"Бан {args[0]} {args[1]}\n", message)

    async def ikickcmd(self, message: Message):
        """Кик <user> [reason:str]"""
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

        