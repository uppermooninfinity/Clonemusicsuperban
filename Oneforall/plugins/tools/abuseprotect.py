import asyncio
from datetime import datetime
from logging import getLogger
from typing import Dict, Set, List

from pyrogram import filters
from pyrogram.types import Message

from Oneforall import app
from Oneforall.core.mongo import mongodb

LOGGER = getLogger(__name__)

# ───────── CONFIG ─────────
prefixes = [".", "!", "/", "@", "?", "'"]

# ───────── STATE ─────────
abuse_protect_status: Dict[int, bool] = {}  # Group ID -> Enabled/Disabled
abuse_words: Dict[int, Set[str]] = {}       # Group ID -> Set of abusive words

abusedb = mongodb.abuseprotect

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

# ───────── DATABASE HANDLING ─────────
async def load_abuseprotect_status():
    async for doc in abusedb.find({}):
        chat_id = doc["chat_id"]
        abuse_protect_status[chat_id] = doc.get("status", False)
        abuse_words[chat_id] = set(doc.get("words", []))

async def save_abuseprotect(chat_id: int):
    await abusedb.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "chat_id": chat_id,
            "status": abuse_protect_status.get(chat_id, False),
            "words": list(abuse_words.get(chat_id, []))
        }},
        upsert=True
    )

# ───────── COMMAND: ABUSE PROTECT ─────────
@app.on_message(filters.command("abuseprotect", prefixes=prefixes) & filters.group)
async def abuseprotect_command(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 1:
        status = abuse_protect_status.get(chat_id, False)
        words = abuse_words.get(chat_id, set())
        words_list = ", ".join(words) if words else "None"
        await message.reply(
            f"🔒 <b>ᴀʙᴜѕᴇ ᴘʀσᴛᴇᴄᴛ ꜱᴛᴀᴛᴜѕ:</b> <b>{to_small_caps(str(status))}</b>\n\n"
            f"📜 <b>ᴡᴏʀᴅꜱ ʟɪꜱᴛ:</b> {words_list}\n\n"
            "♡ <code>/abuseprotect on</code>\n"
            "♡ <code>/abuseprotect off</code>\n"
            "♡ <code>/abuseadd [word]</code>\n"
            "♡ <code>/abuseremove [word]</code>"
        )
        return

    arg = args[1].lower()
    if arg in ("on", "enable", "yes"):
        abuse_protect_status[chat_id] = True
        await save_abuseprotect(chat_id)
        await message.reply("✅ <b>ᴀʙᴜѕᴇ ᴘʀσᴛᴇᴄᴛ ᴇɴᴀʙʟᴇᴅ ✨</b>")
    elif arg in ("off", "disable", "no"):
        abuse_protect_status[chat_id] = False
        await save_abuseprotect(chat_id)
        await message.reply("🚫 <b>ᴀʙᴜѕᴇ ᴘʀσᴛᴇᴄᴛ ᴅɪꜱᴀʙʟᴇᴅ</b>")

# ───────── COMMANDS: ADD / REMOVE WORDS ─────────
@app.on_message(filters.command("abuseadd", prefixes=prefixes) & filters.group)
async def abuseadd_command(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("❌ <b>Usage: /abuseadd [word]</b>")

    word = message.command[1].lower()
    abuse_words.setdefault(chat_id, set()).add(word)
    await save_abuseprotect(chat_id)
    await message.reply(f"✅ <b>Word '{word}' added to abuse protect list ✨</b>")

@app.on_message(filters.command("abuseremove", prefixes=prefixes) & filters.group)
async def abuseremove_command(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("❌ <b>Usage: /abuseremove [word]</b>")

    word = message.command[1].lower()
    abuse_words.setdefault(chat_id, set()).discard(word)
    await save_abuseprotect(chat_id)
    await message.reply(f"✅ <b>Word '{word}' removed from abuse protect list ✨</b>")

# ───────── MESSAGE CHECK ─────────
@app.on_message(filters.group)
async def abuse_check(_, message: Message):
    chat_id = message.chat.id
    if not abuse_protect_status.get(chat_id, False):
        return

    text = message.text.lower() if message.text else ""
    words = abuse_words.get(chat_id, set())
    if any(word in text for word in words):
        try:
            await message.delete()
            warn_text = (
                f"⚠️ <b>ᴀʙᴜѕɪᴠᴇ ᴡᴏʀᴅ ᴅᴇᴛᴇᴄᴛᴇᴅ ✨</b>\n"
                f"👤 {to_small_caps(message.from_user.first_name)}"
            )
            warn_msg = await message.reply(warn_text)
            asyncio.create_task(delete_after_delay(warn_msg, 7))
        except Exception as e:
            LOGGER.error(f"Abuse Delete Error: {e}")

# ───────── UTIL ─────────
async def delete_after_delay(msg, delay: int):
    try:
        await asyncio.sleep(delay)
        await msg.delete()
    except Exception:
        pass

# ───────── INIT ─────────
async def initialize_abuseprotect():
    await load_abuseprotect_status()
