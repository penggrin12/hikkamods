# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class LoggerMod(loader.Module):
    """Logs every message, from every chat"""

    strings = {
        "name": "LoggerMod",
        "gathered": "❤️ Here is what i have gathered so far",
        "already_started": "❌ Logging is already started!",
        "already_stopped": "❌ Logging is already stopped!",
        "started": "❤️ Started logging!",
        "stopped": "❤️ Stopped logging!",
        "please_wait": "❤️ Please wait...",
    }
    strings_ru = {
        "gathered": "❤️ Вот что я собрал за всё время",
        "already_started": "❌ Логгинг уже включен!",
        "already_stopped": "❌ Логгинг уже выключен!",
        "started": "❤️ Логгинг успешно включен!",
        "stopped": "❤️ Логгинг успешно выключен!",
        "please_wait": "❤️ Пожалуйста подождите...",
    }

    def log_write(self, mode, text):
        with open("logger_.txt", mode) as file:
            file.write(text)

    async def client_ready(self, client, db):
        self.client = client

        if not self.get("logging_active"):
            self.set("logging_active", False)

    @loader.command(ru_doc="Включить логгинг")
    async def lstartcmd(self, message):
        """- Start the logging"""
        if self.get("logging_active"):
            await utils.answer(message, self.strings("already_started"))
            return

        self.set("logging_active", True)
        self.log_write("w", "--------- Started ---------\n")
        await utils.answer(message, self.strings("started"))

    @loader.command(ru_doc="Выключить логгинг")
    async def lstopcmd(self, message):
        """- Stop the logging"""
        if not self.get("logging_active"):
            await utils.answer(message, self.strings("already_stopped"))
            return

        self.set("logging_active", False)
        self.log_write("a", "---------- Ended ----------\n")
        await utils.answer(message, self.strings("stopped"))

    @loader.command(ru_doc="Скачать файл логов")
    async def lcollectcmd(self, message):
        """- Download a logs file"""
        await utils.answer(message, self.strings("please_wait"))
        self.log_write("a", "-------- Collected --------\n")

        await self.client.send_file(message.peer_id, "logger_.txt", caption=self.strings("gathered"))

        if message.out:
            await message.delete()

    @loader.watcher("only_messages")
    async def watcher(self, message):
        if not self.get("logging_active"):
            return
        if len(message.message) <= 0:
            return

        user = await self.client.get_entity(message.from_id)
        self.log_write("a", f'[{user.username or user.first_name}]: "{message.message}"\n')

