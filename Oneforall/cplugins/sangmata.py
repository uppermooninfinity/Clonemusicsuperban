from database import DatabaseManager
from typing import List, Dict, Any
from datetime import datetime

class SangmataFeature:
    def __init__(self):
        self.db = DatabaseManager()

    def track_user(self, user_id: int, username: str, first_name: str, last_name: str) -> None:
        self.db.record_user_history(user_id, username, first_name, last_name)

    def get_user_info(self, user_id: int) -> str:
        history = self.db.get_user_history(user_id)

        if not history:
            return "<blockquote expandable>📊 <b>ᴜꜱєʀ ʜɪꜱᴛσʀʏ</b>\n\n❌ ɪᴛ’ꜱ σʙᴠɪσᴜꜱ — ησ ʜɪꜱᴛσʀʏ ꜰσᴜηᴅ ꜰσʀ ᴛʜє ᴜꜱєʀ 📭🔍</blockquote>"

        current = history[-1] if history else None
        changes = len(history)

        message = "<blockquote>📊 <b>ꜱᴧηɢϻᴧᴛᴧ — ᴜꜱєʀ ʜɪꜱᴛσʀʏ ᴛʀᴧᴄᴋєᴅ 📜🔍</b>\n\n"
        message += f"🆔 <b>ᴜꜱєʀ ɪᴅ 🆔🔹:</b> <code>{user_id}</code>\n\n"

        if current:
            message += "📝 <b>ᴄᴜʀʀєηᴛ ɪηꜰσʀϻᴧᴛɪση 📌🔎</b>\n"
            message += f"👤 <b>ꜰɪʀꜱᴛ ηᴧϻє ✨:</b> {current.get('first_name', 'N/A')}\n"
            message += f"👥 <b>ʟᴧꜱᴛ ηᴧϻє 🩷:</b> {current.get('last_name', 'N/A')}\n"
            message += f"🔖 <b>ᴜꜱєʀηᴧϻє 📥:</b> @{current.get('username', 'None')}\n\n"

        message += f"🔄 <b>ᴛσᴛᴧʟ ᴄʜᴧηɢєꜱ 🔄✨:</b> {changes}\n\n"

        message += "📜 <b>ʜɪꜱᴛσʀʏ ʟσɢꜱ 📜✨</b>\n"
        message += "━━━━━━━━━━━━━━━━\n\n"

        for idx, record in enumerate(history, 1):
            recorded_at = record.get('recorded_at', 'Unknown')
            if recorded_at != 'Unknown':
                try:
                    dt = datetime.fromisoformat(recorded_at.replace('Z', '+00:00'))
                    recorded_at = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass

            message += f"<b>#{idx}</b> - 📅 {recorded_at}\n"
            message += f"   👤 ηᴧϻє ✨: {record.get('first_name', 'N/A')} {record.get('last_name', 'N/A')}\n"
            message += f"   🔖 ᴜꜱєʀηᴧϻє ✨: @{record.get('username', 'None')}\n\n"

        message += "━━━━━━━━━━━━━━━━\n"
        message += "ℹ️ <i>ᴛʜɪꜱ ꜰєᴧᴛᴜʀє ᴛʀᴧᴄᴋꜱ ᴜꜱєʀηᴧϻє ᴧηᴅ ηᴧϻє ᴄʜᴧηɢєꜱ σᴠєʀ ᴛɪϻє ⏳✨</i>\n"
        message += "</blockquote>"

        return message

    def format_quick_info(self, user_id: int) -> str:
        history = self.db.get_user_history(user_id)

        if not history:
            return "📊 No history available"

        current = history[-1]
        changes = len(history) - 1

        info = f"👤 {current.get('first_name', 'N/A')}"
        if current.get('username'):
            info += f" (@{current.get('username')})"
        if changes > 0:
            info += f"\n🔄 {changes} change(s) detected"

        return info
