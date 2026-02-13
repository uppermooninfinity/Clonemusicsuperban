import re
from pyrogram import filters
from pyrogram.types import Message
from Oneforall import app
from config import OWNER_ID, BIO_LOG_CHANNEL

# Detect links in bio
LINK_REGEX = r"(https?://\S+|t\.me/\S+|@\w+)"
FLAGGED_USERS = set()
WHITELISTED_USERS = set()


# ================= JOIN CHECK ================= #

@app.on_message(filters.new_chat_members)
async def check_bio_on_join(_, message: Message):
    for member in message.new_chat_members:
        if member.is_bot:
            continue

        try:
            full_user = await app.get_users(member.id)
            bio = full_user.bio or ""
        except:
            bio = ""

        if re.search(LINK_REGEX, bio, re.IGNORECASE):
            FLAGGED_USERS.add(member.id)

            # Send log to channel
            await app.send_message(
                BIO_LOG_CHANNEL,
                f"🚨 **Bio Link Detected**\n\n"
                f"👤 User: {member.mention}\n"
                f"🆔 ID: `{member.id}`\n"
                f"💬 Chat: {message.chat.title}\n"
                f"📌 Bio:\n`{bio}`\n\n"
                f"⚠ User flagged for monitoring."
            )


# ================= MESSAGE MONITOR ================= #

@app.on_message(filters.group & filters.text)
async def monitor_flagged_users(_, message: Message):
    user = message.from_user
    if not user:
        return

    if user.id in FLAGGED_USERS and user.id not in WHITELISTED_USERS:
        try:
            deleted_text = message.text
            await message.delete()
        except:
            return

        # Log deleted message
        await app.send_message(
            BIO_LOG_CHANNEL,
            f"🗑 **Message Deleted (Bio Protection)**\n\n"
            f"👤 User: {user.mention}\n"
            f"🆔 ID: `{user.id}`\n"
            f"💬 Chat: {message.chat.title}\n\n"
            f"📨 Deleted Message:\n`{deleted_text}`"
        )


# ================= WHITELIST COMMAND ================= #

@app.on_message(filters.command("whitelist") & filters.group)
async def whitelist_user(_, message: Message):
    user = message.from_user
    if not user:
        return

    member = await app.get_chat_member(message.chat.id, user.id)

    if user.id != OWNER_ID and not member.privileges:
        return await message.reply_text("❌ Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply_text(
            "⚠ Usage:\n`/whitelist @username`\nor\n`/whitelist user_id`",
            parse_mode="markdown"
        )

    target = message.command[1]

    try:
        if target.startswith("@"):
            target_user = await app.get_users(target)
        else:
            target_user = await app.get_users(int(target))
    except:
        return await message.reply_text("❌ User not found.")

    WHITELISTED_USERS.add(target_user.id)
    FLAGGED_USERS.discard(target_user.id)

    await message.reply_text(
        f"✅ {target_user.mention} has been whitelisted."
    )

    # Log whitelist action
    await app.send_message(
        BIO_LOG_CHANNEL,
        f"✅ **User Whitelisted**\n\n"
        f"👤 Target: {target_user.mention}\n"
        f"🆔 ID: `{target_user.id}`\n"
        f"👮 By: {user.mention}\n"
        f"💬 Chat: {message.chat.title}"
    )
