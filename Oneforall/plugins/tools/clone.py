import asyncio
import logging
import uuid
import requests
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid

from Oneforall import app
from Oneforall.core import userbot
from Oneforall.misc import SUDOERS
from Oneforall.utils.decorators.language import language
from Oneforall.utils.database.clonedb import (
    clonebotdb,
    has_user_cloned_any_bot,
    get_owner_id_from_db,
)
from Oneforall.utils.player import play_music

from config import (
    API_ID,
    API_HASH,
    OWNER_ID,
    SUPPORT_CHAT,
    CLONE_LOGGER,
)

log = logging.getLogger(__name__)
CLONES: set[int] = set()

# ===================== CONSTANTS ===================== #

C_BOT_DESC = (
    "🩷Wᴀɴᴛ ᴀ ʙᴏᴛ ʟɪᴋᴇ ᴛʜɪs? Cʟᴏɴᴇ ɪᴛ ɴᴏᴡ! ✅\n\n"
    "🔍Vɪsɪᴛ: @superban_probot\n"
    "📽️Sᴜᴘᴘᴏʀᴛ: @snowy_hometown"
)

C_BOT_COMMANDS = [
    {"command": "start", "description": "Start the bot"},
    {"command": "help", "description": "Help menu"},
    {"command": "play", "description": "Play music"},
    {"command": "pause", "description": "Pause music"},
    {"command": "resume", "description": "Resume music"},
    {"command": "skip", "description": "Skip track"},
    {"command": "end", "description": "End stream"},
    {"command": "ping", "description": "Ping bot"},
    {"command": "waifu", "description": "spawn a waifu pic in your chat"},
    {"command": "ban", "description": "ban a user in your chat"},
    {"command": "afk", "description": "you can go afk in chat"},
    {"command": "tts", "description": "enter a text and convert it to speech"}, 
    {"command": "slap", "description": "slap someone"},
    {"command": "lick", "description": "lick someone"},
    {"command": "tagall", "description": "tag everyone in gc"},
    {"command": "tagstop", "description": "stop tagging"}
    
]

# ===================== SAFE CLIENT ===================== #

def build_clone_client(bot_id: int, bot_token: str) -> Client:
    return Client(
        name=f"clone_{bot_id}_{uuid.uuid4().hex[:6]}",
        api_id=int(API_ID),
        api_hash=str(API_HASH),
        bot_token=str(bot_token),
        plugins=dict(root="Oneforall.cplugin"),
        in_memory=True,
    )

# ===================== CLONE BOT ===================== #

@app.on_message(filters.command("clone"))
@language
async def clone_bot(_, message, _t):
    user_id = message.from_user.id

    if await has_user_cloned_any_bot(user_id) and user_id != OWNER_ID:
        return await message.reply_text(_t["C_B_H_0"])

    if len(message.command) < 2:
        return await message.reply_text(_t["C_B_H_1"])

    bot_token = message.command[1].strip()
    msg = await message.reply_text(_t["C_B_H_2"])

    temp = build_clone_client(0, bot_token)

    try:
        await temp.start()
        bot = await temp.get_me()
    except (AccessTokenExpired, AccessTokenInvalid):
        return await msg.edit_text(_t["C_B_H_3"])
    except Exception as e:
        return await msg.edit_text(f"❌ `{e}`")
    finally:
        await temp.stop()

    clonebotdb.insert_one(
        {
            "bot_id": bot.id,
            "user_id": user_id,
            "name": bot.first_name,
            "username": bot.username,
            "token": bot_token,
            "date": datetime.utcnow(),
        }
    )

    CLONES.add(bot.id)

    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/setMyCommands",
            json={"commands": C_BOT_COMMANDS},
            timeout=10,
        )
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/setMyDescription",
            data={"description": C_BOT_DESC},
            timeout=10,
        )
    except Exception as e:
        log.warning(f"Command setup failed: {e}")

    await app.send_message(
        CLONE_LOGGER,
        f"🩷 ηєᴡ ᴄʟσηє ᴄʀєᴧᴛєᴅ 🥀\n\n"
        f"ʙσᴛ: @{bot.username}\n"
        f"σᴡηєʀ: [{message.from_user.first_name}](tg://user?id={user_id})",
    )

    await msg.edit_text(_t["C_B_H_6"].format(bot.username))

# ===================== CLONE PLAY ===================== #

@app.on_message(filters.command("play") & filters.group)
async def clone_play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Give a song name")

    try:
        await message.reply_text("❖ ᴘʟᴧʏɪηɢ ꜱσϻєᴛʜɪηɢ ʙєᴧᴜᴛɪғᴜʟ ғσʀ ʏσᴜ 💗")
        await play_music(
            userbot=userbot,
            chat_id=message.chat.id,
            query=" ".join(message.command[1:]),
            requested_by=message.from_user.id,
        )
    except Exception as e:
        log.error(f"Play failed: {e}")
        await message.reply_text("❌ Failed to play track.")

# ===================== DELETE CLONE ===================== #

@app.on_message(filters.command(["delclone", "delbot", "rmbot"]))
@language
async def delete_clone(_, message, _t):
    if len(message.command) < 2:
        return await message.reply_text(_t["C_B_H_8"])

    query = message.command[1].lstrip("@")
    bot = clonebotdb.find_one(
        {"$or": [{"username": query}, {"token": query}]}
    )

    if not bot:
        return await message.reply_text(_t["C_B_H_11"])

    owner = get_owner_id_from_db(bot["bot_id"])
    if message.from_user.id not in (OWNER_ID, owner):
        return await message.reply_text(
            _t["NOT_C_OWNER"].format(SUPPORT_CHAT)
        )

    clonebotdb.delete_one({"_id": bot["_id"]})
    CLONES.discard(bot["bot_id"])

    await message.reply_text(_t["C_B_H_10"])

# ===================== SAFE RESTART ===================== #

async def restart_bots():
    log.info("Restarting cloned bots...")

    for bot in clonebotdb.find():
        try:
            client = build_clone_client(bot["bot_id"], bot["token"])
            await client.start()
            me = await client.get_me()
            CLONES.add(me.id)
            await asyncio.sleep(1)
        except Exception as e:
            log.error(f"Clone skipped ({bot.get('username')}): {e}")

    await app.send_message(CLONE_LOGGER, "✅ All cloned bots restarted.")

# ===================== USER CLONES ===================== #

@app.on_message(filters.command(["mybots", "mybot"]))
@language
async def my_bots(_, message, _t):
    bots = list(clonebotdb.find({"user_id": message.from_user.id}))

    if not bots:
        return await message.reply_text(_t["C_B_H_16"])

    text = f"❄️ ʏσᴜʀ ᴄʟσηєᴅ ʙσᴛꜱ ({len(bots)}):\n\n"
    for b in bots:
        text += f"• @{b['username']}\n"

    await message.reply_text(text)

# ===================== ADMIN ===================== #

@app.on_message(filters.command("cloned") & SUDOERS)
@language
async def list_all_clones(_, message, _t):
    bots = list(clonebotdb.find())

    text = f"☘️ ᴛσᴛᴧʟ ᴄʟσηєᴅ: `{len(bots)}`\n\n"
    for b in bots:
        text += f"• @{b['username']} (`{b['bot_id']}`)\n"

    await message.reply_text(text)
