from hydrogram import Client, filters
from hydrogram.errors import FloodWait,RPCError
from db import set_user_state,get_user_state,add_caption,get_caption,del_caption
from config import LOGS_ID
import asyncio

channel_id = LOGS_ID

@Client.on_message(filters.private & filters.command("set_caption"))
async def ask_for_caption(client,message):
    user_id = message.from_user.id

    try:
        await set_user_state(user_id,"waiting for caption")
        await message.reply_text("please provide text those you want to set as caption")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except RPCError as e:
        await client.send_message(chat_id=channel_id,text=f"error:- {e}")


@Client.on_message(filters.private & filters.text & ~filters.command([]))
async def save_caption(client,message):
    user_id = message.from_user.id

    if message.text.startswith("/"):
        return

    current_state = await get_user_state(user_id)

    try:
        if current_state == "waiting for caption":
            await add_caption(user_id,message.text)
            await set_user_state(user_id, "none")
            await message.reply_text("✅ **Caption saved successfully**")

        else:
            pass

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except RPCError as e:
        await client.send_message(chat_id=channel_id,text=f"error:- {e}")


@Client.on_message(filters.private & filters.command("caption"))
async def caption(client,message):
    user_id = message.from_user.id

    caption = await get_caption(user_id)

    await message.reply_text(caption)

@Client.on_message(filters.private & filters.command("del_caption"))
async def delete_caption(client,message):
    user_id = message.from_user.id

    await del_caption(user_id)

    await message.reply_text("caption deleted succesfully")
