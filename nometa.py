# The MIT License (MIT)
#
# Copyright (c) 2022 penggrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# meta developer: @penggrin
# scope: hikka_only
# scope: hikka_min 1.3.0

from .. import loader, utils
from telethon.tl.types import Message


@loader.tds
class NoMetaMod(loader.Module):
    """Warns people about Meta messages"""

    strings = {
        "name": "NoMeta",
        "no_meta": (
            "<b>👾 <u>Please!</u></b>\n<b>NoMeta</b> aka <i>'Hello', 'Hi' etc.</i>\nAsk"
            " <b>directly</b>, what do you want."
        ),
    }

    strings_ru = {
        "name": "NoMeta",
        "no_meta": (
            "<b>👾 <u>Пожалуйста!</u></b>\n<b>Не нужно лишних сообщений</b> по типу"
            " <i>'Привет', 'Хай' и др.</i>\nСпрашивай(-те) <b>конкретно</b>, что вам нужно."
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "watch_pms",
                True,
                lambda: "Watch private messages for Meta",
                validator=loader.validators.Boolean(),
            ),
        )

    @loader.command(ru_doc="Показать сообщение с предупреждением о мете")
    @loader.unrestricted
    async def nometacmd(self, message: Message):
        """Show message about Meta"""
        await self._client.send_message(message.peer_id, self.strings("no_meta"), reply_to=getattr(message, "reply_to_msg_id", None))
        if message.out:
            await message.delete()

    @loader.tag("only_messages", "only_pm", "in")
    async def watcher(self, message: Message):
        if not self.config["watch_pms"]:
            return

        meta = ["hi", "hello", "hey there", "konichiwa", "hey", "sup", "whats up", "wassup"]
        meta_ru = [ "привет", "хай", "хелло", "хеллоу", "хэллоу", "коничива", "алоха", "хей", "хэй", "йо", "йоу", "прив", "yo", "ку"]

        if (message.raw_text.lower() in meta) or (message.raw_text.lower() in meta_ru):
            await utils.answer(message, self.strings("no_meta"))
            await self._client.send_read_acknowledge(message.chat_id, clear_mentions=True,)