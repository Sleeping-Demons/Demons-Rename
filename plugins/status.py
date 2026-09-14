from hydrogram import Client,filters
from db import get_users

@Client.on_message(filters.private & (filters.command("status")))
async def status_cmd(client,message):
    users = await get_users()

    await message.reply_text(users)
