# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

import re
import random

logger = logging.getLogger(__name__)


@loader.tds
class AutoOwoifyMod(loader.Module):
    """Makes your messages look more awesome!"""

    strings = {
        "name": "AutoOwOify",
        "config_enable": "Status of this module",
    }

    strings_ru = {
        "config_enable": "Статус этого модуля",
    }

    def __init__(self):
        self._kaomoji = [
            "(*^ω^)",
            "(◕‿◕✿)",
            "(◕ᴥ◕)",
            "ʕ•ᴥ•ʔ",
            "ʕ￫ᴥ￩ʔ",
            "(*^.^*)",
            "owo",
            "OwO",
            "(｡♥‿♥｡)",
            "uwu",
            "UwU",
            "(*￣з￣)",
            ">w<",
            "^w^",
            "(つ✧ω✧)つ",
            "(/ =ω=)/",
        ]


        self._patterns = {
            r"[lr]": "w",
            r"[LR]": "W",
            r"[лр]": "в",
            r"[ЛР]": "В",
            r"n([aeiou])": "ny\\1",
            r"N([aeiou])": "Ny\\1",
            r"N([AEIOU])": "NY\\1",
            "th": "d",
            "ove": "uv",
            "no": "nu",
            r"!+": lambda _: " " + random.choice(self._kaomoji),
        }

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enable",
                True,
                lambda: self.strings("config_enable"),
                validator=loader.validators.Boolean(),
            ),
        )

    def owoify(self, text):
        for pattern, repl in self._patterns.items():
            text = re.sub(pattern, repl, text)

        return text

    @loader.command(ru_doc="<text:str> - OwO-фицировать (лучше писать на английском)")
    async def owoifycmd(self, message):
        """<text:str> - OwO-ify"""
        await utils.answer(message, self.owoify(utils.get_args_raw(message)))

    @loader.watcher(out=True, only_messages=True, no_commands=True)
    async def new_message(self, message):
        if not self.config["enable"]:
            return

        await utils.answer(message, self.owoify(message.raw_text))

