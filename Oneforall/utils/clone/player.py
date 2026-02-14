import os
import asyncio
import yt_dlp
import aiohttp

from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from youtubesearchpython.__future__ import VideosSearch

# ───────── GLOBALS ─────────

pytgcalls = None
YOUR_API_URL = None
FALLBACK_API_URL = "https://shrutibots.site"


# ───────── INIT ─────────

def init_pytgcalls(userbot):
    global pytgcalls
    pytgcalls = PyTgCalls(userbot)


# ───────── LOAD API URL ─────────

async def load_api_url():
    global YOUR_API_URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://pastebin.com/raw/rLsBhAQa",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    YOUR_API_URL = (await response.text()).strip()
                else:
                    YOUR_API_URL = FALLBACK_API_URL
    except:
        YOUR_API_URL = FALLBACK_API_URL


# ───────── SEARCH YOUTUBE ─────────

async def search_youtube(query: str):
    try:
        search = VideosSearch(query, limit=1)
        result = (await search.next())["result"][0]
        return result["link"]
    except:
        return None


# ───────── API DOWNLOAD ─────────

async def api_download(link: str):
    global YOUR_API_URL

    if not YOUR_API_URL:
        await load_api_url()

    video_id = link.split("v=")[-1].split("&")[0]

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{video_id}.mp3"

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "audio"}

            async with session.get(
                f"{YOUR_API_URL}/download",
                params=params,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:

                if response.status != 200:
                    return None

                data = await response.json()
                token = data.get("download_token")

                if not token:
                    return None

                stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=audio"

                async with session.get(
                    stream_url,
                    headers={"X-Download-Token": token},
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as file_response:

                    if file_response.status != 200:
                        return None

                    with open(file_path, "wb") as f:
                        async for chunk in file_response.content.iter_chunked(16384):
                            f.write(chunk)

                    return file_path

    except:
        return None


# ───────── YT_DLP FALLBACK ─────────

async def ytdlp_download(link: str):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            return ydl.prepare_filename(info)
    except:
        return None


# ───────── JOIN VC ─────────

async def join_vc(chat_id: int):
    if not pytgcalls:
        raise Exception("PyTgCalls not initialized")

    if not pytgcalls.is_connected(chat_id):
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped("silent.mp3")  # make sure this exists
        )


# ───────── STREAM ─────────

async def stream(chat_id: int, file_path: str):
    await pytgcalls.change_stream(
        chat_id,
        AudioPiped(file_path)
    )


# ───────── MAIN PLAY FUNCTION ─────────

async def play_music(userbot, chat_id: int, query: str, requested_by: int):
    try:
        if not pytgcalls:
            init_pytgcalls(userbot)
            await pytgcalls.start()

        # 🔎 If not link → search first
        if "youtube.com" not in query and "youtu.be" not in query:
            searched_link = await search_youtube(query)
            if not searched_link:
                return False
            query = searched_link

        # 1️⃣ Try API download
        file_path = await api_download(query)

        # 2️⃣ Fallback to yt_dlp
        if not file_path:
            file_path = await ytdlp_download(query)

        if not file_path:
            return False

        await join_vc(chat_id)
        await stream(chat_id, file_path)

        return True

    except Exception as e:
        print(f"Play Music Error: {e}")
        return False
