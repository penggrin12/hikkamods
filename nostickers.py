# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class NoStickersMod(loader.Module):
    """Acts like a default tg setting "No stickers & gifs", but allows for some users to have permission to send stickers & gifs"""
    strings = {
        "name": "NoStickers",
        "allowed": "✅ <b>{}</b> can now send stickers and gifs!",
        "disallowed": "❌ <b>{}</b> cant send stickers and gifs anymore!",
        "noreply": "❌ Reply to a user you want affect with this command!",
        "config_enable": "Status of this module",
        "config_channels": "Channels that will be affected by this module",
    }

    strings_ru = {
        "name": "NoStickers",
        "allowed": "✅ <b>{}</b> теперь может отправлять стикеры и гифки!",
        "disallowed": "❌ <b>{}</b> больше не может отправлять стикеры и гифки!",
        "noreply": "❌ Ответьте на сообщение пользователя, доступ которого вы хотите изменить!",
        "config_enable": "Статус этого модуля",
        "config_channels": "Каналы которые будут задействованы этим модулем",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enable",
                True,
                lambda: self.strings("config_enable"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "channels",
                [],
                lambda: self.strings("config_channels"),
                validator=loader.validators.Series(loader.validators.Integer()),
            ),
        )

    @loader.command(ru_doc="- Ответом на сообщение человека которому вы хотите разрешить стикеры и гифки")
    async def allowcmd(self, message):
        """- Reply to a message of someone to allow them to send stickers and gifs"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("noreply"))
            return

        self.set(str(reply.from_id), True)
        target = await utils.get_user(reply)
        await utils.answer(reply, self.strings("allowed").format(f'<a href={utils.get_link(target)}>{target.first_name}</a>'))

    @loader.command(ru_doc="- Ответом на сообщение человека которому вы хотите запретить стикеры и гифки")
    async def disallowcmd(self, message):
        """- Reply to a message of someone to disallow them to send stickers and gifs"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("noreply"))
            return

        self.set(str(reply.from_id), False)
        target = await utils.get_user(reply)
        await utils.answer(reply, self.strings("disallowed").format(f'<a href={utils.get_link(target)}>{target.first_name}</a>'))

    @loader.watcher(out=False, no_commands=True)
    async def new_message(self, message):
        if not self.config["enable"]:
            return
        if not message.gif and not message.sticker:
            return
        
        me = await self.client.get_me()
        # 
        if (not self.get(str(message.from_id))) and (message.from_id != me.id):
            if message.peer_id.channel_id in self.config["channels"]:
                await message.delete()
                logger.debug("Just deleted a message!")

