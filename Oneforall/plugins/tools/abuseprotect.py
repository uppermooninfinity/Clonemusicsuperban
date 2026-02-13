import asyncio
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.types import Message

from Oneforall import app 
from config import OWNER_ID
from Oneforall.core.mongo import mongodb
from config import SUDO_USERS  # change path if needed

LOGGER = getLogger(__name__)

# ───────── CONFIG ─────────
prefixes = [".", "!", "/", "@", "?", "'"]

# ───────── STATE ─────────
abuse_protect_status: Dict[int, bool] = {}  # group enable/disable
GLOBAL_ABUSE_WORDS: Set[str] = set()       # global word list

abusedb = mongodb.abuseprotect

# ───────── PERMISSION CHECK ─────────
def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS

# ───────── DATABASE LOAD ─────────
async def load_abuseprotect_status():
    # Load global words
    doc = await abusedb.find_one({"_id": "global"})
    if doc:
        GLOBAL_ABUSE_WORDS.update(doc.get("words", []))

    # Load group status
    async for doc in abusedb.find({"_id": {"$ne": "global"}}):
        abuse_protect_status[doc["_id"]] = doc.get("status", False)

# ───────── SAVE FUNCTIONS ─────────
async def save_global_words():
    await abusedb.update_one(
        {"_id": "global"},
        {"$set": {"words": list(GLOBAL_ABUSE_WORDS)}},
        upsert=True
    )

async def save_group_status(chat_id: int):
    await abusedb.update_one(
        {"_id": chat_id},
        {"$set": {"status": abuse_protect_status.get(chat_id, False)}},
        upsert=True
    )

# ───────── ABUSE PROTECT COMMAND ─────────
@app.on_message(filters.command("abuseprotect", prefixes=prefixes) & filters.group)
async def abuseprotect_command(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 1:
        status = abuse_protect_status.get(chat_id, False)
        words_list = ", ".join(GLOBAL_ABUSE_WORDS) if GLOBAL_ABUSE_WORDS else "None"
        return await message.reply(
            f"🔒 Abuse Protect: <b>{status}</b>\n\n"
            f"📜 Global Words: {words_list}\n\n"
            "Commands:\n"
            "/abuseprotect on\n"
            "/abuseprotect off\n"
            "/abuseadd word\n"
            "/abuseremove word"
        )

    arg = args[1].lower()

    if arg in ("on", "enable", "yes"):
        abuse_protect_status[chat_id] = True
        await save_group_status(chat_id)
        await message.reply("✅ Abuse Protect Enabled ✨")

    elif arg in ("off", "disable", "no"):
        abuse_protect_status[chat_id] = False
        await save_group_status(chat_id)
        await message.reply("🚫 Abuse Protect Disabled")

# ───────── ADD WORD ─────────
@app.on_message(filters.command("abuseadd", prefixes=prefixes))
async def abuseadd_command(_, message: Message):

    if not is_authorized(message.from_user.id):
        return await message.reply("🚫 Only Owner & Sudo Users Can Add Words.")

    if len(message.command) < 2:
        return await message.reply("Usage: /abuseadd word")

    word = message.command[1].lower()

    GLOBAL_ABUSE_WORDS.add(word)
    await save_global_words()

    await message.reply(f"✅ Word '{word}' added globally ✨")

# ───────── REMOVE WORD ─────────
@app.on_message(filters.command("abuseremove", prefixes=prefixes))
async def abuseremove_command(_, message: Message):

    if not is_authorized(message.from_user.id):
        return await message.reply("🚫 Only Owner & Sudo Users Can Remove Words.")

    if len(message.command) < 2:
        return await message.reply("Usage: /abuseremove word")

    word = message.command[1].lower()

    GLOBAL_ABUSE_WORDS.discard(word)
    await save_global_words()

    await message.reply(f"✅ Word '{word}' removed globally ✨")

# ───────── MESSAGE CHECK ─────────
@app.on_message(filters.group)
async def abuse_check(_, message: Message):

    chat_id = message.chat.id

    if not abuse_protect_status.get(chat_id, False):
        return

    if not message.text:
        return

    text = message.text.lower()

    if any(word in text for word in GLOBAL_ABUSE_WORDS):
        try:
            await message.delete()
            warn = await message.reply(
                f"⚠️ Abusive word detected!\n"
                f"User: {message.from_user.mention}"
            )
            asyncio.create_task(delete_after_delay(warn, 7))
        except Exception as e:
            LOGGER.error(f"Abuse Delete Error: {e}")

# ───────── AUTO DELETE WARN ─────────
async def delete_after_delay(msg, delay: int):
    try:
        await asyncio.sleep(delay)
        await msg.delete()
    except:
        pass

# ───────── INIT ─────────
async def initialize_abuseprotect():
    await load_abuseprotect_status()
