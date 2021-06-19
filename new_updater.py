"""
✘ Commands Available -
• `{i}update`
    See changelogs if any update is available.
"""

from git import Repo
from telethon.tl.functions.channels import ExportMessageLinkRequest as GetLink

from . import *

FUKING_PIC = "https://telegra.ph/file/1950f61eb163dc3c584f4.jpg"


@Lion.on(admin_cmd(pattern="update$"))
async def _(e):
    xx = await eor(e, "`Checking for updates...`")
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await tgbot.send_file(
            LOGS,
            FUKING_PIC,
            caption="• **Lɪᴏɴ X ᴜᴘᴅᴀᴛᴇ ᴀᴠᴀɪʟᴀʙʟᴇ** •",
            force_document=False,
            buttons=Button.inline("Changelogs", data="changes"),
        )
        Link = (await tgbot(GetLink(x.chat_id, x.id))).link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/TeamUltroid/Ultroid/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail")
@admin_cmd
async def updava(event):
    await event.delete()
    await tgbot.send_file(
        LOGS,
        FUKING_PIC,
        caption="• **Update Available** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
