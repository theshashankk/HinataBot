import random
from datetime import datetime

from pyrogram import filters

from hinataBot import app
from HinataBot.pyrogramee.decorators.errors import capture_err
from hinataBot.utils.dbfunc import get_couple, save_couple

__mod_name__ = "Gay"
__help__ = "/detect_gay - To get gay of the day 😂😂"


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@app.on_message(filters.command("detect_gay") & ~filters.edited)
@capture_err
async def couple(_, message):
    if message.chat.type == "private":
        return await message.reply_text("I don't think it's a group 😒😒😒")
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in app.iter_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("Not enough users")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""**𝙽𝙸𝙱𝙱𝙰 𝙾𝙵 𝚃𝙷𝙴 𝙳𝙰𝚈👀:**
{c1_mention} + {c2_mention} = ❤️

__𝙽𝙴𝚆 𝙽𝙸𝙱𝙱𝙰 𝙾𝙵 𝚃𝙷𝙴 𝙳𝙰𝚈 𝙼𝙰𝚈 𝙱𝚈 𝙱𝙴 𝙼𝙰𝚈𝙱𝙴 𝙲𝙷𝙾𝙾𝚂𝙴𝙽 𝙰𝚃 12:00 𝙰𝙼 {tomorrow}__"""
            await app.send_message(
                message.chat.id, text=couple_selection_message
            )
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""𝙽𝙸𝙱𝙱𝙰 & 𝙽𝙸𝙱𝙱𝙸 𝙾𝙵 𝚃𝙷𝙴 𝙳𝙰𝚈:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 𝙽𝙸𝙱𝙱𝙰 & 𝙽𝙸𝙱𝙱𝙸 🤓✨💞

__𝙽𝙴𝚆 𝙽𝙸𝙱𝙱𝙰 𝙾𝙵 𝚃𝙷𝙴 𝙳𝙰𝚈 𝙼𝙰𝚈 𝙱𝚈 𝙱𝙴 𝙼𝙰𝚈𝙱𝙴 𝙲𝙷𝙾𝙾𝚂𝙴𝙽 𝙰𝚃 12:00 𝙰𝙼 {tomorrow}__"""
            await app.send_message(
                message.chat.id, text=couple_selection_message
            )
    except Exception as e:
        print(e)
        await message.reply_text(e)
