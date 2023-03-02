# module by:
# █▀ █▄▀ █ █░░ █░░ ▀█
# ▄█ █░█ █ █▄▄ █▄▄ █▄
#        /\_/\
#       ( o.o )
#        > ^ <
# █▀▄▀█ █▀▀ █▀█ █░█░█
# █░▀░█ ██▄ █▄█ ▀▄▀▄▀
#   you can edit this module
#            2022
# 🔒 Licensed under the AGPL-3.0
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @PenggrinModules
# meta pic: https://i.imgur.com/Q6TkhP2.jpeg
# meta banner: https://i.imgur.com/gwScaJj.jpeg

# edited by @Penggrin in 2023
# published by @PenggrinModules in 2023

__version__ = (0, 1, 0)

from .. import loader, utils
from telethon.tl.types import Message


class HetaSearcherMod(loader.Module):
    """Search for a module in @hikkamods_bot. Originally by @smeowcodes, see module source code for more details"""

    strings = {
        "name": "HetaSearcher",
        "mod": "<b><emoji document_id=5974405791996710295>🔽</emoji> Probably this module</b>",
        "not_found": "<b><emoji document_id=5032973497861669622>❌</emoji> Module not found</b>"
    }

    string_ru = {
        "mod": "<b><emoji document_id=5974405791996710295>🔽</emoji> Вероятно, это этот модуль</b>",
        "not_found": "<b><emoji document_id=5032973497861669622>❌</emoji> Модуль не найден</b>"
    }

    @loader.command(ru_doc="<имя модуля>")
    async def heta(self, message: Message):
        """<module name>"""
        args = utils.get_args_raw(message)
        result = await message.client.inline_query("hikkamods_bot", args)
        topic = utils.get_topic(message)

        if len(result) <= 0:
            await utils.answer(message, self.strings("not_found"))
            return

        await result[0].click(message.to_id, reply_to=topic or None)
        await message.edit(self.strings("mod"))
