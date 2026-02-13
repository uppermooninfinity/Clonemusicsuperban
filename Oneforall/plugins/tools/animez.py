import glob
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from Oneforall import BOT_USERNAME, OWNER_ID, BOT_NAME, SUPPORT_CHAT
from Oneforall import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_row = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("˹ sᴜᴘᴘᴏʀᴛ ˼", url=f"https://t.me/snowy_hometown")],
        [InlineKeyboardButton("˹ ᴏᴡɴᴇʀ ˼", url=f"https://t.me/snowy_hometown")]
    ]
)

# ───────── LOGO LINKS ─────────
LOGO_LINKS = [  
    "https://telegra.ph/file/fc7fbefe92599bd79d038.jpg",
    "https://telegra.ph/file/b88d6e78e206eb73e2e54.jpg",
    "https://telegra.ph/file/48f8c62829953e82441e8.jpg",
    "https://telegra.ph/file/56f7b34cae98a491e2b35.jpg",
    "https://telegra.ph/file/9c23b4302926d40c46e12.jpg",
    "https://telegra.ph/file/9bf850ea98a2b252ff233.jpg",
    "https://telegra.ph/file/e764f0b3e2ecc56167803.jpg",
    "https://telegra.ph/file/289f9cebe37f31a943f98.jpg",
    "https://telegra.ph/file/0c647be0f5a48d576d692.jpg",
    "https://telegra.ph/file/41c5b44c4f5978828b5b5.jpg",
    "https://telegra.ph/file/9cdce279bdf240a933c14.jpg",
    "https://telegra.ph/file/f20424687f94e9c285133.jpg",
    "https://telegra.ph/file/e7858eb025e1ddb2f6267.jpg",
    "https://telegra.ph/file/3e984aa5ab96df166f2a4.jpg",
    "https://telegra.ph/file/e43e28aa952eaee6a5315.jpg",
    "https://telegra.ph/file/6d222dcaf9ba1072c6062.jpg",
    "https://telegra.ph/file/21e696bbefcfe39c6e74e.jpg",
    "https://telegra.ph/file/64ec61e41da3d4aded33d.jpg",
    "https://telegra.ph/file/5b1d8766504ff75c1bd1f.jpg",
    "https://telegra.ph/file/731879a344b3b49fe51bd.jpg",
    "https://telegra.ph/file/6221afc84b357ed0d1fc5.jpg",
    "https://telegra.ph/file/499bb1117771d8c020038.jpg",
    "https://telegra.ph/file/2690d73bc32cfdb986629.jpg",
    "https://telegra.ph/file/21255de971701b9df0902.jpg",
    "https://telegra.ph/file/434a35e7fe5e2c000c598.jpg",
    "https://telegra.ph/file/22a5d3621aba0b370d0b6.png",
    "https://telegra.ph/file/ae31845d1df2c4a84915b.png",
    "https://telegra.ph/file/ae2b809c8d11e7fa4121d.png",
    "https://telegra.ph/file/ccb7f3113994d5d2b26f6.png",
    "https://telegra.ph/file/5e53f0257ff12a7b0737a.png",
    "https://telegra.ph/file/a613600a9f9f8ee29f0f7.jpg",
    "https://telegra.ph/file/129c14fada1a8c0b151f5.jpg",
    "https://telegra.ph/file/c7552ed4246ccd8efd301.jpg",
    "https://telegra.ph/file/e794f772243d46467bcce.jpg",
    "https://telegra.ph/file/b6c43b9bd63f5f764d60b.jpg",
    "https://telegra.ph/file/11585459a3950de7f307c.png",
    "https://telegra.ph/file/37cde08802c3cea25a03f.jpg",
    "https://telegra.ph/file/d8d2db623223dee65963e.png",
    "https://telegra.ph/file/b7229017ffee2d814c646.jpg",
    "https://telegra.ph/file/65630efca60bfbdf84bc9.jpg",
    "https://telegra.ph/file/b8ce571c2f66a7c7070e5.jpg",
    "https://telegra.ph/file/a39f63f61f143ec00f19f.jpg",
    "https://telegra.ph/file/f7d946d8caaa21bf96dbf.jpg",
    "https://telegra.ph/file/9e4bef8ae0725d6b62108.png",
    "https://telegra.ph/file/3550089b22f3c8f506226.jpg",
    "https://telegra.ph/file/4275a4d4d6d433406b5fa.jpg",
    "https://telegra.ph/file/c476583ff55e1947461ad.jpg",
    "https://telegra.ph/file/87d2e5c0170ead00a2bc2.jpg",
    "https://telegra.ph/file/5027dd7379cc432c06e73.jpg",
    "https://telegra.ph/file/9e447fcaf3c66ddefb603.jpg",
    "https://telegra.ph/file/e5375f8233bea4f74b0f8.jpg",
    "https://telegra.ph/file/a1297510a64733cc5845f.jpg",
    "https://telegra.ph/file/ff04b594b699ce72316d7.jpg",
    "https://telegra.ph/file/093836a52cb166f161819.jpg",
    "https://telegra.ph/file/1e64bae43ca10d628ff6d.jpg",
    "https://telegra.ph/file/678ff9bb3405158a9155e.jpg",
    "https://telegra.ph/file/ab332ced3f63b96c375c5.jpg",
    "https://telegra.ph/file/a736d6cac93294c323303.jpg",
    "https://telegra.ph/file/dce8565bf7742f3d7122b.jpg",
    "https://telegra.ph/file/3f97672eb7b50426d15ff.jpg",
    "https://telegra.ph/file/19c6250369f8588a169c7.jpg",
    "https://telegra.ph/file/13d53b03a48448156564c.jpg",
    "https://telegra.ph/file/d21ff0d35553890e8cf34.jpg",
    "https://telegra.ph/file/a5e4cb43178642ba3709d.jpg",
    "https://telegra.ph/file/ecf108d25a6f5f56f91f4.jpg",
    "https://telegra.ph/file/8bd2b561b4c1f7164f934.png",
    "https://telegra.ph/file/7717658e6930c8196a904.jpg",
    "https://telegra.ph/file/dc85d43c4fc5062de7274.jpg",
    "https://telegra.ph/file/ff05c19f228ab2ed3d39d.jpg",
    "https://telegra.ph/file/ff05c19f228ab2ed3d39d.jpg",
    "https://telegra.ph/file/0d686bfffcb92a2fbdb0f.jpg",
    "https://telegra.ph/file/0d686bfffcb92a2fbdb0f.jpg",
    "https://telegra.ph/file/cdc66f16fbfb75971df2f.jpg",
    "https://telegra.ph/file/5c575892b9f9534fd4f31.jpg",
    "https://telegra.ph/file/78ffc400d4f3236b00e6b.jpg",
    "https://telegra.ph/file/89d32e5bbf084a376c803.jpg",
    "https://telegra.ph/file/b5d7dbcdce241013a061b.jpg",
    "https://telegra.ph/file/c1d228bc1859213d258d7.jpg",
    "https://telegra.ph/file/c6b0720b9f765809ea20a.jpg",
    "https://telegra.ph/file/df7e648f2e68ff8e1a1e6.jpg",
    "https://telegra.ph/file/5148f764cbc4700519909.jpg",
    "https://telegra.ph/file/479e7f51c682dcd1f013f.jpg",
    "https://telegra.ph/file/54a9eb0afe7a0f9c7c2f3.jpg",
    "https://telegra.ph/file/73c52ee54567a61dac47a.jpg",
    "https://telegra.ph/file/1427dbba81bd21b1bfc56.jpg",
    "https://telegra.ph/file/1427dbba81bd21b1bfc56.jpg",
    "https://telegra.ph/file/b0816374b470a5f9c66a6.jpg",
    "https://telegra.ph/file/e10840ec9bea9bbfaff0e.jpg",
    "https://telegra.ph/file/5935275d3ee09bc5a47b8.png",
    "https://telegra.ph/file/c27e64f1e8ece187c8161.jpg",
    "https://telegra.ph/file/055e9af8500ab92755358.jpg",
    "https://telegra.ph/file/f18f71167f9318ea28571.jpg",
    "https://telegra.ph/file/e2e26f252a5e25a1563c5.jpg",
    "https://telegra.ph/file/47ccb13820d6fc54d872b.jpg",
    "https://telegra.ph/file/f2ddccd28ceaeae90b2a3.jpg",
    "https://telegra.ph/file/951c872f7f8d551995652.jpg",
    "https://telegra.ph/file/8e8842f9fe207b8abd951.jpg",
    "https://telegra.ph/file/8a14ecd2347ef88e81201.jpg",
    "https://telegra.ph/file/b3869374ce0af9f26f92a.jpg",
    "https://telegra.ph/file/8e17f8d3633a5696a1ccf.jpg",
    "https://telegra.ph/file/b29d8956ae249773b0ec7.png",
    "https://telegra.ph/file/d0eebe724b67d2ef7647e.jpg",
    "https://telegra.ph/file/5780b3273162d2b9ba9ec.jpg",
    "https://telegra.ph/file/e2d56d5dbb108ba7af20c.jpg",
    "https://telegra.ph/file/1a4f50dd1e4ec9f04bfa1.jpg",
    "https://telegra.ph/file/99b56305fa9c50767f574.jpg",
    "https://telegra.ph/file/0859e0104c671bc9b6b7d.jpg",
    "https://telegra.ph/file/b3af2980caf7040702171.jpg",
    "https://telegra.ph/file/14be160df3b84c59e268e.jpg",
    "https://telegra.ph/file/b958155e1e8e9ab9a0416.jpg",
    "https://telegra.ph/file/24fff051c39b815e5078a.jpg",
    "https://telegra.ph/file/258c02c002e89287d5d9b.jpg",
    "https://telegra.ph/file/d2abc99773a9d4954c2ba.jpg",
    "https://telegra.ph/file/9849b3940f063b065f4e3.jpg",
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
        await app.send_photo(
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
