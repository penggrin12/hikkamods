# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_we
# scope: hikka_min 1.2.10

import asyncio
import logging

from telethon.tl.types import Message
from .. import loader, main, translations, utils

logger = logging.getLogger(__name__)


@loader.tds
class CHMSMod(loader.Module):
    """Load Hikka modules with "Install Via CHMS"."""

    strings = {
        "name": "CHMS",
        "warning": (
            "⚠️ Looks like you added un-offical sources to your trusted sources. Note that this <b>can be dangerous!</b>"
            " (You can disable this warning in <code>.config</code>)"
        ),
        "cfg_trusted": "Trusted sources to load modules from (ID or @USERNAME without the @)",
        "cfg_no_warnings": "Do not show warnings at startup"
    }

    strings_ru = {
        "warning": (
            "⚠️ Вы добавили не-официального бота в свой список доверенных ботов. Знайте что это действие <b>может быть опасным!</b>"
            " (Вы можете выключить это предупреждение в <code>.config</code>)"
        ),
        "cfg_trusted": "Доверенные боты из которых можно загружать модули (АЙДИ или @ЮЗЕРНЕЙМ без @)",
        "cfg_no_warnings": "Не показывать предупреждения при запуске"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "trusted",
                [5829488433], # official sources
                lambda: self.strings("cfg_trusted"),
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "no_warnings",
                False,
                lambda: self.strings("cfg_no_warnings"),
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, *_):
        for source in self.config["trusted"]:
            await utils.dnd(self._client, source, archive=False)

        self.loader_m = self.lookup("loader")
        self.version = "1.1"

        if (self.config["trusted"] != [5829488433]) and (not self.config["no_warnings"]):
            await self.client.send_message("me", self.strings("warning"))

    async def _load_module(self, message):
        doc = (await message.download_media(bytes)).decode("utf-8")
        await self.loader_m.load_module(doc, None, save_fs=True)

        if getattr(self.loader_m, "_fully_loaded", getattr(self.loader_m, "fully_loaded", False)):
            self.loader_m._update_modules_in_db()

        logger.debug("Done loading new custom module!")
        await message.reply(f"#done")

    @loader.command(ru_doc="Показать версию Клиента CHMS")
    async def chmsversion(self, message):
        """Show CHMS Client version"""
        await utils.answer(message, self.version)

    @loader.watcher(only_docs=True)
    async def watcher(self, message):
        if not isinstance(message, Message):
            return
        if not (message.sender_id in self.config["trusted"]):
            return

        await message.delete()

        if message.raw_text == "#version":
            await message.reply(self.version)
        elif message.raw_text == "#cinstall":
            logger.debug("Installing a module from a trusted source")
            await self._load_module(message)
