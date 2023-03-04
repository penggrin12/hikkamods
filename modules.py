# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging


logger = logging.getLogger(__name__)


@loader.tds
class MyModulesMod(loader.Module):
    """Lists all the currently installed modules"""

    strings = {
        "name": "MyModules",
        "amount": "<emoji document_id=5316573023094971227>📦</emoji> Right now there is <b>{}</b> modules loaded:\n",
        "partial_load": (
            "\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>it's not yet all modules,"
            " Userbot is still loading</b>"
        ),
        "module": "<emoji document_id=5402093879316982515>✨</emoji>",
        "core_module": "<emoji document_id=5400245067694747959>💫</emoji>"
    }

    strings_ru = {
        "amount": "<emoji document_id=5316573023094971227>📦</emoji> Сейчас загружено <b>{}</b> модулей:",
        "partial_load": (
            "\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>Это не все модули,"
            " Юзербот ещё загружается</b>"
        ),
    }

    @loader.command(ru_doc="Показать все установленные модули")
    async def modscmd(self, message):
        """List of all of the modules currently installed"""

        result = f"{self.strings('amount').format(str(len(self.allmodules.modules)))}\n"

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__

            emoji = self.strings("core_module") if mod.__origin__.startswith("<core") else self.strings("module")
            result += f"\n {emoji} <code>{name}</code>"

        result += "" if self.lookup("Loader").fully_loaded else f"\n{self.strings('partial_load')}"

        await utils.answer(message, result)
