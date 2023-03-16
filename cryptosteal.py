# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

__version__ = (1, 2, 0)
logger = logging.getLogger(__name__)


@loader.tds
class CryptoStealMod(loader.Module):
    """Automatically claims cryptobot (and some other bots) checks, special thanks to @toxicuse"""

    strings = {
        "name": "CryptoSteal",
        "disabled": "<emoji document_id=5260342697075416641>❌</emoji> Disabled",
        "enabled": "<emoji document_id=5206607081334906820>✅</emoji> Enabled",
        "status_now": "<emoji document_id=5449687343931859785>🤑</emoji> Crypto-Steal was <b>{}</b>!",
        "config_status": "Are we ready to steal?",
        "config_allow_other_bots": "If disabled i will only steal checks by Trusted Bots",
        "config_use_asset_chat": "If disabled the 'crypto-steal' will not be used",
        "config_trusted_bots": "Trusted Bots to steal from even if allow_other_bots is False (lowercase username)",
        "cant_create_asset_chat": "The asset chat is not created, for some reason.",
        "asset_chat_got_check": "☘️ Hopefully got a new check, here is the link to it: {u1}?start={u2}\nor:\n<code>/start {u2}</code> in {u1}",
    }

    strings_ru = {
        "disabled": "<emoji document_id=5260342697075416641>❌</emoji> Выключен",
        "enabled": "<emoji document_id=5206607081334906820>✅</emoji> Включён",
        "status_now": "<emoji document_id=5449687343931859785>🤑</emoji> Crypto-Steal теперь <b>{}</b>!",
        "config_status": "Готовы ли мы тырить?",
        "config_allow_other_bots": "Если выключено то я буду тырить только чеки Доверенных Ботов",
        "config_use_asset_chat": "Если выключено то чат 'crypto-steal' не будет использован",
        "config_trusted_bots": "Доверенные Боты из которых я буду тырить даже если allow_other_bots на False (ник маленькими буквами)",
        "cant_create_asset_chat": "Не удалось создать чат Crypto-Steal, почему-то.",
        "asset_chat_got_check": "☘️ Надеюсь получил новый чек, вот ссылка на него: {u1}?start={u2}\nили:\n<code>/start {u2}</code> в {u1}",
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
                "use_asset_chat",
                True,
                lambda: self.strings("config_use_asset_chat"),
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

    async def client_ready(self):
        self.asset_chat = await utils.asset_channel(
            self.client,
            "crypto-steal",
            "",
            avatar=r"https://img2.joyreactor.cc/pics/post/full/Zettai-Ryouiki-%D1%80%D0%B0%D0%B7%D0%BD%D0%BE%D0%B5-3527844.jpeg",
            silent=True,
            invite_bot=True
        )

        if not self.asset_chat:
            await self.inline.bot.send_message(self._client.tg_id, self.strings("cant_create_asset_chat"))
            logger.error("cant create asset chat")

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
            logging.debug('This check is already activated')
            return

        user = await self.client.get_entity(url[0])

        if (user.username.lower() not in self.config["trusted_bots"]) and (not self.config["allow_other_bots"]):
            logger.debug(f"Ignoring not trusted bot (@{user.username})")
            return

        await self.client.send_message(user.id, f"/start {url[1]}")
        already_claimed.append(url[1])
        logger.debug("Sent check get request, hopefully we got it")
        self.db.set(__name__, 'already_claimed', already_claimed)

        if self.asset_chat and self.config["use_asset_chat"]:
            await self.inline.bot.send_message(
                f"-100{self.asset_chat[0].id}",
                self.strings("asset_chat_got_check").format(u1=url[0], u2=url[1]),
                disable_web_page_preview=True
            )

    async def cryptostealcmd(self, message):
        """Toggle Crypto-Steal"""

        self.config["status"] = not self.config["status"]
        status = self.strings("enabled") if self.config["status"] else self.strings("disabled")

        await utils.answer(message, self.strings("status_now").format(status))
