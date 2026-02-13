import json
import random
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Oneforall import app

# ───────── QUOTES IMAGES ─────────
QUOTES_IMG = [
    "https://graph.org/file/42304defef005c8769ec8-1db22d423d63bfa361.jpg",
    "https://graph.org/file/0b190f1ff31b063b701e6-005e2b13b1fe387308.jpg",
    "https://graph.org/file/b92285ff7a0e976d346fd-112467a5677580da52.jpg",
    "https://graph.org/file/48b35b306853f131a716c-c2f0e4b0718f30afe3.jpg",
    "https://graph.org/file/84aa9a94de7287d1573b1-598d0e289e60afd92f.jpg",
    "https://graph.org/file/1bd47c3763b1c004ddc10-cb0757be9d313b635b.jpg",
    "https://graph.org/file/225096f95b937a035389c-b74b4c798d728139cf.jpg",
    "https://graph.org/file/37a6ad6b1fe9d63095d29-6dbe88235da95d9f4e.jpg",
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
