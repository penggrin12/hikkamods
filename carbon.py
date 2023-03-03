#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# edited by @Penggrin

# meta pic: https://img.icons8.com/stickers/500/000000/code.png
# meta banner: https://mods.hikariatama.ru/badges/carbon.jpg
# meta developer: @hikarimods
# scope: hikka_only
# scope: hikka_min 1.2.10
# requires: urllib requests

import io

import requests
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class CarbonMod(loader.Module):
    """Create beautiful code images. Edited by @Penggrin"""

    strings = {
        "name": "Carbon",
        "args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>No code specified</b>"
        ),
        "loading": "<emoji document_id=5213452215527677338>⏳</emoji> <b>Loading...</b>"
    }

    strings_ru = {
        "args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Не указаны"
            " код</b>"
        ),
        "loading": (
            "<emoji document_id=5213452215527677338>⏳</emoji> <b>Обработка...</b>"
        ),
        "_cls_doc": "Создает симпатичные фотки кода. Отредактировано @Penggrin"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "theme",
                "vsc-dark-plus",
                "Theme from clck.ru/33HUNM",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "color",
                "gray",
                "Background color",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "language",
                "python",
                "Programming language",
                validator=loader.validators.String()
            ),
        )

    @loader.command(ru_doc="<код> - Сделать красивую фотку кода")
    async def carboncmd(self, message: Message):
        """<code> - Create beautiful code image"""
        args = utils.get_args_raw(message)

        try:
            code_from_message = (
                await self._client.download_file(message.media, bytes)
            ).decode("utf-8")
        except Exception:
            code_from_message = ""

        try:
            reply = await message.get_reply_message()
            code_from_reply = (
                await self._client.download_file(reply.media, bytes)
            ).decode("utf-8")
        except Exception:
            code_from_reply = ""

        args = args or code_from_message or code_from_reply

        if not args:
            await utils.answer(message, self.strings("args"))
            return

        message = await utils.answer(message, self.strings("loading"))

        doc = io.BytesIO(
            (
                await utils.run_sync(
                    requests.post,
                    f'https://code2img.vercel.app/api/to-image?theme={self.config["theme"]}&language={self.config["language"]}&line-numbers=true&background-color={self.config["color"]}',
                    headers={"content-type": "text/plain"},
                    data=bytes(args, "utf-8"),
                )
            ).content
        )
        doc.name = "carbonized.jpg"

        await self._client.send_message(
            utils.get_chat_id(message),
            file=doc,
            force_document=(len(args.splitlines()) > 35),
            reply_to=getattr(message, "reply_to_msg_id", None),
        )
        await message.delete()
