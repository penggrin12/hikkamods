# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class VahuiMod(loader.Module):
    """Auto-Respond to "вахуи" """

    strings = {
        "name": "VahuiMod",
        "config_enable": "Status of this module",
        "config_vahuis": "Vahuis that we can respond to",
        "config_response": "The reponse we will give",
        "done": "❤️ Done!",
    }

    strings_ru = {
        "config_enable": "Статус этого модуля",
        "config_vahuis": "Вахуи на которые мы можем ответить",
        "config_response": "Ответ который мы дадим",
        "done": "❤️ Готово!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enable",
                True,
                lambda: self.strings("config_enable"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "response",
                "втрихуи",
                lambda: self.strings("config_response"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "vahuis",
                ["вахуи", "вахуй"],
                lambda: self.strings("config_vahuis"),
                validator=loader.validators.Series(loader.validators.String()),
            ),
        )

    @loader.command(ru_doc="Переключить авто-ответ на 'вахуи' (используйте .config вместо этого)")
    async def togglevahuicmd(self, message):
        """Toggle the auto-answer to 'vahui' (use .config instead)"""
        self.config["enable"] = not self.config["enable"]
        await utils.answer(message, self.strings("done") + (" 🟩" if self.config["enable"] else " 🟥"))

    @loader.watcher(only_messages=True, no_commands=True)
    async def new_message(self, message):
        if not self.config["enable"]:
            return

        for vahui in self.config["vahuis"]:
            if vahui in message.raw_text.lower():
                logger.debug('Responding "%s" to a "%s"', self.config["response"], message.raw_text)
                await utils.answer(message, self.config["response"])
