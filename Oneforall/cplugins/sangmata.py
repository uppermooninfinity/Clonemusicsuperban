import asyncio
import random

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import Message
from pyrogram.enums import ParseMode

from Oneforall import app
from Oneforall import userbot as us
from Oneforall.core.userbot import assistants


@app.on_message(filters.command("sg"))
async def sangmata_lookup(client: Client, message: Message):

    # ✨ Decorative Processing Message
    processing = await message.reply_text(
        "🔎 ᴘʀᴏᴄᴇssɪɴɢ ʜɪsᴛᴏʀɪᴄᴀʟ ᴜsᴇʀɴᴀᴍᴇs...",
        parse_mode=ParseMode.HTML
    )

    # Determine target
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await processing.edit_text(
            "⚠️ ᴜsᴀɢᴇ:\n"
            "/sg ᴜsᴇʀɴᴀᴍᴇ\n"
            "ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴡɪᴛʜ /sg",
            parse_mode=ParseMode.HTML
        )

    # Fetch user
    try:
        user = await client.get_users(user_id)
    except Exception:
        return await processing.edit_text(
            "❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ sᴘᴇᴄɪғɪᴇᴅ.",
            parse_mode=ParseMode.HTML
        )

    # Random sangmata bot
    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    selected_bot = random.choice(sangmata_bots)

    # Assistant check
    if 1 in assistants:
        ubot = us.one
    else:
        return await processing.edit_text(
            "❌ ᴜsᴇʀʙᴏᴛ ᴀssɪsᴛᴀɴᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",
            parse_mode=ParseMode.HTML
        )

    # Send ID
    try:
        sent = await ubot.send_message(selected_bot, str(user.id))
        await sent.delete()
    except Exception as e:
        return await processing.edit_text(
            f"❌ {str(e)}",
            parse_mode=ParseMode.HTML
        )

    await asyncio.sleep(2)

    # Get reply
    result = None
    async for msg in ubot.search_messages(selected_bot, limit=5):
        if msg.text:
            result = msg.text
            break

    if result:
        await message.reply_text(
            f"👤 ᴜsᴇʀ: {user.mention}\n"
            f"🆔 {user.id}\n\n"
            f"📜 ɴᴀᴍᴇ ʜɪsᴛᴏʀʏ:\n\n"
            f"{result}",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            "⚠️ ɴᴏ ʜɪsᴛᴏʀɪᴄᴀʟ ᴅᴀᴛᴀ ғᴏᴜɴᴅ.",
            parse_mode=ParseMode.HTML
        )

    # Clear history with bot
    try:
        peer = await ubot.resolve_peer(selected_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    await processing.delete()
