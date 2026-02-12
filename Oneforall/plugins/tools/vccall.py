import asyncio
from datetime import datetime
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw import functions

from Oneforall import app
from Oneforall.utils.database import get_assistant
from Oneforall.core.mongo import mongodb

LOGGER = getLogger(__name__)

# ───────── CONFIG ─────────

VC_LOG_CHANNEL_ID = -1003852280111  # 🔥 PUT YOUR VC LOG CHANNEL ID
prefixes = [".", "!", "/", "@", "?", "'"]

# ───────── STATE ─────────

vc_active_users: Dict[int, Set[int]] = {}
vc_logging_status: Dict[int, bool] = {}
vc_monitor_tasks: Dict[int, asyncio.Task] = {}

vcloggerdb = mongodb.vclogger


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


# ───────── DATABASE ─────────

async def load_vc_logger_status():
    async for doc in vcloggerdb.find({}):
        vc_logging_status[doc["chat_id"]] = doc["status"]
        if doc["status"]:
            await start_monitor(doc["chat_id"])

async def save_vc_logger_status(chat_id: int, status: bool):
    await vcloggerdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "status": status}},
        upsert=True
    )

async def get_vc_logger_status(chat_id: int) -> bool:
    if chat_id in vc_logging_status:
        return vc_logging_status[chat_id]
    doc = await vcloggerdb.find_one({"chat_id": chat_id})
    return doc["status"] if doc else False


# ───────── COMMAND: VC LOGGER ─────────

@app.on_message(filters.command("vclogger", prefixes=prefixes) & filters.group)
async def vclogger_command(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 1:
        status = await get_vc_logger_status(chat_id)
        await message.reply(
            f"🎧 <b>ᴠᴄ ʟσɢɢєʀ ꜱᴛᴧᴛᴜꜱ 🎙️✨:</b> <b>{to_small_caps(str(status))}</b>\n\n"
            "♡ <code>/vclogger on</code>\n"
            "♡ <code>/vclogger off</code>"
        )
        return

    arg = args[1].lower()

    if arg in ("on", "enable", "yes"):
        vc_logging_status[chat_id] = True
        await save_vc_logger_status(chat_id, True)
        await start_monitor(chat_id)
        await message.reply("✅ <b>ᴠᴄ ʟσɢɢєʀ ση 🎙️✨</b>")

    elif arg in ("off", "disable", "no"):
        vc_logging_status[chat_id] = False
        await save_vc_logger_status(chat_id, False)
        await stop_monitor(chat_id)
        await message.reply("🚫 <b>VC Logger Disabled</b>")


# ───────── COMMAND: VC MEMBERS ─────────

@app.on_message(filters.command("vcmembers", prefixes=prefixes) & filters.group)
async def vc_members_command(_, message: Message):
    chat_id = message.chat.id

    userbot = await get_assistant(chat_id)
    if not userbot:
        return await message.reply("❌ <b>Assistant session not found</b>")

    try:
        peer = await userbot.resolve_peer(chat_id)
        participants = await get_group_call_participants(userbot, peer)

        if not participants:
            return await message.reply("🎧 <b>No Active Voice Chat Found</b>")

        user_ids = [
            p.peer.user_id
            for p in participants
            if hasattr(p.peer, "user_id")
        ]

        users = await userbot.get_users(user_ids)

        text = "╭─── 🎙️ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀs ───╮\n\n"
        text += f"👥 ᴛᴏᴛᴀʟ : <code>{len(users)}</code>\n\n"

        for i, user in enumerate(users, start=1):
            mention = f'<a href="tg://user?id={user.id}">{to_small_caps(user.first_name)}</a>'
            text += f"{i}. {mention}\n"

        text += "\n╰──────────────────────╯"

        await message.reply(text)

    except Exception as e:
        LOGGER.error(f"VC Members Error: {e}")
        await message.reply("⚠️ <b>Error fetching VC members</b>")


# ───────── MONITOR CONTROL ─────────

async def start_monitor(chat_id: int):
    if chat_id in vc_monitor_tasks:
        return
    task = asyncio.create_task(monitor_vc_chat(chat_id))
    vc_monitor_tasks[chat_id] = task

async def stop_monitor(chat_id: int):
    task = vc_monitor_tasks.pop(chat_id, None)
    if task:
        task.cancel()
    vc_active_users.pop(chat_id, None)


# ───────── VC CORE ─────────

async def get_group_call_participants(userbot, peer):
    try:
        full = await userbot.invoke(
            functions.channels.GetFullChannel(channel=peer)
        )
        if not full.full_chat.call:
            return []

        call = full.full_chat.call
        res = await userbot.invoke(
            functions.phone.GetGroupParticipants(
                call=call,
                ids=[],
                sources=[],
                offset="",
                limit=100
            )
        )
        return res.participants

    except Exception:
        return []


async def monitor_vc_chat(chat_id: int):
    userbot = await get_assistant(chat_id)
    if not userbot:
        return

    while await get_vc_logger_status(chat_id):
        try:
            peer = await userbot.resolve_peer(chat_id)
            participants = await get_group_call_participants(userbot, peer)

            new_users = {
                p.peer.user_id for p in participants
                if hasattr(p.peer, "user_id")
            }

            old_users = vc_active_users.get(chat_id, set())

            for uid in new_users - old_users:
                asyncio.create_task(handle_user_join(chat_id, uid, userbot))

            for uid in old_users - new_users:
                asyncio.create_task(handle_user_leave(chat_id, uid, userbot))

            vc_active_users[chat_id] = new_users
            await asyncio.sleep(5)

        except asyncio.CancelledError:
            break
        except Exception as e:
            LOGGER.error(f"VC Monitor Error: {e}")
            await asyncio.sleep(5)


# ───────── BEAUTIFUL JOIN / LEAVE ─────────

async def handle_user_join(chat_id: int, user_id: int, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = f'<a href="tg://user?id={user_id}">{to_small_caps(user.first_name)}</a>'
        now = datetime.now().strftime("%H:%M:%S")

        text = (
            "╭─── 🎙️ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ───╮\n\n"
            f"➤ {mention}\n"
            "   ʜᴀs ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ ✨\n\n"
            f"⏰ {now}\n"
            "╰────────────────╯"
        )

        msg = await app.send_message(chat_id, text)
        asyncio.create_task(delete_after_delay(msg, 10))

    except Exception as e:
        LOGGER.error(f"Join Error: {e}")


async def handle_user_leave(chat_id: int, user_id: int, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = f'<a href="tg://user?id={user_id}">{to_small_caps(user.first_name)}</a>'
        now = datetime.now().strftime("%H:%M:%S")

        text = (
            "╭─── 🎙️ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ───╮\n\n"
            f"➤ {mention}\n"
            "   ʜᴀs ʟᴇꜰᴛ ᴛʜᴇ ᴠᴄ 👋\n\n"
            f"⏰ {now}\n"
            "╰────────────────╯"
        )

        msg = await app.send_message(chat_id, text)
        asyncio.create_task(delete_after_delay(msg, 10))

    except Exception as e:
        LOGGER.error(f"Leave Error: {e}")


async def delete_after_delay(msg, delay: int):
    try:
        await asyncio.sleep(delay)
        await msg.delete()
    except Exception:
        pass


# ───────── INIT ─────────

async def initialize_vc_logger():
    await load_vc_logger_status()
