# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: notes
# Description: Advanced notes module with folders and other features
# Author: hikariatama
# Commands:
# .hsave | .hget | .hdel | .hlist
# ---------------------------------------------------------------------------------


#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# Modified by Penggrin
# All credits goes to the original author

# meta pic: https://static.hikari.gay/notes_icon.png
# meta banner: https://mods.hikariatama.ru/badges/notes.jpg
# meta developer: @penggrinmods
# scope: hikka_only
# scope: hikka_min 1.2.10

from io import StringIO
from meval import meval
from types import ModuleType

import logging
import telethon
import sys
import itertools
import traceback

from telethon.tl.types import Message

from .. import loader, utils, main

logger = logging.getLogger(__name__)


class HegaCode():
    """
    Runs Python code
    (Modified HegaCode)
    """

    def __init__(self, mod):
        self.mod = mod

    def get_sub(self, obj, _depth = 1):
        return {
            **dict(
                filter(
                    lambda x: x[0][0] != "_"
                    and x[0][0].upper() == x[0][0]
                    and callable(x[1]),
                    obj.__dict__.items(),
                )
            ),
            **dict(
                itertools.chain.from_iterable(
                    [
                        self.get_sub(y[1], _depth + 1).items()
                        for y in filter(
                            lambda x: x[0][0] != "_"
                            and isinstance(x[1], ModuleType)
                            and x[1] != obj
                            and x[1].__package__.rsplit(".", _depth)[0]
                            == "telethon.tl",
                            obj.__dict__.items(),
                        )
                    ]
                )
            ),
        }

    async def getattrs(self, message):
        reply = await message.get_reply_message()
        return {
            **{
                "message": message,
                "client": self.mod._client,
                "_client": self.mod._client,
                "reply": reply,
                "r": reply,
                **self.get_sub(telethon.tl.types),
                **self.get_sub(telethon.tl.functions),
                "event": message,
                "chat": message.to_id,
                "telethon": telethon,
                "utils": utils,
                "main": main,
                "loader": loader,
                "f": telethon.tl.functions,
                "c": self.mod._client,
                "m": message,
                "lookup": self.mod.lookup,
                "self": self.mod,
                "db": self.mod.db,
            },
        }

    async def run(self, message, code):
        logs = ''
        old_stdout = sys.stdout
        result = sys.stdout = StringIO()

        try:
            await meval(
                code,
                globals(),
                **await self.getattrs(message),
            )
        except Exception:
            logs = traceback.format_exc(0)

        sys.stdout = old_stdout

        if logs:
            return logs

        try:
            return result.getvalue()
        except Exception as e:
            return str(e)


@loader.tds
class CodeNotesMod(loader.Module):
    """Advanced notes module that can run python code"""

    strings = {
        "name": "CodeNotes",
        "saved": (
            "💾 <b>Saved code note with name </b><code>{}</code>.\nFolder:"
            " </b><code>{}</code>.</b>"
        ),
        "no_reply": "🚫 <b>Reply and code note name are required.</b>",
        "no_name": "🚫 <b>Specify code note name.</b>",
        "no_note": "🚫 <b>Code note not found.</b>",
        "available_notes": "💾 <b>Current code notes:</b>\n",
        "no_notes": "😔 <b>You have no code notes yet</b>",
        "deleted": "🙂 <b>Deleted code note </b><code>{}</code>",
    }

    strings_ru = {
        "saved": (
            "💾 <b>Заметка кода с именем </b><code>{}</code><b> сохранена</b>.\nПапка:"
            " </b><code>{}</code>.</b>"
        ),
        "no_reply": "🚫 <b>Требуется реплай на контент заметки.</b>",
        "no_name": "🚫 <b>Укажи имя заметки кода.</b>",
        "no_note": "🚫 <b>Заметка кода не найдена.</b>",
        "available_notes": "💾 <b>Текущие заметки кода:</b>\n",
        "no_notes": "😔 <b>У тебя пока что нет заметок кода</b>",
        "deleted": "🙂 <b>Заметка кода с именем </b><code>{}</code> <b>удалена</b>",
    }

    async def client_ready(self):
        self._notes = self.get("notes", {})
        self.code = HegaCode(self)

    @loader.command(ru_doc="[папка] <имя> - Сохранить заметку")
    async def cnsavecmd(self, message: Message):
        """[folder] <name> - Save new note"""
        args = utils.get_args_raw(message)

        if len(args.split()) >= 2:
            folder = args.split()[0]
            args = args.split(maxsplit=1)[1]
        else:
            folder = "global"

        reply = await message.get_reply_message()

        if not (reply and args):
            await utils.answer(message, self.strings("no_reply"))
            return

        if folder not in self._notes:
            self._notes[folder] = {}
            logger.warning(f"Created new folder {folder}")

        asset = await self._db.store_asset(reply)

        self._notes[folder][args] = {"id": asset}

        self.set("notes", self._notes)

        await utils.answer(message, self.strings("saved").format(args, folder))

    def _get_note(self, name):
        for category, notes in self._notes.items():
            for note, asset in notes.items():
                if note == name:
                    return asset

    def _del_note(self, name):
        for category, notes in self._notes.copy().items():
            for note, asset in notes.copy().items():
                if note == name:
                    del self._notes[category][note]

                    if not self._notes[category]:
                        del self._notes[category]

                    self.set("notes", self._notes)
                    return True

        return False

    @loader.command(ru_doc="<имя> - Показать заметку")
    async def cngetcmd(self, message: Message):
        """<name> - Show specified note"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_name"))
            return

        asset = self._get_note(args)
        if not asset:
            await utils.answer(message, self.strings("no_note"))
            return

        code = (await self._db.fetch_asset(asset["id"])).message
        result = (await self.code.run(message, code))

        if message.out:
            await message.delete()

        if not result:
            return

        await self._client.send_message(
            message.peer_id,
            result,
            reply_to=getattr(message, "reply_to_msg_id", False),
        )

    @loader.command(ru_doc="<имя> - Удалить заметку")
    async def cndelcmd(self, message: Message):
        """<name> - Delete specified note"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_name"))
            return

        asset = self._get_note(args)
        if not asset:
            await utils.answer(message, self.strings("no_note"))
            return

        try:
            await (await self._db.fetch_asset(asset["id"])).delete()
        except Exception:
            pass

        self._del_note(args)

        await utils.answer(message, self.strings("deleted").format(args))

    @loader.command(ru_doc="[папка] - Показать все заметки")
    async def cnlistcmd(self, message: Message):
        """[folder] - List all notes"""
        args = utils.get_args_raw(message)

        if not self._notes:
            await utils.answer(message, self.strings("no_notes"))
            return

        result = self.strings("available_notes")

        if not args or args not in self._notes:
            for category, notes in self._notes.items():
                result += f"\n🔸 <b>{category}</b>\n"
                for note, asset in notes.items():
                    result += f"    🔹 <code>{note}</code>\n"

            await utils.answer(message, result)
            return

        for note, asset in self._notes[args].items():
            result += f"🔹 <code>{note}</code>\n"

        await utils.answer(message, result)