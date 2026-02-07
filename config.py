import os
import re
from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from pyrogram import filters

# ===== BASIC CONFIG (REHNE DO) =====

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")

BOT_TOKEN = getenv("BOT_TOKEN", "")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
GIT_TOKEN = getenv("GIT_TOKEN", None)

MONGO_DB_URI = getenv(
    "MONGO_DB_URI",
    ""
)

MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "")
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 100000))
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/izarjuna1/roshu",
)
# ===== LOGGER (REHNE DO) =====

LOGGER_ID = int(getenv("LOGGER_ID", ""))
GBAN_LOG_CHAT = int(getenv("GBAN_LOG_CHAT", ""))

OWNER_ID = getenv("OWNER_ID", "")
SUDO_USERS = getenv("SUDO_USERS", "")

# ===== HEROKU (AUTO WORK) =====

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# superban section 

SUPERBAN_CHAT_ID = -1003228624224
STORAGE_CHANNEL_ID = -1003132769250
AUTHORS = [7651303468]

#--------------------------------
STRING_SESSION1= ""
STRING_SESSION2 = ""
STRING_SESSION3 = ""
Mustjoin = "dark_musictm"

#--------------------------------
SUPERBAN_REQUEST_TEMPLATE = """ᴀᴘᴘʀᴏᴠᴇ sᴜᴘᴇʀʙᴀɴ ꜰᴏʀ ᴜꜱᴇʀ :
{user_first}
ᴜꜱᴇʀ ɪᴅ : {user_id}

ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɪᴅ : {chat_id}
ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɴᴀᴍᴇ : {chat_name}

ʀᴇᴀꜱᴏɴ : {reason}
ʀᴇQᴜᴇꜱᴛ ʙʏ : {request_by}

ᴅᴀᴛᴇ & ᴛɪᴍᴇ : {ind_time}
ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERBAN_REQUEST_RESPONSE = """ʏᴏᴜʀ sᴜᴘᴇʀʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴅᴇᴅ ᴛᴏ ᴛᴇᴀᴍ

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ʀᴇQᴜᴇꜱᴛ ʙʏ : {request_by}

ʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄʜᴇᴄᴋᴇᴅ ᴀɴᴅ ɪꜰ ɪᴛ'ꜱ ɢᴇɴᴜɪɴ ᴛʜᴇɴ ʙᴇ ꜱᴜʀᴇ ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴘᴘʀᴏᴠᴇᴅ.
ᴛʜᴀɴᴋꜜs ꜰᴏʀ ʏᴏᴜʀ sᴜᴘᴇʀʙᴀɴ ʀᴇQᴜᴇꜱᴛ

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @snowy_hometown
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERBAN_APPROVED_TEMPLATE = """ʏᴏᴜʀ sᴜᴘᴇʀʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ, ɴᴏᴡ ꜱᴛᴀʀᴛɪɴɢ sᴜᴘᴇʀʙᴀɴ.....

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERBAN_DECLINED_TEMPLATE = """ʏᴏᴜʀ sᴜᴘᴇʀʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ᴅᴇᴄʟɪɴᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERBAN_COMPLETE_TEMPLATE = """sᴜᴘᴇʀʙᴀɴ ɪꜱ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.

ᴜꜱᴇʀ : {user_first}
ᴜꜱᴇʀ ɪᴅ : {user_id}

ʀᴇᴀꜱᴏɴ : {reason}
ᴛᴏᴛᴀʟ ʙᴀɴ ɪɴ ꜰᴇᴅꜱ : {fed_count}
ɢʙᴀɴ ɪɴ : {extra_bans}

ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴛɪᴍᴇ ᴛᴀᴋᴇɴ : {time_taken}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @snowy_hometown
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

#--------------------------------
SUPERUNBAN_REQUEST_TEMPLATE = """ᴀᴘᴘʀᴏᴠᴇ sᴜᴘᴇʀᴜɴʙᴀɴ ꜰᴏʀ ᴜꜱᴇʀ :
{user_first}
ᴜꜱᴇʀ ɪᴅ : {user_id}

ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɪᴅ : {chat_id}
ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɴᴀᴍᴇ : {chat_name}

ʀᴇᴀꜱᴏɴ : {reason}
ʀᴇQᴜᴇꜱᴛ ʙʏ : {request_by}

