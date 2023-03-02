# -*- coding: utf-8 -*-

#   Friendly Telegram (telegram userbot)
#   Copyright (C) 2018-2020 The Authors

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#   если не подписан на t.me/keyzend
#   твоя мама шлюха
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   MODIFIED BY @PenggrinModules
#   ALL CREDITS GOES TO THE ORIGINAL CREATOR
#   ( @KeyZenD )

# meta developer: @KeyZenD
# requires: youtube_search

from .. import loader, utils
import logging

from youtube_search import YoutubeSearch


logger = logging.getLogger(__name__)


@loader.tds
class YTsearchMod(loader.Module):
    """Video search on youtube. Translated and Edited by @PenggrinModules"""

    strings = {
        "name": "YTsearch",
        "found": "❤️ Results by query: <code>{}</code>",
        "video": "Video",
    }
    strings_ru = {
        "found": "❤️ Результаты по запросу: <code>{}</code>",
        "video": "Видео",
    }

    @loader.command(ru_doc="<query:str OR reply> - Найти что-то на YouTube")
    async def ytsearchcmd(self, message):
        """<query:str OR reply> - Search something on YouTube"""
        text = utils.get_args_raw(message)

        if not text:
            reply = await message.get_reply_message()
            if not reply:
                await message.delete()
                return
            text = reply.raw_text

        results = YoutubeSearch(text, max_results=10).to_dict()
        result = self.strings("found").format(text)

        for r in results:
            video_type = "[Shorts]" if "shorts" in r["url_suffix"] else f"[{self.strings('video')}]"
            result += f'\n\n🔗 <a href="https://www.youtube.com{r["url_suffix"]}">{r["title"]}</a> <b>{video_type}</b> {r["duration"]}\nℹ️ <i>{r["views"]} | {r["publish_time"]}</i>\n👤 <b>{r["channel"]}</b>'

        await utils.answer(message, result)
