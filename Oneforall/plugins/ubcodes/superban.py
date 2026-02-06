import asyncio
import base64
import logging
import re
from datetime import datetime
from shlex import split as shlex_split

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ParseMode, ChatType, ChatMemberStatus
from pytz import timezone

from config import (
    SUPERBAN_REQUEST_TEMPLATE,
    SUPERBAN_REQUEST_RESPONSE,
    SUPERBAN_APPROVED_TEMPLATE,
    SUPERBAN_DECLINED_TEMPLATE,
    SUPERBAN_COMPLETE_TEMPLATE,
    CLIENT_CHAT_DATA,
    SUPERBAN_CHAT_ID,
    STORAGE_CHANNEL_ID,
    AUTHORS
)

from Superban import app
from Superban.core.mongo import group_log_db
import Superban.core.userbot as userbot_module
from Superban.core.readable_time import get_readable_time
from Superban.core.chat_tracker import verify_all_groups_from_db

reason_storage = {}
next_reason_id = 1
superban_request_messages = {}

def store_reason(reason):
    global next_reason_id
    reason_id = next_reason_id
    reason_storage[reason_id] = reason
    next_reason_id += 1
    return reason_id

async def get_user_id(user_query):
    try:
        if user_query.isdigit():
            return int(user_query)
        user_query = user_query.lstrip('@')
        user = await app.get_users(user_query)
        return user.id
    except Exception as e:
        logging.error(f"Error fetching user ID for {user_query}: {e}")
        return None

async def send_request_message(user, reason, action, message):
    reason_id = store_reason(reason) if reason else None
    chat_name = message.chat.title if message.chat.title else "Private Chat"
    chat_id = message.chat.id
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    encoded_reason = base64.b64encode(str(reason_id).encode()).decode() if reason_id else ""

    return await app.send_message(
        SUPERBAN_CHAT_ID,
        SUPERBAN_REQUEST_TEMPLATE.format(
            user_first=user.first_name,
            user_id=user.id,
            chat_id=chat_id,
            chat_name=chat_name,
            reason=reason if reason else "No reason provided",
            request_by=message.from_user.first_name,
            ind_time=ind_time,
            utc_time=utc_time,
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✯ ᴀᴘᴘʀᴏᴠᴇ ✯", callback_data=f"{action}_approve_{user.id}_{encoded_reason}")],
            [InlineKeyboardButton("✯ ᴅᴇᴄʟɪɴᴇ ✯", callback_data=f"{action}_decline_{user.id}_{encoded_reason}")]
        ])
    )

