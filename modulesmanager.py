#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/cloud_icon.png
# meta banner: https://mods.hikariatama.ru/badges/cloud.jpg
# meta developer: @PenggrinModules
#                     ^^^ Originally made by @hikarimods

# scope: hikka_only
# scope: hikka_min 1.2.10

# edited by @Penggrin in 2023
# published by @PenggrinModules in 2023

import difflib
import inspect
import io
import logging
import os
import copy
import contextlib

from telethon.tl.types import Message
from .. import loader, utils
from ..types import DragonModule

CORE_MODULES_DIR = os.path.join(loader.BASE_DIR, "hikka", "modules")
logger = logging.getLogger(__name__)


@loader.tds
class ModulesManagerMod(loader.Module):
    """Hikka Modules Manager, originally made by @hikarimods"""

    strings = {
        "name": "ModulesManager",
        "args": "<emoji document_id=5974229895906069525>❓</emoji> <b>Args not specified</b>",
        "404": "<emoji document_id=5974229895906069525>❓</emoji> <b>Module not found</b>",
        "no_class": "<emoji document_id=5974229895906069525>❓</emoji> <b>What class needs to be unloaded?</b>",
        "unloaded": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Module {} unloaded.</b>",
        "not_unloaded": "<emoji document_id=5312526098750252863>🚫</emoji> <b>Module not unloaded.</b>",
        "cannot_unload_lib": "<emoji document_id=5454225457916420314>😖</emoji> <b>You can't unload library</b>",
    }

    strings_ru = {
        "_cls_doc": "Менеджер модулей Хикки, оригинальный автор: @hikarimods",
        "args": "<emoji document_id=5974229895906069525>❓</emoji> <b>Нет аргументов</b>",
        "404": "<emoji document_id=5974229895906069525>❓</emoji> <b>Модуль не найден</b>",
        "no_class": "<emoji document_id=5974229895906069525>❓</emoji> <b>А что выгружать то?</b>",
        "unloaded": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Модуль {} выгружен.</b>",
        "not_unloaded": "<emoji document_id=5312526098750252863>🚫</emoji> <b>Модуль не выгружен.</b>",
        "cannot_unload_lib": "<emoji document_id=5454225457916420314>😖</emoji> <b>Ты не можешь выгрузить библиотеку</b>",
    }

    async def unload_module(self, classname: str):
        """Remove module and all stuff from it"""
        worked = []

        for module in self.allmodules.modules:
            if classname.lower() in (
                module.name.lower(),
                module.__class__.__name__.lower(),
            ):
                worked += [module.__class__.__name__]

                path1 = os.path.join(loader.LOADED_MODULES_DIR, f"{module.__class__.__name__}_{self.client.tg_id}.py")
                path2 = os.path.join(CORE_MODULES_DIR, f"{module.__module__.replace('hikka.modules.', '')}.py")

                if os.path.isfile(path1):
                    os.remove(path1)

                if ("http" not in module.__module__) and (os.path.isfile(path2)):
                    os.remove(path2)

                self.allmodules.modules.remove(module)

                await module.on_unload()

                self.allmodules.unregister_raw_handlers(module, "unload")
                self.allmodules.unregister_loops(module, "unload")
                self.allmodules.unregister_commands(module, "unload")
                self.allmodules.unregister_watchers(module, "unload")
                self.allmodules.unregister_inline_stuff(module, "unload")

        return worked

    @loader.owner
    @loader.command(ru_doc="<имя модуля> - Выгрузить любой модуль")
    async def cunloadmod(self, message: Message):
        """<module name> - Unload any module by class name"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings("no_class"))
            return

        instance = self.lookup(args, include_dragon=True)

        if issubclass(instance.__class__, loader.Library):
            await utils.answer(message, self.strings("cannot_unload_lib"))
            return

        if isinstance(instance, DragonModule):
            worked = [instance.name] if self.allmodules.unload_dragon(instance) else []
        else:
            worked = await self.unload_module(args)

        if not self.allmodules.secure_boot:
            self.set(
                "loaded_modules",
                {
                    mod: link
                    for mod, link in self.get("loaded_modules", {}).items()
                    if mod not in worked
                },
            )

        msg = (
            self.strings("unloaded").format(
                ", ".join(
                    [(mod[:-3] if mod.endswith("Mod") else mod) for mod in worked]
                ),
            )
            if worked else self.strings("not_unloaded")
        )

        await utils.answer(message, msg)

    @loader.command(ru_doc="<имя модуля> - Отправить ссылку на любой модуль")
    async def cmlcmd(self, message: Message):
        """<module name> - Send link to any module"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        try:
            try:
                class_name = next(
                    module.strings["name"]
                    for module in self.allmodules.modules
                    if args.lower() == module.strings["name"].lower()
                )
            except Exception:
                try:
                    class_name = next(
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    )
                except Exception:
                    await utils.answer(message, self.strings("404"))
                    return

            module = next(
                filter(
                    lambda mod: class_name.lower() == mod.strings["name"].lower(),
                    self.allmodules.modules,
                )
            )

            sys_module = inspect.getmodule(module)

            link = module.__origin__

            text = (
                f"<emoji document_id=5974492756494519709>🔗</emoji> <b>{utils.escape_html(class_name)}</b>"
                if not utils.check_url(link)
                else (
                    f'<emoji document_id=5974492756494519709>🔗</emoji> <b><a href="{link}">Link</a> for '
                    f"{utils.escape_html(class_name)}:</b> "
                    f'<code>{link}</code>\n\n'
                )
            )

            file = io.BytesIO(sys_module.__loader__.data)
            file.name = f"{class_name}.py"
            file.seek(0)

            reply = (await message.get_reply_message()) or utils.get_topic(message) or None
            await message.respond(text, file=file, reply_to=reply)

            if message.out:
                await message.delete()
        except Exception as e:
            logger.error(e)
            await utils.answer(message, self.strings("404"))
