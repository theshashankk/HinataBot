import asyncio
import importlib
import re

import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from wbb import BOT_NAME, BOT_USERNAME, USERBOT_NAME, app
from wbb.modules import ALL_MODULES
from wbb.modules.sudoers import bot_sys_stats
from wbb.utils import paginate_modules

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    global COMMANDS_COUNT
    for module in ALL_MODULES:
        imported_module = importlib.import_module("wbb.modules." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              HINATA                           |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"[INFO]: HINATA IS READY TO ROCK!")
    print(f"[INFO]: USERBOT STARTED AS {USERBOT_NAME}!")
    await idle()


@app.on_message(filters.command(["help", "start"]))
async def help_command(_, message):
    if message.chat.type != "private":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Help ⁉️",
                        url=f"t.me/{BOT_USERNAME}?start=help",
                    ),
                    InlineKeyboardButton(
                        text="🚑 Support Group 🚑",
                        url="https://t.me/CoffinXsupport",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Hinata stats", callback_data="stats_callback"
                    ),
                    InlineKeyboardButton(
                        text="📔 Logs", url="t.me/HinataLogs"
                    ),
                ],
            ]
        )
        await message.reply("Pm Me For More Details.", reply_markup=keyboard)
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Commands 👨‍💻", callback_data="bot_commands"
                ),
                InlineKeyboardButton(
                    text="🚑 Support Group 🚑",
                    url="https://t.me/CoffinXsupport",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Hinata Stats 🖥", callback_data="stats_callback"
                ),
                InlineKeyboardButton(text="📓 Logs", url="t.me/HinataLogs"),
            ],
            [
                InlineKeyboardButton(
                    text="Add Me To Your Group 🎉",
                    url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
                )
            ],
        ]
    )
SAITAMA_IMG = "https://camo.githubusercontent.com/a8ca5d18d61bfdd4112d53657f6edc0e78d4d674f2f633b4e86d685c74a662d7/68747470733a2f2f74656c656772612e70682f66696c652f6362313938346432393861383635363166393864642e6a7067"    
        f"YOO!!! MY NAME IS {BOT_NAME} \nI HAVE AWESOME FEATURES TO MANAGE UR GROUP",
        reply_markup=keyboard,
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Yoo!! {first_name}
I'm {bot_name} An Group security Bot...
I have many awesome feature for you 💞""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id, text=text, reply_markup=keyboard
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Hello {query.from_user.first_name}! My name is {BOT_NAME}!
I'm a group management bot with some usefule features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.

General command are:
 - /start: Start the bot
 - /help: Give this message
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text, reply_markup=keyboard, disable_web_page_preview=True
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
