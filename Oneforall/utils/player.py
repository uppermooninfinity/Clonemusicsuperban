from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

pytgcalls = PyTgCalls(userbot)  # initialize

async def extract_audio(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        return ydl.prepare_filename(info)

async def join_vc(chat_id):
    if not pytgcalls.is_connected(chat_id):
        await pytgcalls.join_group_call(chat_id, AudioPiped("silent.mp3"))

async def pytgcalls_stream(chat_id, file_path):
    await pytgcalls.change_stream(
        chat_id,
        AudioPiped(file_path)
    )
