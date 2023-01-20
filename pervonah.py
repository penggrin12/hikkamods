# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class PervoNahMod(loader.Module):
    """Automatically comments under any channels you want"""

    strings = {
        "name": "PervoNah",
        "disabled": "❌ Disabled",
        "enabled": "✅ Enabled",
        "status_now": "👌 Pervo-Nah was <b>{}</b>!",
        "config_status": "Are we ready to comment?",
        "config_channels": "Under which channels i should comment? (ids)",
        "config_message": "What i will comment?",
    }

    strings_ru = {
        "disabled": "❌ Выключен",
        "enabled": "✅ Включён",
        "status_now": "👌 Перво-Нах теперь <b>{}</b>!",
        "config_status": "Комментим ли мы?",
        "config_channels": "Под каким каналами я должен комментировать (айди)",
        "config_message": "Как я прокомментирую?",
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
                "message",
                "I'm the first! 😎",
                lambda: self.strings("config_message"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "channels",
                [],
                lambda: self.strings("config_channels"),
                validator=loader.validators.Series(
                    loader.validators.Union(
                        loader.validators.Integer(),
                    )
                )
            ),
        )

    @loader.watcher(only_messages=True, only_channels=True)
    async def watcher(self, message):
        if not self.config["status"]:
            return

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
