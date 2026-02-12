from pyrogram.enums import ParseMode

from config import LOGGER_ID
from Oneforall import app
from Oneforall.utils.database import is_on_off


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""<blockquote><i>
<b><u>{app.mention} ηєᴡ ꜱᴛʀєᴧϻ ʀєQᴜєꜱᴛ ɪᴅєηᴛɪꜰɪєᴅ 🚀🎶</u></b>

<b>ɢʀσᴜᴘ ᴜηɪQᴜє ɪᴅ 🆔✨ :</b> <code>{message.chat.id}</code>
<b>ɢʀσᴜᴘ ηᴧϻє 👥✨ :</b> {message.chat.title}
<b>ɢʀσᴜᴘ ᴜꜱєʀηᴧϻє 🌐✨:</b> @{message.chat.username}

<b>ᴜꜱєʀ ɪᴅ 🆔✨ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє 🌿✨ :</b> {message.from_user.mention}
<b>ᴅєᴛєᴄᴛєᴅ ᴜꜱєʀηᴧϻє 🛰️✨ :</b> @{message.from_user.username}

<b>ꜱєᴧʀᴄʜ 🔎✨:</b> {message.text.split(None, 1)[1]}
<b>ꜱᴛʀєᴧϻ ʙʏᴘᴧꜱꜱ ᴛʜʀσᴜɢʜ ⚡🎶:</b> {streamtype}</i></blockquote>"""
    
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return

async def clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype):

    if not clone_logger_id:
        print("[ERROR] clone_logger_id is missing!")
        return

    logger_text = f"""<blockquote><i>
<b><u>{bot_mention} ηєᴡ ꜱᴛʀєᴧϻ ʀєQᴜєꜱᴛ ɪᴅєηᴛɪꜰɪєᴅ 🚀🎶</u></b>

<b>ɢʀσᴜᴘ ᴜηɪQᴜє ɪᴅ 🆔✨ :</b> <code>{message.chat.id}</code>
<b>ɢʀσᴜᴘ ηᴧϻє 👥✨ :</b> {message.chat.title}
<b>ɢʀσᴜᴘ ᴜꜱєʀηᴧϻє 🌐✨:</b> @{message.chat.username}

<b>ᴜꜱєʀ ɪᴅ 🆔✨ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє 🌿✨ :</b> {message.from_user.mention}
<b>ᴅєᴛєᴄᴛєᴅ ᴜꜱєʀηᴧϻє 🛰️✨ :</b> @{message.from_user.username}

<b>ꜱєᴧʀᴄʜ 🔎✨:</b> {message.text.split(None, 1)[1]}
<b>ꜱᴛʀєᴧϻ ʙʏᴘᴧꜱꜱ ᴛʜʀσᴜɢʜ ⚡🎶:</b> {streamtype}</i></blockquote>"""
    
    if message.chat.id != clone_logger_id:
        try:
            await client.send_message(
                chat_id=int(clone_logger_id),
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"[ERROR] Clone Bot Log Failed ({bot_mention}): {e}")
