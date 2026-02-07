from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="▷", callback_data="resume_cb"),
            InlineKeyboardButton(text="II", callback_data="pause_cb"),
            InlineKeyboardButton(text="‣‣I", callback_data="skip_cb"),
            InlineKeyboardButton(text="▢", callback_data="end_cb"),
        ]
    ]
  [
            InlineKeyboardButton("📥ᴘʀᴏᴍᴏ📥", url="https://t.me/velle_logzz"),
            InlineKeyboardButton("♻️ɢʀᴏᴜᴘ ᴄʜᴀᴛ♻️", url="https://t.me/snowy_hometown"),
        ],
  [
            InlineKeyboardButton("❄️ᴅєᴠєʟσᴘєʀ❄️", url="https://t.me/cyber_github")
  ]

)
close_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="❖ ᴄʟσꜱє ❖", callback_data="close")]]
)
