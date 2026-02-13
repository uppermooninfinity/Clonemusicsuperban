import os
import aiohttp
import asyncio
from datetime import datetime
from logging import getLogger
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client

from Oneforall import app

LOGGER = getLogger(__name__)

# ───────── LOAD ENV ─────────
DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")  # Must be in .env

# ───────── STATE ─────────
nsfw_protection_enabled = {}  # chat_id -> bool

# ───────── SMALL CAPS ─────────
def to_small_caps(text: str):
    mapping = {
        "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ꜰ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ",
        "k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ",
        "u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ",
        "A":"ᴀ","B":"ʙ","C":"ᴄ","D":"ᴅ","E":"ᴇ","F":"ꜰ","G":"ɢ","H":"ʜ","I":"ɪ","J":"ᴊ",
        "K":"ᴋ","L":"ʟ","M":"ᴍ","N":"ɴ","O":"ᴏ","P":"ᴘ","Q":"ǫ","R":"ʀ","S":"s","T":"ᴛ",
        "U":"ᴜ","V":"ᴠ","W":"ᴡ","X":"x","Y":"ʏ","Z":"ᴢ"
    }
    return "".join(mapping.get(c, c) for c in text)

# ───────── COMMAND: TOGGLE NSFW ─────────
@app.on_message(filters.command("nsfwprotect") & filters.group)
async def toggle_nsfw(_, message: Message):
    chat_id = message.chat.id
    current = nsfw_protection_enabled.get(chat_id, False)
    nsfw_protection_enabled[chat_id] = not current
    status_text = "ON ✅" if nsfw_protection_enabled[chat_id] else "OFF ❌"
    await message.reply(f"🔞 <b>NSFW Protection is now {status_text}</b>")

# ───────── NSFW HANDLER ─────────
@app.on_message(filters.group & (filters.text | filters.photo | filters.video | filters.sticker))
async def nsfw_checker(_, message: Message):
    chat_id = message.chat.id
    if not nsfw_protection_enabled.get(chat_id, False):
        return
    if message.from_user.is_bot:
        return

    # Prepare content for DeepSeek
    content = ""
    if message.text:
        content = message.text
    elif message.photo or message.video or message.sticker:
        content = "media"

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}"}
            payload = {"message": content}
            async with session.post("https://api.deepseek.ai/nsfw", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    nsfw_score = data.get("nsfw_score", 0)
                    if nsfw_score >= 0.6:  # Threshold for NSFW
                        # Delete message
                        await message.delete()
                        # Warn user
                        await message.reply(f"⚠️ <b>{to_small_caps(message.from_user.first_name)}</b>, NSFW content is not allowed!")
                else:
                    LOGGER.error(f"NSFW API Error: {resp.status}")
    except Exception as e:
        LOGGER.error(f"NSFW Checker Error: {e}")
