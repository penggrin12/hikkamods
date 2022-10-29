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

from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class MyModulesMod(loader.Module):
    """See ur modules, without the commands"""

    strings = {
        "name": "MyModules",
        "modules": "❤️ All of the modules i have:"
    }

    strings_ru = {
        "name": "MyModules",
        "modules": "❤️ Все модули которые у меня есть:"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def mymodulescmd(self, message):
        """- See ur modules, without the commands"""

        result = f"{self.strings('modules')} | "

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__
            result += f"<code>{name}</code> | "

        await utils.answer(message, result)

