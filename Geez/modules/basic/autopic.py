# if you can read this, this meant you use code from Geez Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Geez and Ram doesn't care about credit
# at least we are know as well
# who Geez and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Geez & Ram Team
import asyncio
from datetime import datetime
from pathlib import Path
from random import choice
from shutil import copyfile
from geezlibs.geez.helper.basic import eor
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters, Client

from Geez import SUDO_USER
from Geez.modules.basic import add_command_help
from Geez import cmds

__XOR = []
FIRST_TIME = True
DIM = [(100, 200), (1280, 200), (1280, 1600), (100, 1600)]


async def _autopic(_, delay):
    global FIRST_TIME

    while bool(__XOR):
        await asyncio.sleep(delay)
        original = "cache/autopic-template.jpg"
        photo = "pic.png"
        copyfile(original, photo)
        current_time = datetime.now().strftime(
            f'%H:%M %d-%m-%y\nLife Is too short\nto argue.\njust say "fuck off"\nand move on.'
        )
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("cache/autopic-font-ubuntu.ttf", 60)
        drawn_text.text(choice(DIM), current_time, font=fnt, fill=(0, 0, 0))
        img.save(photo)
        try:
            if not FIRST_TIME:
                async for pic in _.get_chat_photos("me", limit=1):
                    await _.delete_profile_photos(pic.file_id)
                    await asyncio.sleep(2)
            await _.set_profile_photo(photo=photo)
            FIRST_TIME = False
        except Exception as exc:
            print("Autopic Error: " + exc)
        finally:
            Path(photo).unlink()


@Client.on_message(
    filters.command(["autopic"], cmds) & (filters.me | filters.user(SUDO_USER))
)
async def autopic_Geez(_, m):
    global __XOR
    arc = await eor(m, "...")
    if bool(__XOR):
        __XOR[0].cancel()
        t = "`Autopic Stopped Successfully.`"
        __XOR.clear()
    else:
        _task = _autopic(_, delay=300)
        task = asyncio.create_task(_task)
        __XOR.append(task)
        t = "`Started Autopic.`"
    await arc.edit_text(t)


add_command_help(
    "autopic",
    [[f"{cmds}autopic", f"Change your DP every 5 minute. \nRun {cmds}autopic again to stop it."]],
)
