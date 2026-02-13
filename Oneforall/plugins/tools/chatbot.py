import os
import aiohttp
import asyncio
from logging import getLogger
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Oneforall import app

LOGGER = getLogger(__name__)

DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")

# ───────── STATE ─────────
chatbot_status = {}  # chat_id -> bool
TRIGGER_WORDS = ["hi", "hello", "kaise ho", "how are you", "roshni"]

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

# ───────── COMMAND: TOGGLE CHATBOT ─────────
@app.on_message(filters.command("chatbot") & filters.group)
async def chatbot_toggle(_, message: Message):
    chat_id = message.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Enable", callback_data=f"chatbot_enable:{chat_id}"),
                InlineKeyboardButton("❌ Disable", callback_data=f"chatbot_disable:{chat_id}")
            ]
        ]
    )
    status = chatbot_status.get(chat_id, False)
    await message.reply(
        f"🤖 <b>ChatBot Status:</b> <b>{to_small_caps(str(status))}</b>",
        reply_markup=keyboard
    )

# ───────── CALLBACK HANDLER ─────────
@app.on_callback_query()
async def chatbot_callback(_, callback: CallbackQuery):
    data = callback.data
    chat_id = int(data.split(":")[1])
    if data.startswith("chatbot_enable"):
        chatbot_status[chat_id] = True
        await callback.answer("✅ Chatbot Enabled")
        await callback.message.edit(f"🤖 <b>ChatBot is now ON</b>")
    elif data.startswith("chatbot_disable"):
        chatbot_status[chat_id] = False
        await callback.answer("❌ Chatbot Disabled")
        await callback.message.edit(f"🤖 <b>ChatBot is now OFF</b>")

# ───────── CHATBOT RESPONSE ─────────
@app.on_message(filters.group & filters.text)
async def chatbot_response(_, message: Message):
    chat_id = message.chat.id
    if not chatbot_status.get(chat_id, False):
        return
    if message.from_user.is_bot:
        return

    msg_text = message.text.lower()
    if not any(word in msg_text for word in TRIGGER_WORDS):
        return

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}"}
            payload = {"message": message.text}
            async with session.post("https://api.deepseek.ai/chat", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data.get("reply", "🤖 Sorry, I couldn't generate a reply.")
                    await message.reply(reply)
                else:
                    LOGGER.error(f"ChatBot API Error: {resp.status}")
    except Exception as e:
        LOGGER.error(f"ChatBot Error: {e}")
