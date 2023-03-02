# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import logging

import datetime

logger = logging.getLogger(__name__)


@loader.tds
class ActiveTimerMod(loader.Module):
    """Shows a (since my last message) timer in your lastname"""

    strings = {
        "name": "ActiveTimerMod",
        "timer_set": "✅ Cool. The timer is set to: {}",
        "not_enough_arguments": "❌ Not enough arguments!",
        "config_custom_divider": "Custom divider, Defaults to »|« (Bob »|« 💚 0:05:00 ago)",
        "config_custom_prefix": "Custom prefix, Defaults to a colored heart (Bob | »💚« 0:05:00 ago)",
        "config_custom_suffix": "Custom suffix, Defaults to »ago« (Bob | 💚 0:05:00 »ago«)",
        "ago": "ago",
    }
    strings_ru = {
        "timer_set": "✅ Люти пон. Таймер установлен на: {}",
        "not_enough_arguments": "❌ Не достаточно параметров!",
        "config_custom_divider": "Кастомный разделитель, по стандарту: »|« (Bob »|« 💚 0:05:00 назад)",
        "config_custom_prefix": "Кастомный префикс, по стандарту: сердечко (Bob | »💚« 0:05:00 назад)",
        "config_custom_suffix": "Кастомный суфикс, по стандарту: »назад« (Bob | 💚 0:05:00 »назад«)",
        "ago": "назад",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_divider",
                None,
                lambda: self.strings("config_custom_divider")
            ),
            loader.ConfigValue(
                "custom_prefix",
                None,
                lambda: self.strings("config_custom_prefix")
            ),
            loader.ConfigValue(
                "custom_suffix",
                None,
                lambda: self.strings("config_custom_suffix")
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
        return f'{self.config["custom_divider"] or "|"} {self.config["custom_prefix"] or self.get_timer_emoji(self.get("timer"))} {str(datetime.timedelta(seconds=self.get("timer")))} {self.config["custom_suffix"] or self.strings("ago")}'

    async def setname(self):
        new_name = await self.get_new_name()
        await self.client(UpdateProfileRequest(first_name=None, last_name=new_name, about=None))

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
    async def new_message(self, message):
        self.set("timer", 0)

    @loader.loop(interval=30, autostart=True)
    async def loop(self):
        self.set("timer", self.get("timer") + 30)
        await self.setname()
