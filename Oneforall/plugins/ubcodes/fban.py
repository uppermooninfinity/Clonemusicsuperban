from pyrogram import Client, filters
from Oneforall import app
from pyrogram.types import Message
import asyncio
from datetime import datetime
from config import STORAGE_CHANNEL_ID

@Client.on_message(filters.command(["fban"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def fban_handler(client: Client, message: Message):
    if len(message.command) < 3:
        await message.edit_text("Please provide a username or reply to a message and a reason.")
        await asyncio.sleep(5)
        await message.delete()
        return

    target = message.command[1]
    reason = " ".join(message.command[2:])

    if isinstance(target, str) and not target.isdigit():
        target_id = await resolve_username(client, target)
        if not target_id:
            await message.edit_text("Username not found.")
            await asyncio.sleep(5)
            await message.delete()
            return
    else:
        target_id = int(target)

    user_info = await client.get_users(target_id)
    target_first_name = user_info.first_name
    target_username = user_info.username or "No username"

    sender_info = message.from_user
    sender_first_name = sender_info.first_name
    sender_username = sender_info.username or "No username"
    sender_id = sender_info.id

    chat_info = message.chat
    chat_name = chat_info.title or "No title"
    chat_id = chat_info.id

    utc_now = datetime.utcnow()
    utc_time = utc_now.strftime('%Y-%m-%d %H:%M:%S')

    rose_bot_message = f"/fedban {target_id} {reason}"
    await client.send_message("MissRose_bot", rose_bot_message)

    await message.edit_text(f"ꜰᴇᴅʙᴀɴɴᴇᴅ {target_first_name} for reason: {reason}")
    await asyncio.sleep(3)
    await message.delete()

    support_message = (
        f"Fedban Report\n"
        f"Executed By:\n"
        f"Name: {sender_first_name}\n"
        f"Username: @{sender_username}\n"
        f"User ID: {sender_id}\n\n"
        f"Target:\n"
        f"Name: {target_first_name}\n"
        f"Username: @{target_username}\n"
        f"User ID: {target_id}\n\n"
        f"Group/Channel:\n"
        f"Name: {chat_name}\n"
        f"Group ID: {chat_id}\n\n"
        f"Reason:** {reason}\n\n"
        f"Time (UTC): {utc_time}\n"
    )
    await app.send_message(STORAGE_CHANNEL_ID, support_message)

async def resolve_username(client: Client, username: str):
    try:
        user = await client.get_users(username)
        return user.id
    except Exception:
        return None
