# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only
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

    strings = {"name": "CHMS"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "trusted",
                [5829488433],
                "Trusted sources to load modules from",
                validator=loader.validators.Series(loader.validators.Integer()),
            )
        )

    async def client_ready(self, *_):
        for source in self.config["trusted"]:
            await utils.dnd(self._client, source, archive=False)
        self.loader_m = self.lookup("loader")

    async def _load_module(self, message):
        doc = (await message.download_media(bytes)).decode("utf-8")
        await self.loader_m.load_module(doc, None, save_fs=True)

        if getattr(self.loader_m, "_fully_loaded", getattr(self.loader_m, "fully_loaded", False)):
            self.loader_m._update_modules_in_db()

        logger.debug("Done loading new custom module!")
        await message.reply(f"#done")

    @loader.watcher(only_docs=True)
    async def watcher(self, message: Message):
        if not isinstance(message, Message):
            return

        if (message.sender_id in self.config["trusted"]) and (message.raw_text.startswith("#cinstall")):
            await message.delete()
            logger.debug("Installing a module from a trusted source")

            await self._load_module(message)