ᴅᴀᴛᴇ & ᴛɪᴍᴇ : {ind_time}
ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERUNBAN_REQUEST_RESPONSE = """ʏᴏᴜʀ sᴜᴘᴇʀᴜɴʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴅᴇᴅ ᴛᴏ ᴛᴇᴀᴍ

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀᴜɴʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ʀᴇQᴜᴇꜱᴛ ʙʏ : {request_by}

ʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄʜᴇᴄᴋᴇᴅ ᴀɴᴅ ɪꜰ ɪᴛ'ꜱ ɢᴇɴᴜɪɴ ᴛʜᴇɴ ʙᴇ ꜱᴜʀᴇ ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴘᴘʀᴏᴠᴇᴅ.
ᴛʜᴀɴᴋꜜs ꜰᴏʀ ʏᴏᴜʀ sᴜᴘᴇʀᴜɴʙᴀɴ ʀᴇQᴜᴇꜱᴛ

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @snowy_hometown
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERUNBAN_APPROVED_TEMPLATE = """ʏᴏᴜʀ sᴜᴘᴇʀᴜɴʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ, ɴᴏᴡ ꜱᴛᴀʀᴛɪɴɢ sᴜᴘᴇʀᴜɴʙᴀɴ.....

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀᴜɴʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERUNBAN_DECLINED_TEMPLATE = """ʏᴏᴜʀ sᴜᴘᴇʀᴜɴʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ

ʀᴇQᴜᴇꜱᴛ ᴛᴏ sᴜᴘᴇʀᴜɴʙᴀɴ
ᴜꜱᴇʀ : {user_first}

ʀᴇᴀꜱᴏɴ : {reason}
ᴅᴇᴄʟɪɴᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""

SUPERUNBAN_COMPLETE_TEMPLATE = """sᴜᴘᴇʀᴜɴʙᴀɴ ɪꜱ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.

ᴜꜱᴇʀ : {user_first}
ᴜꜱᴇʀ ɪᴅ : {user_id}

ʀᴇᴀꜱᴏɴ : {reason}
ᴛᴏᴛᴀʟ ᴜɴʙᴀɴ ɪɴ ꜰᴇᴅꜱ : {fed_count}
ɢᴜɴʙᴀɴ ɪɴ : {extra_bans}

ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}
ᴛɪᴍᴇ ᴛᴀᴋᴇɴ : {time_taken}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @snowy_hometown
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @dark_musictm"""
#--------------------------------
CLIENT_CHAT_DATA = [
    {
        "STRING_SESSION1": SESSION_STRING1,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 1111-aaaa",
            "/fban {user_id} {reason} \n\nApproved by {approver} \nTime: {utc_time}"
        ]
    },
    {
        "STRING_SESSION2": SESSION_STRING2,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 2222-bbbb",
            "/fban {user_id} Reason: {reason} \n\nDone by {approver}"
        ]
    },
    {
        "STRING_SESSION3": SESSION_STRING3,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 3333-cccc",
            "Ban user {user_id} - Reason: {reason} - By: {approver}"
        ]
    },
]

#--------------------------------
CLIENT_CHAT_DATA2 = [
    {
        "STRING_SESSION1": String_client_1,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 1111-aaaa",
            "/fban {user_id} {reason} \n\nApproved by {approver} \nTime: {utc_time}"
        ]
    },
    {
        "STRING_SESSION2": String_client_2,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 2222-bbbb",
            "/fban {user_id} Reason: {reason} \n\nDone by {approver}"
        ]
    },
    {
        "STRING_SESSION3": String_client_3,
        "chat_ids": [-1003228624224],
        "messages": [
            "/Joinfed 3333-cccc",
            "Ban user {user_id} - Reason: {reason} - By: {approver}"
        ]
    },
]

#--------------------------------
# ===== SUPPORT =====

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dark_musictm")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/snowy_hometown")

# ===== IMAGES (REHNE DO BHAI 😄) =====

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/r2toj2.jpg")
PING_IMG_URL = START_IMG_URL
PLAYLIST_IMG_URL = START_IMG_URL
STATS_IMG_URL = START_IMG_URL
TELEGRAM_AUDIO_URL = START_IMG_URL
TELEGRAM_VIDEO_URL = START_IMG_URL
STREAM_IMG_URL = START_IMG_URL
SOUNCLOUD_IMG_URL = START_IMG_URL
YOUTUBE_IMG_URL = START_IMG_URL
SPOTIFY_ARTIST_IMG_URL = START_IMG_URL
SPOTIFY_ALBUM_IMG_URL = START_IMG_URL
SPOTIFY_PLAYLIST_IMG_URL = START_IMG_URL

# ===== FUNCTIONS =====

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ===== VALIDATION =====

if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("SUPPORT_CHANNEL must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("SUPPORT_CHAT must start with https://")

# ===== OTHERS =====

BANNED_USERS = filters.user()
TEMP_DB_FOLDER = "tempdb"
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
