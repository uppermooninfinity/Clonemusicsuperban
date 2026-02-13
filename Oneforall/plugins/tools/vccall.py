import asyncio
from datetime import datetime
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw import functions
from pyrogram.errors import FloodWait

from Oneforall import app
from Oneforall.utils.database import get_assistant
from Oneforall.core.mongo import mongodb

LOGGER = getLogger(__name__)

# ───────── CONFIG ─────────

VC_LOG_CHANNEL_ID = -1003852280111
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
        "k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"ꜱ","t":"ᴛ",
        "u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ"
    }
    return "".join(mapping.get(c.lower(), c) for c in text)


# ───────── DATABASE ─────────

async def save_status(chat_id: int, status: bool):
    await vcloggerdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "status": status}},
        upsert=True
    )
    vc_logging_status[chat_id] = status


async def get_status(chat_id: int) -> bool:
    if chat_id in vc_logging_status:
        return vc_logging_status[chat_id]
    doc = await vcloggerdb.find_one({"chat_id": chat_id})
    status = doc["status"] if doc else False
    vc_logging_status[chat_id] = status
    return status


# ───────── COMMAND ─────────

@app.on_message(filters.command("vclogger", prefixes=prefixes) & filters.group)
async def vclogger_cmd(_, message: Message):
    chat_id = message.chat.id
    args = message.command

    if len(args) == 1:
        status = await get_status(chat_id)
        return await message.reply(
            f"🎧 <b>ᴠᴄ ʟσɢɢєʀ —:</b> <code>{status}</code>"
        )

    arg = args[1].lower()

    if arg in ["on", "enable"]:
        await save_status(chat_id, True)
        await start_monitor(chat_id)
        await message.reply("<i><u>✅ <b>ᴠᴄ ʟσɢɢєʀ — єηᴧʙʟєᴅ 🟢</b></u></i>")

    elif arg in ["off", "disable"]:
        await save_status(chat_id, False)
        await stop_monitor(chat_id)
        await message.reply("<i><u>🚫 <b>ᴠᴄ ʟσɢɢєʀ — ᴅɪꜱᴧʙʟєᴅ 🔴</b></u></i>")


# ───────── MONITOR CONTROL ─────────

async def start_monitor(chat_id: int):
    if chat_id in vc_monitor_tasks:
        return

    task = asyncio.create_task(monitor_vc(chat_id))
    vc_monitor_tasks[chat_id] = task


async def stop_monitor(chat_id: int):
    task = vc_monitor_tasks.pop(chat_id, None)
    if task:
        task.cancel()

    vc_active_users.pop(chat_id, None)


# ───────── FETCH PARTICIPANTS ─────────

async def fetch_participants(userbot, peer):
    try:
        full = await userbot.invoke(
            functions.channels.GetFullChannel(channel=peer)
        )

        if not full.full_chat.call:
            return []

        call = full.full_chat.call
        offset = ""
        all_participants = []

        while True:
            result = await userbot.invoke(
                functions.phone.GetGroupParticipants(
                    call=call,
                    ids=[],
                    sources=[],
                    offset=offset,
                    limit=100
                )
            )

            all_participants.extend(result.participants)

            if not result.next_offset:
                break

            offset = result.next_offset

        return all_participants

    except Exception as e:
        LOGGER.error(f"Fetch Error: {e}")
        return []


# ───────── MAIN MONITOR ─────────

async def monitor_vc(chat_id: int):
    LOGGER.info(f"Started VC monitor for {chat_id}")

    while await get_status(chat_id):
        try:
            userbot = await get_assistant(chat_id)
            if not userbot:
                await asyncio.sleep(5)
                continue

            peer = await userbot.resolve_peer(chat_id)
            participants = await fetch_participants(userbot, peer)

            new_users = {
                p.peer.user_id
                for p in participants
                if hasattr(p.peer, "user_id")
            }

            old_users = vc_active_users.get(chat_id, set())

            joined = new_users - old_users
            left = old_users - new_users

            for uid in joined:
                asyncio.create_task(handle_join(chat_id, uid, userbot))

            for uid in left:
                asyncio.create_task(handle_leave(chat_id, uid, userbot))

            vc_active_users[chat_id] = new_users

            if not participants:
                vc_active_users[chat_id] = set()

            await asyncio.sleep(4)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except asyncio.CancelledError:
            break

        except Exception as e:
            LOGGER.error(f"Monitor Error: {e}")
            await asyncio.sleep(5)

    LOGGER.info(f"Stopped VC monitor for {chat_id}")


# ───────── LOG HANDLERS ─────────

async def handle_join(chat_id: int, user_id: int, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = f'<a href="tg://user?id={user_id}">{to_small_caps(user.first_name)}</a>'

        now = datetime.now().strftime("%d-%m-%Y | %H:%M:%S")

        text = (
            "╭── 🎙️ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ──╮\n\n"
            f"➤ {mention}\n"
            "   ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ ✨\n\n"
            f"⏰ {now}\n"
            "╰────────────────╯"
        )

        await app.send_message(VC_LOG_CHANNEL_ID or chat_id, text)

    except Exception as e:
        LOGGER.error(f"Join Error: {e}")


async def handle_leave(chat_id: int, user_id: int, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = f'<a href="tg://user?id={user_id}