@Client.on_message(filters.command(["superban"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def super_ban(_, message):
    reason = None
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            args = shlex_split(message.text)
            reason = " ".join(args[1:]) if len(args) > 1 else None
        except Exception:
            reason = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None
    else:
        try:
            args = shlex_split(message.text)
            if len(args) > 1:
                user_query = args[1]
                user_id = await get_user_id(user_query)
                reason = " ".join(args[2:]) if len(args) > 2 else None
        except Exception:
            msg_parts = message.text.split(None, 1)
            if len(msg_parts) > 1:
                user_query = msg_parts[1].split()[0]
                user_id = await get_user_id(user_query)
                reason = " ".join(msg_parts[1].split()[1:]) if len(msg_parts[1].split()) > 1 else None

    if user_id is None:
        await message.reply("Please specify a user ID, username, or reply to a message.")
        return

    try:
        user = await app.get_users(user_id)
    except Exception as e:
        logging.error(f"Error fetching user with ID {user_id}: {e}")
        await message.reply("User not found or inaccessible.")
        return

    await send_request_message(user, reason, "Super_Ban", message)
    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    superban_msg = await message.edit_text(
        SUPERBAN_REQUEST_RESPONSE.format(
            user_first=user.first_name,
            reason=reason if reason else "No reason provided",
            request_by=message.from_user.first_name,
            utc_time=utc_time,
        )
    )
    superban_request_messages[user.id] = superban_msg

    try:
        await superban_msg.pin(disable_notification=True)
    except Exception as e:
        logging.warning(f"Could not pin the message: {e}")

@app.on_callback_query(filters.regex(r'^Super_Ban_(approve|decline)_(\d+)_(.+)$'))
async def handle_super_ban_callback(client: Client, query: CallbackQuery):
    try:
        match = re.match(r'^Super_Ban_(approve|decline)_(\d+)_(.+)$', query.data)
        if not match:
            raise ValueError("Invalid callback data format")
        action, user_id_str, encoded_reason = match.groups()
        user_id = int(user_id_str)
        reason_id = base64.b64decode(encoded_reason).decode()
        reason = reason_storage.get(int(reason_id), "No reason provided")
        user = await app.get_users(user_id)
    except Exception as e:
        logging.error(f"Callback data parsing error: {e}")
        await query.answer("Error occurred while processing.", show_alert=True)
        return

    if query.from_user.id not in AUTHORS:
        await query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴜᴛʜᴏʀ", show_alert=True)
        return

    approval_author = query.from_user.first_name

    try:
        if action == "approve":
            await query.answer("ꜱᴜᴘᴇʀʙᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ.", show_alert=True)

            if user.id in superban_request_messages:
                try:
                    await superban_request_messages[user.id].edit(
                        SUPERBAN_APPROVED_TEMPLATE.format(
                            user_first=user.first_name,
                            reason=reason,
                            approval_author=approval_author,
                            utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        )
                    )
                except Exception as e:
                    logging.warning(f"Failed to edit original approval message: {e}")

            await query.message.edit(
                SUPERBAN_APPROVED_TEMPLATE.format(
                    user_first=user.first_name,
                    reason=reason,
                    approval_author=approval_author,
                    utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                )
            )

            try:
                await query.message.pin(disable_notification=True)
            except Exception:
                pass

            note = await app.send_message(SUPERBAN_CHAT_ID, f"ꜱᴜᴘᴇʀʙᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ {approval_author}.")
            await asyncio.sleep(10)
            await note.delete()

            start_time = datetime.utcnow()
            fed_count, extra_bans = await super_ban_action(user_id, query.message, approval_author, reason)
            end_time = datetime.utcnow()
            readable_time = get_readable_time(end_time - start_time)

            complete_text = SUPERBAN_COMPLETE_TEMPLATE.format(
                user_first=user.first_name,
                user_id=user.id,
                reason=reason,
                fed_count=fed_count,
                extra_bans=extra_bans,
                approval_author=approval_author,
                utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                time_taken=readable_time,
            )

            try:
                await query.message.edit(complete_text)

                if user.id in superban_request_messages:
                    try:
                        await superban_request_messages[user.id].edit(complete_text)
                    except Exception as e:
                        logging.warning(f"Failed to edit superban_request_messages to complete: {e}")
            except Exception as e:
                logging.warning(f"Failed to edit message to complete: {e}")

        elif action == "decline":
            await query.answer("ꜱᴜᴘᴇʀʙᴀɴ ᴅᴇᴄʟɪɴᴇᴅ.", show_alert=True)

            if user.id in superban_request_messages:
                try:
                    await superban_request_messages[user.id].edit(
                        SUPERBAN_DECLINED_TEMPLATE.format(
                            user_first=user.first_name,
                            reason=reason,
                            approval_author=approval_author,
                            utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        )
                    )
                except Exception as e:
                    logging.warning(f"Failed to edit original decline message: {e}")

            await query.message.edit(
                SUPERBAN_DECLINED_TEMPLATE.format(
                    user_first=user.first_name,
                    reason=reason,
                    approval_author=approval_author,
                    utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                )
            )

            try:
                await query.message.pin(disable_notification=True)
            except Exception:
                pass

            note = await app.send_message(SUPERBAN_CHAT_ID, f"ꜱᴜᴘᴇʀʙᴀɴ ᴅᴇᴄʟɪɴᴇᴅ ʙʏ {approval_author}.")
            await asyncio.sleep(10)
            await query.message.delete()
            await note.delete()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await query.answer("An unexpected error occurred. Please try again.", show_alert=True)

semaphore = asyncio.Semaphore(2)

async def send_message_with_semaphore(client, chat_id, msg):
    async with semaphore:
        try:
            logging.info(f"[SEND] Trying to send to {chat_id}: {msg}")
            await client.send_message(chat_id, msg)
            logging.info(f"[SUCCESS] Sent to {chat_id}")
            return True
        except Exception as e:
            logging.error(f"[ERROR] send_message_with_semaphore to {chat_id}: {e}")
            return False

async def ban_user_from_all_groups_via_userbots(user_id: int) -> int:
    total_banned = 0
    for client in userbot_module.userbot_clients:
        async for dialog in client.get_dialogs():
            chat = dialog.chat
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                try:
                    member = await client.get_chat_member(chat.id, user_id)
                    if member.status == ChatMemberStatus.BANNED:
                        logging.info(f"[SKIP] {user_id} is already banned in {chat.title} ({chat.id}) via {client.name}")
                        continue
                except Exception as e:
                    logging.debug(f"[INFO] Could not get member info in {chat.title}: {e}")
                try:
                    await client.ban_chat_member(chat.id, user_id)
                    logging.info(f"[USERBOT BAN] {user_id} banned in {chat.title} ({chat.id}) via {client.name}")
                    total_banned += 1
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logging.warning(f"[USERBOT FAIL] Could not ban {user_id} from {chat.title}: {e}")
    return total_banned

async def super_ban_action(user_id, message, approval_author, reason):
    try:
        await verify_all_groups_from_db(app)
        user = await app.get_users(user_id)
        banned_chats_set = set()
        start_time = datetime.utcnow()

        verified_chat_ids = {
            doc["_id"] async for doc in group_log_db.find({})
        }

        async def send_custom_messages(client, chat_ids, message_templates, bot_index):
            for chat_id in chat_ids:
                if chat_id not in verified_chat_ids:
                    continue
                try:
                    starter_msg = f"⚠️ Starting Superban on [{user.first_name}](tg://user?id={user.id}) in this chat."
                    await app.send_message(chat_id, starter_msg, parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(2)
                except Exception:
                    pass
                for template in message_templates:
                    try:
                        msg = template.format(
                            user_id=user.id,
                            reason=reason,
                            approver=approval_author,
                            utc_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        )
                        if await send_message_with_semaphore(client, chat_id, msg):
                            banned_chats_set.add(chat_id)
                        await asyncio.sleep(4)
                    except Exception:
                        pass

        await asyncio.gather(*[
            send_custom_messages(
                userbot_module.userbot_clients[i],
                CLIENT_CHAT_DATA[i]["chat_ids"],
                CLIENT_CHAT_DATA[i]["messages"],
                i + 1
            )
            for i in range(len(userbot_module.userbot_clients))
        ])

        end_time = datetime.utcnow()
        readable_time = get_readable_time(end_time - start_time)

        try:
            extra_bans = await ban_user_from_all_groups_via_userbots(user.id)
        except Exception as e:
            logging.error(f"[EXTRA BAN ERROR] Global userbot ban failed: {e}")
            extra_bans = "0"

        if await group_log_db.find_one({"_id": STORAGE_CHANNEL_ID}):
            await app.send_message(
                STORAGE_CHANNEL_ID,
                SUPERBAN_COMPLETE_TEMPLATE.format(
                    user_first=user.first_name,
                    user_id=user.id,
                    reason=reason,
                    fed_count=len(banned_chats_set),
                    extra_bans=extra_bans,
                    approval_author=approval_author,
                    utc_time=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    time_taken=readable_time,
                )
            )

    except Exception as e:
        logging.error(f"Error during superban action: {e}")