import time
from pyrogram import Client, filters
from wbb import
"""
fuck off kanger 
"""
from wbb.helper_functions.cust_p_filters import f_onw_fliter

@Client.on_message(filters.command("ping", COMMAND_HAND_LER) & f_onw_fliter)
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"""ＰＯＮＧ !!\n𝚃𝙸𝙼𝙴 𝚃𝙰𝙺𝙴𝙽: {time_taken_s:.3f}\n𝙷𝙸𝙽𝙰𝚃𝙰 𝚄𝙿𝚃𝙸𝙼𝙴: {uptime}""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📘 logs", url="https://t.me/HinataLogs")
                ]
            ]
        )
   )
                
