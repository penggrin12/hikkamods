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
class PostModuleMod(loader.Module):
    """Description"""

    strings = {
        "name": "PostModule",
    }
    strings_ru = {
        "name": "PostModule",
    }

    async def client_ready(self, client, db):
        self.client = client

    async def postmodulecmd(self, message):
        """<name> <short description> <norus (true, false)> <noeng (true, false)> <link> - ||| in description will make a new line (example: FOO|||BAR)"""
        args = utils.get_args(message)
        desc = args[1].replace('|||', '\nℹ️ ').replace('|', ' ')
        rus = '❗️ No Russian translation!\n' if args[2].lower() == 'true' else ''
        eng = '❗️ No English translation!\n' if args[3].lower() == 'true' else ''

        await utils.answer(message, f"💻 <code>{args[0]}</code>\nℹ️ {desc}\n\n{rus}{eng}\n🌘 <code>.dlmod {args[4]}</code>")

