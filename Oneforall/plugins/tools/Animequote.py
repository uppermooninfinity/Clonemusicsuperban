import json
import random
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Oneforall import app

# ───────── QUOTES IMAGES ─────────
QUOTES_IMG = [
    "https://i.imgur.com/Iub4RYj.jpg",
    "https://i.imgur.com/uvNMdIl.jpg",
    "https://i.imgur.com/YOBOntg.jpg",
    "https://i.imgur.com/fFpO2ZQ.jpg",
    "https://i.imgur.com/f0xZceK.jpg",
    "https://i.imgur.com/RlVcCip.jpg",
    "https://i.imgur.com/CjpqLRF.jpg",
    "https://i.imgur.com/8BHZDk6.jpg",
    "https://i.imgur.com/8bHeMgy.jpg",
    "https://i.imgur.com/5K3lMvr.jpg",
    "https://i.imgur.com/NTzw4RN.jpg",
    "https://i.imgur.com/wJxryAn.jpg",
    "https://i.imgur.com/9L0DWzC.jpg",
    "https://i.imgur.com/sBe8TTs.jpg",
    "https://i.imgur.com/1Au8gdf.jpg",
    "https://i.imgur.com/28hFQeU.jpg",
    "https://i.imgur.com/Qvc03JY.jpg",
    "https://i.imgur.com/gSX6Xlf.jpg",
    "https://i.imgur.com/iP26Hwa.jpg",
    "https://i.imgur.com/uSsJoX8.jpg",
]

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

# ───────── FETCH RANDOM QUOTE ─────────
def anime_quote():
    try:
        response = requests.get("https://animechan.vercel.app/api/random").json()
        return response["quote"], response["character"], response["anime"]
    except Exception:
        return "❝Error fetching quote❞", "Unknown", "Unknown"

# ───────── COMMAND: /quote ─────────
@app.on_message(filters.command("quote") & filters.group)
async def quotes(client, message: Message):
    quote, character, anime = anime_quote()
    msg_text = f"<i>❝{quote}❞</i>\n\n<b>{to_small_caps(character)} from {to_small_caps(anime)}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="ᴄʜᴀɴɢᴇ 🔁", callback_data="change_quote")]]
    )
    await message.reply_text(msg_text, reply_markup=keyboard)

# ───────── INLINE BUTTON CALLBACK ─────────
@app.on_callback_query(filters.regex("change_quote"))
async def change_quote(client, callback):
    quote, character, anime = anime_quote()
    msg_text = f"<i>❝{quote}❞</i>\n\n<b>{to_small_caps(character)} from {to_small_caps(anime)}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="ᴄʜᴀɴɢᴇ 🔁", callback_data="change_quote")]]
    )
    await callback.message.edit_text(msg_text, reply_markup=keyboard)
    await callback.answer()

# ───────── COMMAND: /animequotes (random anime pics) ─────────
@app.on_message(filters.command("animequotes") & filters.group)
async def animequotes(client, message: Message):
    img_url = random.choice(QUOTES_IMG)
    await message.reply_photo(img_url, caption=f"ᴄʜᴏsᴇɴ ʙʏ {to_small_caps(message.from_user.first_name)}")
