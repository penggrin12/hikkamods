# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @PenggrinModules
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
        "searching": "❤️ Please wait!\n⚙️ Searching...",
        "uploading": "❤️ Please wait!\n⚙️ Uploading...",
    }
    strings_ru = {
        "gathered": "❤️ Вот что я собрал за время работы",
        "already_started": "❌ Логгинг уже включен!",
        "already_stopped": "❌ Логгинг уже выключен!",
        "started": "❤️ Логгинг успешно включен!",
        "stopped": "❤️ Логгинг успешно выключен!",
        "searching": "❤️ Пожалуйста подождите!\n⚙️ Ищем...",
        "uploading": "❤️ Пожалуйста подождите!\n⚙️ Загружаем...",
    }

    def log_write(self, mode, text):
        with open("logger_.txt", mode) as file:
            file.write(text)

    async def client_ready(self, client, db):
        # Should this be removed?
        if not self.get("logging_active"):
            self.set("logging_active", False)

    @loader.command(ru_doc="Включить логгинг")
    async def logstartcmd(self, message):
        """- Start the logging"""
        if self.get("logging_active"):
            await utils.answer(message, self.strings("already_started"))
            return

        self.set("logging_active", True)
        self.log_write("w", "--------- Started ---------\n")
        await utils.answer(message, self.strings("started"))

    @loader.command(ru_doc="- Выключить логгинг")
    async def logstopcmd(self, message):
        """- Stop the logging"""
        if not self.get("logging_active"):
            await utils.answer(message, self.strings("already_stopped"))
            return

        self.set("logging_active", False)
        self.log_write("a", "---------- Ended ----------\n")
        await utils.answer(message, self.strings("stopped"))

    @loader.command(ru_doc="<запрос> - Найти что-то в файле логов")
    async def logfindcmd(self, message):
        """<query> - Find something in the logs file"""
        await utils.answer(message, self.strings("searching"))
        with open("loggerfind_.txt", "w") as out:
            with open("logger_.txt", "r") as inp:
                for line in inp:
                    if utils.get_args_raw(message).lower() in line.lower():
                        out.write(line)
        await utils.answer(message, self.strings("uploading"))
        self.log_write("a", "-------- Collected --------\n")

        await self.client.send_file(
            message.peer_id,
            "loggerfind_.txt",
            caption=self.strings("gathered")
        )

        if message.out:
            await message.delete()

    @loader.command(ru_doc="- Скачать весь файл логов")
    async def logcollectcmd(self, message):
        """- Download the whole logs file"""
        await utils.answer(message, self.strings("uploading"))
        self.log_write("a", "-------- Collected --------\n")

        await self.client.send_file(
            message.peer_id,
            "logger_.txt",
            caption=self.strings("gathered")
        )

        if message.out:
            await message.delete()

    @loader.watcher("only_messages")
    async def watcher(self, message):
        if not self.get("logging_active"):
            return
        if len(message.message) <= 0:
            return

        try:
            user = await self.client.get_entity(message.from_id)
            self.log_write("a", f'{message.id} - {message.peer_id} [{user.id}] [{user.username or user.first_name}]: "{message.message}"\n')
        except Exception:
            pass
