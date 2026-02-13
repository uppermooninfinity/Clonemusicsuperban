import glob
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from Oneforall import telethn, BOT_USERNAME, OWNER_ID, BOT_NAME, SUPPORT_CHAT
from Oneforall.modules.nightmode import button_row

# ───────── LOGO LINKS ─────────
LOGO_LINKS = [
    "https://telegra.ph/file/d1838efdafce9fe611d0c.jpg",
    "https://telegra.ph/file/c1ff2d5ec5e1b5bd1b200.jpg",
    "https://telegra.ph/file/08c5fbe14cc4b13d1de05.jpg",
    "https://telegra.ph/file/66614a049d74fe2a220dc.jpg",
    "https://telegra.ph/file/9cc1e4b24bfa13873bd66.jpg",
    # ... keep all other links here ...
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

# ───────── COMMAND: /logo ─────────
@Client.on_message(filters.command("logo") & filters.group)
async def create_logo(client: Client, message: Message):
    text = message.text.split(maxsplit=1)
    if len(text) < 2 or not text[1]:
        await message.reply(
            "`ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟᴏɢᴏ!\nExample: /logo (text you want on the image)`"
        )
        return

    text_to_write = text[1]
    loading_msg = await message.reply("**ᴄʀᴇᴀᴛɪɴɢ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**")

    try:
        # Pick random background and font
        rand_bg = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(rand_bg).content))
        draw = ImageDraw.Draw(img)
        fonts = glob.glob("./Oneforall/resources/fonts/*")
        font_path = random.choice(fonts)
        font = ImageFont.truetype(font_path, 120)

        # Calculate position
        bbox = draw.textbbox((0, 0), text_to_write, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        h += int(h * 0.21)
        x = (img.width - w) / 2
        y = (img.height - h) / 2

        # Draw text with stroke
        draw.text((x, y), text_to_write, font=font, fill="white", stroke_width=1, stroke_fill="black")

        # Save and send
        fname = "roshnilogos.png"
        img.save(fname, "PNG")
        await telethn.send_file(
            chat_id=message.chat.id,
            file=fname,
            caption=f"""━━━━━━━{BOT_NAME}━━━━━━━

☘️ ʟᴏɢᴏ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ☘️
◈──────────────◈
🔥 ᴄʀᴇᴀᴛᴇᴅ ʙʏ : @{BOT_USERNAME}
━━━━━━━{BOT_NAME}━━━━━━━""",
            buttons=button_row
        )
        await loading_msg.delete()
        os.remove(fname)
    except Exception as e:
        await message.reply(f"ᴇʀʀᴏʀ: {e}\nReport to @{SUPPORT_CHAT}")

# ───────── MODULE INFO ─────────
__mod_name__ = "Lᴏɢᴏ"

__help__ = f"""
@{BOT_USERNAME} ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ʙᴇᴀᴜᴛɪғᴜʟ ʟᴏɢᴏs.

❍ /logo <Text> : ᴄʀᴇᴀᴛᴇ ᴀ ʟᴏɢᴏ ᴏғ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ʙᴀᴄᴋɢʀᴏᴜɴᴅ.
"""
