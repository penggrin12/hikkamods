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

# meta developer: @penggrinmods
# scope: hikka_only

from telethon.tl.types import Message
from .. import loader, utils

import requests, random


@loader.tds
class FunApisMod(loader.Module):
    """Many different api's from all over the internet!"""

    strings = {
        "name": "FunApisMod",
    }

    async def client_ready(self, client, db):
        self.client = client

    async def __send(self, message: Message, text: str, photo = None):
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

    async def cathttpcmd(self, message: Message):
        """<http code> - Get a cat that represents a certain http code"""
        args = utils.get_args(message)
        await self.__send(message, utils.ascii_face(), photo = f"https://http.cat/{args[0]}")

    async def catpiccmd(self, message: Message):
        """Get a random cat picture"""
        json = requests.get("https://aws.random.cat/meow").json()
        await self.__send(message, utils.ascii_face(), photo = json["file"])

    async def dogpiccmd(self, message: Message):
        """Get a random dog picture"""
        json = requests.get("https://random.dog/woof.json").json()
        await self.__send(message, utils.ascii_face(), photo = json["url"])

    async def jokecmd(self, message: Message):
        """Get a random joke"""
        json = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        await self.__send(message, f'1️⃣ {json["setup"]}\n2️⃣ <span class="tg-spoiler">{json["punchline"]}</span>')

    async def chuckcmd(self, message: Message):
        """Get a hand curated Chuck Norris fact"""
        json = requests.get("https://api.chucknorris.io/jokes/random").json()
        await self.__send(message, f"Chuck Norris fact 👇\n\n{json['value']}")

    async def uselesscmd(self, message: Message):
        """Get a random useless fact"""
        json = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        await self.__send(message, f"Useless fact 👇\n\n{json['text']}")

    async def memescmd(self, message: Message):
        """Get a random meme"""
        json = requests.get("https://api.imgflip.com/get_memes").json()
        meme = random.choice(json['data']['memes'])
        await self.__send(message, f"{meme['name']}", photo = meme['url'])

    async def aboutmecmd(self, message: Message):
        """<firstname> - Get some information about your name"""
        args = utils.get_args(message)
        name = args[0].lower()
        age = requests.get(f"https://api.agify.io/?name={name}").json()
        gender = requests.get(f"https://api.genderize.io/?name={name}").json()

        if (age['age'] != None) and (gender['gender'] != None):
            await self.__send(message, f"👋 Hey, {name}!\n\nYou are a {gender['gender']}, with probability of about {gender['probability'] * 100}%.\nAnd also you probably about {age['age']} years old.\n\nRight?")
        else:
            await self.__send(message, f"Umm.. Something tells us, thats not a name...\n(Or just not an american one!)")

        