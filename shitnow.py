__version__ = (1, 0, 2)

#
#                 █░░ █ ▀█▀ █▀▀
#                 █▄▄ █ ░█░ ██▄
#
#               © Copyright 2023
#
#          Licensed under the GNU GPLv3
#      https://www.gnu.org/licenses/agpl-3.0.html

#
# лайт ну ты еблан, что с банером
# Modified by @penggrin at <https://t.me/penggrin>
# Published on @PenggrinModules at <https://t.me/penggrinmodules>
# See lines 3-10 for a license
#

# meta developer: @penggrinmodules
# requires: git+https://github.com/MarshalX/yandex-music-api@dev aiohttp
# meta desc: Module for yandex music. Based on SpotifyNow. (Modified by @penggrin for @penggrinmodules)

import logging
import aiohttp
from asyncio import sleep
from yandex_music import ClientAsync
from telethon import TelegramClient
from telethon.tl.types import Message
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils


logger = logging.getLogger(__name__)
logging.getLogger("yandex_music").propagate = False


@loader.tds
class YaNowMod(loader.Module):
    """Module for work with Yandex Music. Based on SpotifyNow. (Modified by @penggrin for @penggrinmodules)"""

    strings = {
        "name": "YaNow",
        "no_token": "<b>🚫 Specify a token in config!</b>",
        "playing": "<b>🎧 Now playing: </b><code>{}</code><b> - </b><code>{}</code>\n<b>🕐 {}</b>",
        "listening": "<b>🎙 Now listening: </b><code>{}</code>\n<b>🕐 {}</b>",
        "no_args": "<b>🚫 Provide arguments!</b>",
        "best_result": (
            "<b>🥇 Best result type: </b><code>{}</code>"
            "\n"
            "{}"
            "\n"
            "<b>Artists: </b><code>{}</code>"
            "\n"
            "<b>Tracks: </b><code>{}</code>"
            "\n"
            "<b>Albums: </b><code>{}</code>"
            "\n"
            "<b>Playlists: </b><code>{}</code>"
            "\n"
            "<b>Videos: </b><code>{}</code>"
            "\n"
            "<b>Users: </b><code>{}</code>"
            "\n"
            "<b>Podcasts: </b><code>{}</code>"
        ),
        "no_results": "<b>☹ No results found :(</b>",
        "autobioe": "<b>🔁 Autobio enabled</b>",
        "autobiod": "<b>🔁 Autobio disabled</b>",
        "lyrics": "<b>📜 Lyrics: \n{}</b>",
        "already_liked": "<b>🚫 Currently playing track is already liked!</b>",
        "liked": "<b>❤ Liked currently playing track!</b>",
        "not_liked": "<b>🚫 Currently playing track not liked!</b>",
        "disliked": "<b>💔 Disliked currently playing track!</b>",
        "my_wave": "<b>🌊 You listening to a track in 'my wave', i can't see it.</b>",
        "_cfg_yandexmusictoken": (
            "Yandex.Music account token"
            " (https://github.com/MarshalX/yandex-music-api/discussions/513?ysclid=liyx9ywznd272568668#discussion-3903521)"
        ),
        "_cfg_autobiotemplate": "Template for AutoBio",
        "no_lyrics": "<b>🚫 Track doesn't have lyrics.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "YandexMusicToken",
                None,
                lambda: self.strings["_cfg_yandexmusictoken"],
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "AutoBioTemplate",
                "🎧 {}",
                lambda: self.strings["_cfg_autobiotemplate"],
                validator=loader.validators.String(),
            ),
        )

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.db = db

        self._premium = getattr(await self.client.get_me(), "premium", False)

        if self.get("autobio", False):
            self.autobio.start()

    @loader.command()
    async def ynowcmd(self, message: Message):
        """Get now playing track"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            await utils.answer(message, self.strings["no_token"])
            return
        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return
        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        is_podcast = "podcast" in last_track.type

        info = await client.tracks_download_info(last_track.id, True)
        link = info[0].direct_link

        artists = ", ".join(last_track.artists_name())
        title = last_track.title
        if last_track.version:
            title += f" ({last_track.version})"
        else:
            pass

        caption = self.strings["playing"].format(
            utils.escape_html(artists),
            utils.escape_html(title),
            f"{last_track.duration_ms // 1000 // 60:02}:{last_track.duration_ms // 1000 % 60:02}",
        )

        if is_podcast:
            caption = self.strings["listening"].format(
                utils.escape_html(title),
                f"{last_track.duration_ms // 1000 // 60:02}:{last_track.duration_ms // 1000 % 60:02}",
            )

        try:
            lnk = last_track.id.split(":")[1]
        except Exception:
            lnk = last_track.id
        else:
            pass

        await self.inline.form(
            message=message,
            text=caption,
            reply_markup={
                "text": "song.link",
                "url": f"https://song.link/ya/{lnk}",
            },
            silent=True,
            audio={
                "url": link,
                "title": utils.escape_html(title),
                "performer": utils.escape_html(artists),
            }
            if not is_podcast
            else None,
        )

    @loader.command()
    async def ylyrics(self, message: Message):
        """Get now playing track lyrics"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

        queues = await client.queues_list()
        last_queue = await client.queue(queues[0].id)

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        try:
            lyrics = await client.tracks_lyrics(last_track.id)
            async with aiohttp.ClientSession() as session:
                async with session.get(lyrics.download_url) as request:
                    lyric = await request.text()

            text = self.strings["lyrics"].format(utils.escape_html(lyric))
        except Exception:
            text = self.strings["no_lyrics"]

        await utils.answer(message, text)

    @loader.command()
    async def ysearchcmd(self, message: Message):
        """Search tracks, artists, albums, playlists, users, podcasts, videos"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        results = await client.search(args)

        if results.best:
            type_ = results.best.type
            best = results.best.result

        if not results.best:
            await utils.answer(message, self.strings["no_results"])
            return

        if type_ in ["track", "podcast_episode"]:
            artists = ""
            if best.artists:
                artists = ", ".join(artist.name for artist in best.artists)
            best_result_text = f"<code>{artists}</code><b> - </b><code>{best.title}</code>"
        elif type_ == "artist":
            best_result_text = f"<code>{best.name}</code>"
        elif type_ in ["album", "podcast", "playlist", "video"]:
            best_result_text = f"<code>{best.title}</code>"

        await utils.answer(
            message,
            self.strings["best_result"].format(
                self.strings[type_],
                best_result_text,
                results.artists.total if results.artists else 0,
                results.tracks.total if results.tracks else 0,
                results.albums.total if results.albums else 0,
                results.playlists.total if results.playlists else 0,
                results.users.total if results.users else 0,
                results.videos.total if results.videos else 0,
                results.podcasts.total if results.podcasts else 0,
            ),
        )

    @loader.command()
    async def ybio(self, message: Message):
        """Show now playing track in your bio"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

        current = self.get("autobio", False)
        new = not current
        self.set("autobio", new)

        if new:
            await utils.answer(message, self.strings["autobioe"])
            self.autobio.start()
        else:
            await utils.answer(message, self.strings["autobiod"])
            self.autobio.stop()

    async def ylikecmd(self, message: Message):
        """❤"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        liked_tracks = await client.users_likes_tracks()
        liked_tracks = await liked_tracks.fetch_tracks_async()

        if isinstance(liked_tracks, list):
            if last_track in liked_tracks:
                await utils.answer(message, self.strings["already_liked"])
                return
            else:
                await last_track.like_async()
                await utils.answer(message, self.strings["liked"])
        else:
            await last_track.like_async()
            await utils.answer(message, self.strings["liked"])

    async def ydislikecmd(self, message: Message):
        """💔"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except Exception:
            logging.info("Указан неверный токен!")
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except Exception:
            await utils.answer(message, self.strings["my_wave"])
            return

        liked_tracks = await client.users_likes_tracks()
        liked_tracks = await liked_tracks.fetch_tracks_async()

        if isinstance(liked_tracks, list):
            if last_track in liked_tracks:
                await last_track.dislike_async()
                await utils.answer(message, self.strings["disliked"])

            else:
                await utils.answer(message, self.strings["not_liked"])
                return

        else:
            await utils.answer(message, self.strings["not_liked"])
            return

    @loader.loop(interval=60)
    async def autobio(self):
        client = ClientAsync(self.config["YandexMusicToken"])

        await client.init()
        queues = await client.queues_list()
        last_queue = await client.queue(queues[0].id)

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except Exception:
            return

        artists = ", ".join(last_track.artists_name())
        title = last_track.title

        text = self.config["AutoBioTemplate"].format(
            f"{artists} - {title}" + (f" ({last_track.version})" if last_track.version else "")
        )

        try:
            await self.client(UpdateProfileRequest(about=text[: 140 if self._premium else 70]))
        except FloodWaitError as e:
            logger.info(f"Sleeping {e.seconds}")
            await sleep(e.seconds)
            return
