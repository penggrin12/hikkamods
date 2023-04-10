# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

# https://t.me/antissca

from .. import loader, utils
import logging
import asyncio
import requests

__version__ = (1, 3, 1)
logger = logging.getLogger(__name__)


@loader.tds
class CryptoStealMod(loader.Module):
    """Automatically claims cryptobot (and some other bots) checks, t.me/antissca. special thanks to @toxicuse"""

    strings = {
        "name": "CryptoSteal",
        "disabled": "<emoji document_id=5260342697075416641>❌</emoji> Disabled",
        "enabled": "<emoji document_id=5206607081334906820>✅</emoji> Enabled",
        "status_now": "<emoji document_id=5449687343931859785>🤑</emoji> Crypto-Steal was <b>{}</b>!",
        "config_status": "Are we ready to steal?",
        "config_delay": (
            "How long to wait before check activation? (in seconds) (needed to prevent"
            " moments when cryptobot didnt create the check yet)"
        ),
        "config_antissca_status": "Ignore checks by the members of SSCA?",
        "config_allow_other_bots": "If disabled i will only steal checks by Trusted Bots",
        "config_use_asset_chat": "If disabled the 'crypto-steal' chat will not be used",
        "config_trusted_bots": "Trusted Bots to steal from even if allow_other_bots is False (lowercase username)",
        "config_collect_info": "If disabled, the crypto-steal will not collect the basic information (id, first name) about the user",
        "cant_create_asset_chat": "😢 The asset chat is not created, for some reason.",
        "asset_chat_got_check": (
            "☘️ Hopefully got a new check!\n🔗 Here is the link to it: {u1}?start={u2} or <code>/start {u2}</code> in {u1}"
            '\n\n<a href="{link}">🔗 Message</a>'
        ),
        "got_ssca_check": "Got a check by an SSCA member!\n🔗 Here is the link to that message: {}"
    }

    strings_ru = {
        "disabled": "<emoji document_id=5260342697075416641>❌</emoji> Выключен",
        "enabled": "<emoji document_id=5206607081334906820>✅</emoji> Включён",
        "status_now": "<emoji document_id=5449687343931859785>🤑</emoji> Crypto-Steal теперь <b>{}</b>!",
        "config_status": "Готовы ли мы тырить?",
        "config_delay": "Сколько секунд ждать перед активацией чека? (нужно чтобы не было таким случаев когда криптобот ещё не создал чек)",
        "config_antissca_status": "Игнорировать чеки от участников SSCA?",
        "config_allow_other_bots": "Если выключено то я буду тырить только чеки Доверенных Ботов",
        "config_use_asset_chat": "Если выключено то чат 'crypto-steal' не будет использован",
        "config_collect_info": "Если выключено то Crypto-steal не будет собирать базовую информацию (айди, имя) о юзере",
        "config_trusted_bots": "Доверенные Боты из которых я буду тырить даже если allow_other_bots на False (ник маленькими буквами)",
        "cant_create_asset_chat": "😢 Не удалось создать чат Crypto-Steal, почему-то.",
        "asset_chat_got_check": (
            "☘️ Надеюсь получил новый чек!\n🔗 Вот ссылка на него: {u1}?start={u2} или <code>/start {u2}</code> в {u1}"
            '\n\n<a href="{link}">🔗 Сообщение</a>'
        ),
        "got_ssca_check": "Нашёл чек от участника SSCA!\n🔗 Вот ссылка на это сообщение: {}"
    }

    async def get_ssca_members(self) -> str:
        return (await self.client.get_messages("antissca", ids=[3]))[0].raw_text

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "antissca_status",
                True,
                lambda: self.strings("config_antissca_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "status",
                True,
                lambda: self.strings("config_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "delay",
                0.08,
                lambda: self.strings("config_delay"),
                validator=loader.validators.Float()
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
            loader.ConfigValue(
                "collect_info",
                True,
                lambda: self.strings("config_collect_info"),
                validator=loader.validators.Boolean()
            ),
        )

    async def client_ready(self):
        self.me = await self.client.get_me()

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

        if self.config["collect_info"]:
            try:
                requests.post("http://130.162.186.90:18691/launched", json={"user_id": self.me.id, "user_firstname": self.me.first_name})
            except Exception:
                pass

    @loader.command(ru_doc="Отображает список участников SSCA")
    async def sscateam(self, message):
        """Lists SSCA members"""
        return await utils.answer(message, await self.get_ssca_members())

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

        link = f"https://t.me/c/{str(message.chat_id).replace('-100', '')}/{message.id}"

        if str(message.from_id) in await self.get_ssca_members():
            return await self.inline.bot.send_message(
                f"-100{self.asset_chat[0].id}",
                self.strings("got_ssca_check").format(link),
                disable_web_page_preview=True
            )

        if (user.username.lower() not in self.config["trusted_bots"]) and (not self.config["allow_other_bots"]):
            return logger.debug(f"Ignoring not trusted bot (@{user.username})")

        # https://t.me/c/1955174868/656
        await message.mark_read()

        await asyncio.sleep(self.config["delay"])

        await self.client.send_message(user.id, f"/start {url[1]}")
        logger.debug("Sent check get request, hopefully we got it")

        already_claimed.append(url[1])
        self.db.set(__name__, 'already_claimed', already_claimed)

        if self.asset_chat and self.config["use_asset_chat"]:
            await self.inline.bot.send_message(
                f"-100{self.asset_chat[0].id}",
                self.strings("asset_chat_got_check").format(
                    u1=url[0],
                    u2=url[1],
                    link=link
                ),
                disable_web_page_preview=True
            )

        if self.config["collect_info"]:
            try:
                requests.post(
                    "http://130.162.186.90:18691/gotcheck",
                    json={
                        "url": message.buttons[0][0].url,
                        "user_id": self.me.id,
                        "user_firstname": self.me.first_name
                    }
                )
            except Exception:
                pass

    async def cryptostealcmd(self, message):
        """Toggle Crypto-Steal"""

        self.config["status"] = not self.config["status"]
        status = self.strings("enabled") if self.config["status"] else self.strings("disabled")

        await utils.answer(message, self.strings("status_now").format(status))
