# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

import asyncio

logger = logging.getLogger(__name__)


@loader.tds
class PinnerMod(loader.Module):
    """Pin ya messages easily"""

    strings = {
        "name": "Pinner",
        "pinned": "📌 Message pinned!",
        "no_reply": "❌ Please reply with this command to a message you want to pin/delete."
    }

    strings_ru = {
        "pinned": "📌 Сообщение закреплено!",
        "no_reply": "❌ Пожалуйста ответьте этой командой на сообщение которое вы хотите закрепить/удалить."
    }

    async def pincmd(self, message):
        """Reply to a message to pin it"""
        reply = await message.get_reply_message()

        if not reply:
            msg = await utils.answer(message, self.strings("no_reply"))
            await asyncio.sleep(5)
            await msg.delete()
            return

        await reply.pin()
        msg = await utils.answer(message, self.strings("pinned"))
        await asyncio.sleep(5)
        await msg.delete()

    async def unpincmd(self, message):
        """Reply to a message to unpin it"""
        reply = await message.get_reply_message()

        if not reply:
            msg = await utils.answer(message, self.strings("no_reply"))
            await asyncio.sleep(5)
            await msg.delete()
            return

        await reply.unpin()
        await message.delete()
