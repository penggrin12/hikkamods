# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only
# scop: hikka_min 1.3.0

__version__ = (1, 0, 0)

from telethon.tl.functions.account import UpdateProfileRequest
import time, logging, datetime, asyncio
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ActiveTimerMod(loader.Module):
    """Shows a (since my last message) timer in your lastname"""

    strings = {
        "name": "ActiveTimerMod",
        "timer_set": "✅ Cool. The timer is set to: {}",
        "not_enough_arguments": "❌ Not enough arguments!",
    }
    strings_ru = {
        "timer_set": "✅ Люти пон. Таймер установлен на: {}",
        "not_enough_arguments": "❌ Не достаточно параметров!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_divider",
                None,
                lambda: "Custom divider, Defaults to | (example: <b>Bob (divider) 0:15:08</b>)",
            ),
            loader.ConfigValue(
                "custom_message",
                None,
                lambda: "Custom divider, Defaults to nothing (example: <b>Bob | (message) 0:15:08</b>)",
            ),
        )

    async def client_ready(self, client, db):
        if not self.get("timer"):
            self.set("timer", 0)

    def get_timer_emoji(self, timer):
        if timer > 10800:
            return "💤"
        elif timer > 3000:
            return "❤️"
        elif timer > 900:
            return "💛"
        else:
            return "💚"

    async def get_new_name(self):
        return f'{self.config["custom_divider"] or "|"} {self.config["custom_message"] or self.get_timer_emoji(self.get("timer"))} {str(datetime.timedelta(seconds=self.get("timer")))}'

    async def setname(self):
        newName = await self.get_new_name()
        await self.client(UpdateProfileRequest(first_name=None, last_name=newName, about=None))

    @loader.command(ru_doc="<timer:int> - Поменять время таймера вручную")
    async def settimercmd(self, message):
        """<timer:int> - Manually change the timer"""
        args = utils.get_args(message)
        if len(args) < 1:
            await utils.answer(message, self.strings("not_enough_arguments"))
            return

        self.set("timer", int(args[0]))
        await self.setname()
        await utils.answer(message, self.strings("timer_set").format(str(datetime.timedelta(seconds=int(args[0])))))

    @loader.watcher(only_messages=True, out=True, no_commands=True)
    async def newMessage(self, message):
        self.set("timer", 0)
        #await self.setname()
        
    @loader.loop(interval=30, autostart=True)
    async def loop(self):
        self.set("timer", self.get("timer") + 30)
        await self.setname()
