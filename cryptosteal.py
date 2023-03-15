# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

__version__ = (1, 1, 0)
logger = logging.getLogger(__name__)


@loader.tds
class CryptoStealMod(loader.Module):
    """Automatically claims cryptobot (and some other bots) checks, special thanks to @toxicuse"""

    strings = {
        "name": "CryptoSteal",
        "disabled": "❌ Disabled",
        "enabled": "✅ Enabled",
        "status_now": "👌 Crypto-Steal was <b>{}</b>!",
        "config_status": "Are we ready to steal?",
        "config_allow_other_bots": "If disabled i will only steal checks by Trusted Bots",
        "config_trusted_bots": "Trusted Bots to steal from even if allow_other_bots is False (lowercase username)",
    }

    strings_ru = {
        "disabled": "❌ Выключен",
        "enabled": "✅ Включён",
        "status_now": "👌 Crypto-Steal теперь <b>{}</b>!",
        "config_status": "Готовы ли мы тырить?",
        "config_allow_other_bots": "Если выключено то я буду тырить только чеки Доверенных Ботов",
        "config_trusted_bots": "Доверенные Боты из которых я буду тырить даже если allow_other_bots на False (ник маленькими буквами)",
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
                "allow_other_bots",
                False,
                lambda: self.strings("config_allow_other_bots"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "trusted_bots",
                ["cryptobot", "tonrocketbot", "xjetswapbot"],
                lambda: self.strings("trusted_bots"),
                validator=loader.validators.Series(
                    loader.validators.Union(
                        loader.validators.String(),
                        loader.validators.Integer()
                    )
                )
            ),
        )

    @loader.watcher(only_messages=True, only_inline=True)
    async def watcher(self, message):
        text = message.raw_text.lower()
        already_claimed: list = self.db.get(__name__, 'already_claimed', [])

        if not self.config["status"]:
            return
        if not (("check for " in text) or ("чек на " in text)):
            return

        url = message.buttons[0][0].url.split("?start=")
        if url[1] in already_claimed:
            logging.debug('The check is already activated')
            return
        user = await self.client.get_entity(url[0])

        if (user.username.lower() not in self.config["trusted_bots"]) and (not self.config["allow_other_bots"]):
            logger.debug(f"Ignoring not trusted bot (@{user.username})")
            return

        await self.client.send_message(user.id, f"/start {url[1]}")
        already_claimed.append(url[1])
        logger.debug("Sent check get request, hopefully we got it")
        self.db.set(__name__, 'already_claimed', already_claimed)

    async def cryptostealcmd(self, message):
        """Toggle Crypto-Steal"""

        self.config["status"] = not self.config["status"]
        status = self.strings("enabled") if self.config["status"] else self.strings("disabled")

        await utils.answer(message, self.strings("status_now").format(status))
