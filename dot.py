# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class DotMod(loader.Module):
    """Dota 2"""

    strings = {
        "name": "DotMod",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "toggle",
                True,
                lambda: "Should i dot each message?",
                validator=loader.validators.Boolean(),
            ),
        )

    async def toggledotcmd(self, message):
        """please use .config instead"""
        self.config["toggle"] = not self.config["toggle"]
        await utils.answer(message, "Done!")

    @loader.tag("only_messages", "no_commands", "out")
    async def watcher(self, message):
        if not self.config["toggle"]:
            return

        if (not message.text.strip().endswith(".")) and (not message.text.strip().endswith(",")) and (not message.text.strip().endswith("!")) and (not message.text.strip().endswith("?")):
            await message.edit(message.text + ".")
