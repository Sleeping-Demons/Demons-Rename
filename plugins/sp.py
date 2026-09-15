from hydrogram import Client,filters
from db import get_suffix,set_suffix,del_suffix,get_prefix,set_prefix,del_prefix

@Client.on_message(filters.private & filters.command("set_suffix"))
async def add_suffix(client,message):
    user_id = message.from_user.id

    if len(message.command) < 2:
        await message.reply_text("set suffix like this /set_suffix your text")
        return

    suffix_text = message.command[1:]
    await set_suffix(user_id,suffix_text)

    await message.reply_text("suffix set succesfully you can check it by doing /suffix command")


@Client.on_message(filters.private & filters.command("del_suffix"))
async def remove_suffix(client,message):
    user_id = message.from_user.id

    try:
        await del_suffix(user_id)
        await message.reply_text("suffix deleted succesfully")
    except:
        await message.reply_text("you have not set any suffux yet")


@Client.on_message(filters.private & filters.command("suffix"))
async def suffix(client,message):
    user_id = message.from_user.id

    suffix_text = await get_suffix(user_id)
    if suffix_text:
        suffix_text = " ".join(suffix_text)
        await message.reply_text(suffix_text)

    else:
        await message.reply_text("set suffix first")



@Client.on_message(filters.private & filters.command("set_prefix"))
async def add_prefix(client,message):
    user_id = message.from_user.id

    if len(message.command) < 2:
        await message.reply_text("set prefix like this /set_prefix your text ")
        return

    suffix_text = message.command[1:]
    await set_prefix(user_id,prefix_text)

    await message.reply_text("prefix set succesfully you can check it by doing /suffix command")


@Client.on_message(filters.private & filters.command("del_prefix"))
async def remove_prefix(client,message):
    user_id = message.from_user.id

    try:
        await del_prefix(user_id)
        await message.reply_text("prefix deleted succesfully")
    except:
        await message.reply_text("you have not set any prefix yet")


@Client.on_message(filters.private & filters.command("prefix"))
async def prefix(client,message):
    user_id = message.from_user.id

    prefix_text = await get_prefix(user_id)
    if prefix_text:
        prefix_text = " ".join(prefix_text)
        await message.reply_text(prefix_text)

    else:
        await message.reply_text("set prefix first")
