from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config

from ..logging import LOGGER


class Hotty(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="Oneforall",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_photo(
                    config.LOGGER_ID,
                    photo=config.START_IMG_URL,
                text=f"<u><b>📢 ʙσᴛ σηʟɪηє 🟢✨\n\n»{self.mention} ʙσᴛ ꜱᴛᴧʀᴛєᴅ ꜱᴜᴄᴄєꜱꜱꜰᴜʟʟʏ 🚀✨ :</b><u>\n\n♡ ᴘʏʀσɢʀᴧϻ ᴠєʀꜱɪση ⚙️ : v2.0.107\n♡ ᴘʏ-ᴛɢᴄᴧʟʟꜱ 🎙️ : 1.2.9\n\n💽ʙσᴛ ꜱᴜᴅσєʀꜱ ᴀηᴅ ϻᴧηᴧɢєϻєηᴛ ᴛєᴧϻ ᴀʀє ʀєqᴜєꜱᴛєᴅ ᴛσ ϻσηɪᴛσʀ ᴛʜє ᴅɪꜱᴋ ꜱᴘᴧᴄє ᴀηᴅ ʀᴧϻ σꜰ ᴠϻ єηɢɪηє ",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )

        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
