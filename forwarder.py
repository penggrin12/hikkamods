# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class ForwarderMod(loader.Module):
    """Automatically forwards any messages you get from the given chat"""

    strings = {
        "name": "Forwarder",
        "disabled": "❌ Disabled",
        "enabled": "✅ Enabled",
        "status_now": "👌 Forwarder was <b>{}</b>!",
        "status_now": "👌 Forwarder was <b>{}</b>!",
        "config_status": "Forwarding messages?",
        "config_origin": "The chat that i will pull messages from",
        "config_destination": "The chat that will put these messages in",
    }

    strings_ru = {
        "disabled": "❌ Выключен",
        "enabled": "✅ Включён",
        "status_now": "👌 Forwarder теперь <b>{}</b>!",
        "config_status": "Пересылаем сообщения?",
        "config_origin": "Чат из которого я буду брать сообщения",
        "config_destination": "Чат в который я отправлю эти сообщения",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                lambda: self.strings("config_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "origin",
                None,
                lambda: self.strings("config_origin"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "destination",
                None,
                lambda: self.strings("config_destination"),
                validator=loader.validators.Integer()
            ),
        )

    @loader.watcher(only_messages=True, only_channels=True)
    async def watcher(self, message):
        if not self.config["status"]:
            return
        if not (self.config["origin"] or self.config["destination"]):
            

        chat = utils.get_chat_id(message)

        if chat not in self.config["channels"]:
            return
        await self.client.send_message(entity=chat, message=self.config["message"], comment_to=message)
        logger.debug(f"commented on {message.id} in {chat}")

    async def pervonahcmd(self, message):
        """Toggle Pervo-Nah"""

        self.config["status"] = not self.config["status"]
        status = self.strings("enabled") if self.config["status"] else self.strings("disabled")

        await utils.answer(message, self.strings("status_now").format(status))
