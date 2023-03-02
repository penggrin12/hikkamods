# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only
# requires: emoji

from .. import loader, utils
import logging
import emoji
import random

logger = logging.getLogger(__name__)


@loader.tds
class EmojiPonMod(loader.Module):
    """Luti emoji"""

    strings = {
        "name": "EmojiPonMod",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "toggle",
                True,
                lambda: "Should i emoji each message?",
                validator=loader.validators.Boolean(),
            ),
        )

    async def toggleemojicmd(self, message):
        """please use .config instead"""
        self.config["toggle"] = not self.config["toggle"]
        await utils.answer(message, "Done!")

    @loader.tag("only_messages", "no_commands", "out")
    async def watcher(self, message):
        if not self.config["toggle"]:
            return

        if (not message.text.strip().endswith(".")) and (not message.text.strip().endswith(",")) and (not message.text.strip().endswith("!")) and (not message.text.strip().endswith("?")):
            await message.edit(message.text + random.choice(list(emoji.EMOJI_DATA.keys())))
