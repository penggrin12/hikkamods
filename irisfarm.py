 # The MIT License (MIT)
#
# Copyright (c) 2022 penggrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# meta developer: @penggrin
# scope: hikka_only
# scop: hikka_min 1.3.0

__version__ = (1, 0, 0)

import asyncio
from .. import loader, utils

import time
import logging

from telethon.tl.functions.messages import ReadMentionsRequest
from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)


@loader.tds
class IrisAutoFarmMod(loader.Module):
    """Auto farming for the Iris bot"""

    strings = {"name": "Iris auto-farm"}
    strings_ru = {"_cls_doc": "Фарм в Ирис боте"}

    _request_timeout = 3
    _last_iter = 0
    _cache = {}

    chat = None
    _client = None

    async def client_ready(self, client, db):
        self._client = client
        try:
            self.chat = await self._client.get_entity("irissupertop")
            await self._client(JoinChannelRequest(self.chat or "irissupertop"))
        except Exception as e:
            logger.error(e)
            pass # everything is fine, probably

        await self._client.send_message("irissupertop", "начинаю фарм")

    async def setdelaycmd(self, message):
        """<delay>"""
        args = utils.get_args(message)
        self.set("delay", int(args[0]))

    @loader.loop(interval=3, autostart=True)
    async def loop(self):
        if not self.get("delay") or self.get("delay") < time.time():
            try:
                await self._client.send_message("irissupertop", "ферма")
            except Exception as e:
                logger.error(f"For some reason, we didnt farm - {e}")

            self.set("delay", int(time.time() + ((60 * 60) * 4)))
            await self._client(ReadMentionsRequest(self.chat or "irissupertop"))