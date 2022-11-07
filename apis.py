# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# scope: hikka_only

from .. import loader, utils
import logging

import requests
import random

logger = logging.getLogger(__name__)


@loader.tds
class FunApisMod(loader.Module):
    """Many different api's from all over the internet!"""

    strings = {
        "name": "FunApisMod",
        "chuck": "❤️ Chuck Norris fact",
        "useless": "❤️ Useless fact",
        "name_error": "❌ Umm.. Something tells us, thats not a name...\n(Or just not an american one!)",
        "name_success": "👋 Hey, {}!\n\n❤️ You are a {}, with probability of about {}%.\n❤️ And also you probably about {} years old.\n\n❔ Right?",
        "no_zenserp_token": "❌ You dont have <b>zenserp</b> token!\n❓ You can set it in <code>.config</code>",
        "search_success": "❤️ Here are {} results that i have found for you!",
    }
    strings_ru = {
        "chuck": "❤️ Факт про Чака Норриса",
        "useless": "❤️ Безполезный факт",
        "name_error": "❌ Хмм.. Что-то нам подсказывает, что это не имя...\n(Либо просто не американское!)",
        "name_success": "👋 Хей, {}!\n\nВы {}, с вероятностью примерно {}%.\nА также вам примерно {} лет.\n\nВерно?",
        "no_zenserp_token": "❌ У вас нет <b>zenserp</b> токена!\n❓ Вы можете его поставить в <code>.config</code>",
        "search_success": "❤️ Вот {} результата которые я для вас нашёл!",
    }

    def list_to_str(self, a = None):
        if (a is None) or (len(a) < 1):
            return ""

        return ' '.join(str(b) for b in a)

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "zenserp_token",
                None,
                lambda: "Get this token from <code>zenserp.com</code> to access <code>.gdz</code> command",
            ),
        )

    async def __send(self, message, text: str, photo = None):
        reply = await message.get_reply_message()

        if photo:
            if reply:
                result = await self.client.send_file(message.peer_id, caption = text, file = photo, reply_to = reply)
            else:
                result = await self.client.send_file(message.peer_id, caption = text, file = photo)
        else:
            if reply:
                result = await reply.reply(text)
            else:
                result = await message.respond(text)

        #await utils.answer(message, text, photo=photo)
        await message.delete()

    async def __search(self, message, query, num = 3, lang = "ru"):
        if not self.config["zenserp_token"]:
            await utils.answer(message, self.strings("no_zenserp_token"))
            return

        params = {"q": str(query), "gl": str(lang), "hl": str(lang), "num": str(num)}
        response = requests.get('https://app.zenserp.com/api/v2/search', headers={"apikey": self.config["zenserp_token"]}, params=params)

        return response.json()

    @loader.command(ru_doc="<http code:int> - Получить котика на тему http кода")
    async def cathttpcmd(self, message):
        """<http code:int> - Get a cat that represents a certain http code"""
        args = utils.get_args(message)
        await self.__send(message, utils.ascii_face(), photo = f"https://http.cat/{args[0]}")

    @loader.command(ru_doc="- Получить случайную картинку котика")
    async def catpiccmd(self, message):
        """- Get a random cat picture"""
        json = requests.get("https://aws.random.cat/meow").json()
        await self.__send(message, utils.ascii_face(), photo = json["file"])

    @loader.command(ru_doc="- Получить случайную картинку собачки")
    async def dogpiccmd(self, message):
        """- Get a random dog picture"""
        json = requests.get("https://random.dog/woof.json").json()
        await self.__send(message, utils.ascii_face(), photo = json["url"])

    @loader.command(ru_doc="- Получить случайную шутку")
    async def jokecmd(self, message):
        """- Get a random joke"""
        json = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        await self.__send(message, f'1️⃣ {json["setup"]}\n2️⃣ <tg-spoiler>{json["punchline"]}</tg-spoiler>')

    @loader.command(ru_doc="- Получить случайный Факт про Чака Норриса")
    async def chuckcmd(self, message):
        """- Get a hand curated Chuck Norris fact"""
        json = requests.get("https://api.chucknorris.io/jokes/random").json()
        await self.__send(message, f"{self.strings('chuck')} 👇\n\n{json['value']}")

    @loader.command(ru_doc="- Получить случайный Безполезный факт")
    async def uselesscmd(self, message):
        """- Get a random useless fact"""
        json = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        await self.__send(message, f"{self.strings('useless')} 👇\n\n{json['text']}")

    @loader.command(ru_doc="Получить случайную заготовку для мема")
    async def memetemplatecmd(self, message):
        """- Get a random meme template"""
        json = requests.get("https://api.imgflip.com/get_memes").json()
        meme = random.choice(json['data']['memes'])
        await self.__send(message, f"{meme['name']}", photo = meme['url'])

    @loader.command(ru_doc="Получить немного информации про ваше имя")
    async def aboutmecmd(self, message):
        """<firstname:str> - Get some information about someones name"""
        args = utils.get_args(message)
        name = args[0].lower()
        age = requests.get(f"https://api.agify.io/?name={name}").json()
        gender = requests.get(f"https://api.genderize.io/?name={name}").json()

        if (age['age'] != None) and (gender['gender'] != None):
            await self.__send(message, self.strings("name_success").format(name, gender["gender"], gender['probability'] * 100, age["age"]))
        else:
            await self.__send(message, self.strings("name_error"))

    @loader.command(ru_doc="<query:str> - Найти гдз, показывает до 3 результатов")
    async def gdzcmd(self, message):
        """<query:str> - Will search "гдз <query>" and show up to 3 results"""
        q = utils.get_args_raw(message)

        response = await self.__search(message, f"гдз {q}")
        result = f"{self.strings('search_success').format(len(response))}\n\n"

        for i in response["organic"]:
            result += f'📄 <b>{i["title"]}</b>\n🔗 {i["url"]}\n\n'

        await self.__send(message, result)

    @loader.command(ru_doc="<query:str> - Найти что угодно, показывает до 10 результатов")
    async def searchcmd(self, message):
        """<query:str> - Will search "<query>" and show up to 10 results"""
        q = utils.get_args_raw(message)

        response = await self.__search(message, q)
        result = f"{self.strings('search_success').format(len(response))}\n\n"

        for i in response["organic"]:
            result += f'📄 <b>{i["title"]}</b>\n🔗 {i["url"]}\n\n'

        await self.__send(message, result)

        
