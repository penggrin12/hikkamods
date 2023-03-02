# The MIT License (MIT)
# Copyright (c) 2023 penggrin

# meta developer: @PenggrinModules
# scope: hikka_only

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


class CryptoBalanceMod(loader.Module):
    """Check your balance in many Crypto Wallet Bots"""

    strings = {
        'name': 'CryptoBalance',
        'balance': '<emoji document_id=5336938396507969966>🪙</emoji> <b>Your balance in @{}:</b>\n\n{}'
    }

    strings_ru = {
        'balance': '<emoji document_id=5336938396507969966>🪙</emoji> <b>Твой баланс в @{}:</b>\n\n{}'
    }

    @staticmethod
    async def check_balance(bot, message):
        async with message.client.conversation(bot) as conv:
            walletrequest = await conv.send_message('/wallet')
            walletanswer = await conv.get_response()

            await walletrequest.delete()
            await walletanswer.delete()

        return walletanswer.text

    @loader.command(ru_doc="Проверить твой баланс в @CryptoBot")
    async def bcrypto(self, message):
        """Check your balance in @CryptoBot"""
        balance = ((await self.check_balance('CryptoBot', message))[18:])
        await utils.answer(message, self.strings('balance').format('CryptoBot', balance))

    @loader.command(ru_doc="Проверить твой баланс в @TonRocketBot")
    async def bton(self, message):
        """Check your balance in @TonRocketBot"""
        balance = (await self.check_balance('tonRocketBot', message))[21:]
        await utils.answer(message, self.strings('balance').format('tonRocketBot', balance))

    @loader.command(ru_doc="Проверить твой баланс в @xJetSwapBot")
    async def bjet(self, message):
        """Check your balance in @xJetSwapBot"""
        balance = (await self.check_balance('xJetSwapBot', message))[26:]
        await utils.answer(message, self.strings('balance').format('xJetSwapBot', balance))

    @loader.command(ru_doc="Проверить твой баланс в @CryptoTestNetBot")
    async def btest(self, message):
        """Check your balance in @CryptoTestNetBot"""
        balance = (await self.check_balance('CryptoTestnetBot', message))[18:]
        await utils.answer(message, self.strings('balance').format('CryptoTestnetBot', balance))

    @loader.command(ru_doc="Проверить твой баланс в @Wallet")
    async def bwallet(self, message):
        """Check your balance in @Wallet"""
        balance = (await self.check_balance('wallet', message))[22:]
        await utils.answer(message, self.strings('balance').format('wallet', balance))
