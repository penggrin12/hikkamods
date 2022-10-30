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

from telethon.tl.functions.account import UpdateProfileRequest
import time, logging, datetime, asyncio
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ActiveTimerMod(loader.Module):
    """Shows a (since my last message) timer in your lastname"""

    strings = {"name": "ActiveTimerMod"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_divider",
                None,
                lambda: "Custom divider, Defaults to | (example: <b>Bob (divider) 0:15:08</b>)",
            ),
            loader.ConfigValue(
                "custom_message",
                None,
                lambda: "Custom divider, Defaults to nothing (example: <b>Bob | (message) 0:15:08</b>)",
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.me = await self.client.get_me()

        if not self.get("timer"):
            self.set("timer", 0)

        logger.info("activetimer")

    def get_timer_emoji(self, timer):
        if timer > 10800:
            return "💤"
        elif timer > 3000:
            return "❤️"
        elif timer > 900:
            return "💛"
        else:
            return "💚"

    async def get_new_name(self):
        #return f"{self.me.last_name.split(' | ')[0]} | {str(datetime.timedelta(seconds=timer))}"
        return f'{self.config["custom_divider"] or "|"} {self.config["custom_message"] or self.get_timer_emoji(self.get("timer"))} {str(datetime.timedelta(seconds=self.get("timer")))}'

    async def setname(self):
        #try:
        newName = await self.get_new_name()
        await self.client(UpdateProfileRequest(first_name=None, last_name=newName, about=None))
        #except Exception as e:
        #    logger.error(e)

    async def settimercmd(self, message):
        """<timer> - You probably dont wanna use it"""
        args = utils.get_args(message)
        self.set("timer", int(args[0]))
        await self.setname()
        await utils.answer(message, f"✅ люти пон, таймер теперь: {str(datetime.timedelta(seconds=int(args[0])))}")

    @loader.watcher(only_messages=True, out=True, no_commands=True)
    async def newMessage(self, message):
        logger.debug("New Message By A User!")
        self.set("timer", 0)
        #await self.setname()
        
    @loader.loop(interval=30, autostart=True)
    async def loop(self):
        self.set("timer", self.get("timer") + 30)
        await self.setname()
