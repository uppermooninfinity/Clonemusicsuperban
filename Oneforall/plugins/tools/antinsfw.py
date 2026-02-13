import asyncio
import aiohttp
import os
from logging import getLogger
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from datetime import datetime, timedelta
from dotenv import load_dotenv  # <--- to load .env

from Oneforall import app

# ───────── LOAD ENV ─────────
load_dotenv()  # loads variables from .env
DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")
DEESEEK_API_URL = "https://api.deepseek.ai/nsfw"
NSFW_THRESHOLD = 0.80
MUTE_DURATION_MINUTES = 5

LOGGER = getLogger(__name__)

# ───────── CONFIG ─────────
prefixes = [".", "!", "/", "@", "?", "'"]

# ───────── STATE ─────────
nsfw_protect_status = {}  # chat_id -> bool

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

# ───────── COMMAND: NSFW PROTECT ─────────
@app.on_message(filters.command("nsfwprotect", prefixes=prefixes) & filters.group)
async def nsfw_protect_command(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 1:
        status = nsfw_protect_status.get(chat_id, False)
        await message.reply(
            f"🔞 <b>ɴꜱꜰᴡ ᴘʀσᴛᴇᴄᴛσʀ:</b> <b>{to_small_caps(str(status))}</b>\n\n"
            "♡ <code>/nsfwprotect on</code>\n"
            "♡ <code>/nsfwprotect off</code>"
        )
        return

    arg = args[1].lower()

    if arg in ("on", "enable", "yes"):
        nsfw_protect_status[chat_id] = True
        await message.reply("✅ <b>ɴꜱꜰᴡ ᴘʀσᴛᴇᴄᴛσʀ ησ ✔️</b>")

    elif arg in ("off", "disable", "no"):
        nsfw_protect_status[chat_id] = False
        await message.reply("🚫 <b>ɴꜱꜰᴡ ᴘʀσᴛᴇᴄᴛσʀ σƒƒ ❌</b>")

# ───────── NSFW CHECK & ACTION ─────────
@app.on_message(filters.group & (filters.photo | filters.video | filters.sticker | filters.text))
async def nsfw_check_and_action(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not nsfw_protect_status.get(chat_id, False):
        return

    member = await app.get_chat_member(chat_id, user_id)
    if member.status in ["administrator", "creator"]:
        return

    try:
        nsfw_detected = False

        if message.text:
            nsfw_detected = await check_nsfw_text(message.text)
        else:
            file_path = await message.download(f"temp_{message.message_id}")
            nsfw_detected = await check_nsfw_file(file_path)

        if nsfw_detected:
            await message.delete()
            await warn_and_mute_user(chat_id, user_id, message)

    except Exception as e:
        LOGGER.error(f"NSFW action error: {e}")

# ───────── CHECK NSFW IMAGE/VIDEO/STICKER ─────────
async def check_nsfw_file(file_path: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("file", f, filename=file_path)
                headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}"}
                async with session.post(DEESEEK_API_URL, data=form, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        score = data.get("nsfw_score", 0)
                        return score >= NSFW_THRESHOLD
    except Exception as e:
        LOGGER.error(f"DeepSeek NSFW file check failed: {e}")
    return False

# ───────── CHECK NSFW TEXT ─────────
async def check_nsfw_text(text: str) -> bool:
    nsfw_keywords = ["nsfw", "sex", "xxx", "18+", "porn", "nude"]
    return any(word.lower() in text.lower() for word in nsfw_keywords)

# ───────── WARN & MUTE USER ─────────
async def warn_and_mute_user(chat_id: int, user_id: int, message: Message):
    mention = f'<a href="tg://user?id={user_id}">{to_small_caps(message.from_user.first_name)}</a>'
    now = datetime.now().strftime("%H:%M:%S")

    warn_msg = await message.reply(
        f"⚠️ <b>ɴꜱꜰᴡ ᴄᴏɴᴛᴇɴᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ!</b>\n"
        f"👤 {mention}\n"
        f"⏰ {now}\n"
        f"❌ ᴍᴇssage ᴅᴇʟᴇᴛᴇᴅ & ᴜsᴇʀ ᴍᴜᴛᴇᴅ {MUTE_DURATION_MINUTES}ᴍɪɴ"
    )

    until = datetime.utcnow() + timedelta(minutes=MUTE_DURATION_MINUTES)
    try:
        await app.restrict_chat_member(
            chat_id, user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until
        )
    except Exception as e:
        LOGGER.error(f"Failed to mute user: {e}")

    asyncio.create_task(delete_after_delay(warn_msg, 10))

# ───────── DELETE AFTER DELAY ─────────
async def delete_after_delay(msg, delay: int):
    try:
        await asyncio.sleep(delay)
        await msg.delete()
    except Exception:
        pass
