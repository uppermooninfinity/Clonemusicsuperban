import os
import re
from os import getenv
from pyrogram import filters

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# ===== BASIC CONFIG =====

API_ID = int(getenv("API_ID", "12345")) # Default value zaroori hai
API_HASH = getenv("API_HASH", "")

BOT_TOKEN = getenv("BOT_TOKEN", "")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY")
GIT_TOKEN = getenv("GIT_TOKEN", None)

MONGO_DB_URI = getenv("MONGO_DB_URI", "")

CLONE_LOGGER = getenv("CLONE_LOGGER", "-1003748760283")


MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "")
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 100000))
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/uppermooninfinity/clonemusicsuperban",
)

# ===== LOGGER =====

LOGGER_ID = int(getenv("LOGGER_ID", "0"))
GBAN_LOG_CHAT = int(getenv("GBAN_LOG_CHAT", "0"))

OWNER_ID = getenv("OWNER_ID", "")
SUDO_USERS = getenv("SUDO_USERS", "")
BIO_LOG_CHANNEL = getenv("BIO_LOG_CHANNEL", "-1003634796457")
# ===== HEROKU =====

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "6fb7e1766693439b86ec57e3deb3c36f")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "da3f94c6a68d49f6b64a7216ec9eb905"
)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "1000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "1000"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "2000"))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

# ===== SUPERBAN SECTION =====

SUPERBAN_CHAT_ID = -1003228624224
STORAGE_CHANNEL_ID = -1003132769250
AUTHORS = [7651303468]

# SESSION STRINGS
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

Mustjoin = "snowy_hometown"

#--------------------------------
# TEMPLATES (Shortened for view, keep your stylized text)
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
# CLIENT DATA CONFIG (Sahi kiya gaya hai)
CLIENT_CHAT_DATA = [
    {
        "session": STRING1,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 1111-aaaa",
            "/fban {user_id} {reason} \n\nApproved by {approver}"
        ]
    },
    {
        "session": STRING2,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 2222-bbbb",
            "/fban {user_id} Reason: {reason}"
        ]
    },
    {
        "session": STRING3,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 3333-cccc",
            "/fban {user_id} Reason: {reason}"
        ]
    },
    {
        "session": STRING4,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 4444-dddd",
            "/fban {user_id} Reason: {reason}"
        ]
    },
    {
        "session": STRING5,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 5555-eeee",
            "/fban {user_id} Reason: {reason}"
        ]
    },
]

# UNBAN DATA
CLIENT_CHAT_DATA2 = [
    {
        "session": STRING1,
        "chat_ids": [SUPERBAN_CHAT_ID],
        "messages": [
            "/Joinfed 1111-aaaa",
            "/unfban {user_id} \n\nUnbanned by {approver}"
        ]
    }
]

#--------------------------------
# ===== SUPPORT & IMAGES =====

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dark_musictm")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/snowy_hometown")

START_IMG_URL = getenv("START_IMG_URL", "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg")
PING_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
PLAYLIST_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
STATS_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
STREAM_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/cb128c7c5df838c999ede-47c87694df487b317c.jpg"
# ... (Baaki links same rahenge)

#--------------------------------
# ===== FUNCTIONS & VALIDATION =====


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
# ===== GLOBALS =====
BANNED_USERS = filters.user()
TEMP_DB_FOLDER = "tempdb"
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
