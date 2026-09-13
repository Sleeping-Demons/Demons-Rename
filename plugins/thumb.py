from hydrogram import Client,filters
from db import get_thumb_state, set_thumb_state, set_thumb, get_thumb,del_thumb
import os


THUMB_DIR="user_thumbs"
if not os.path.exists(THUMB_DIR):
    os.makedirs(THUMB_DIR)


@Client.on_message(filters.private & filters.command("set_thumb"))
async def add_thumb(client,message):
    user_id = message.from_user.id

    await set_thumb_state(user_id,"setting_thumb")
    await message.reply_text("now send me any image to set your custom thumbnail")

@Client.on_message(filters.private & filters.photo)
async def thumb_img(client,message):
    user_id = message.from_user.id

    thumb_state = await get_thumb_state(user_id)

    file_path = await client.download_media(message,file_name=f"{THUMB_DIR}/{user_id}.jpg")


    if thumb_state == "setting_thumb":

        string_path = str(file_path)
        await set_thumb(user_id,string_path)
        await set_thumb_state(user_id,"idle")
        await message.reply_text("thumbnail saved")

    else:
        pass

@Client.on_message(filters.private & filters.command("thumb"))
async def check_thumb(client,message):
    user_id = message.from_user.id

    thumb_path = await get_thumb(user_id)

    if os.path.exists(str(thumb_path)):
        await message.reply_photo(photo=thumb_path, caption="this is your current thumbnail")
    else:
        await message.reply_text("you have not saved any thumbnail yet")


@Client.on_message(filters.private & filters.command("del_thumb"))
async def delete_thumb(client,message):
    user_id = message.from_user.id

    thumb_path = await get_thumb(user_id)

    if os.path.exists(str(thumb_path)):
        os.remove(thumb_path)
        await del_thumb(user_id)
        await message.reply_text("deleted")
