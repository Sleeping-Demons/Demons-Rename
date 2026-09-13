from hydrogram import Client,filters


@Client.on_message(filters.private & filters.command("set_suffix"))
async def add_suffix(client,message):
    pass

@Client.on_message(filters.private & filters.command("set_suffix"))
async def remove_suffix(client,message):
    pass

@Client.on_message(filters.private & filters.command("set_suffix"))
async def add_prefix(client,message):
    pass

@Client.on_message(filters.private & filters.command("set_suffix"))
async def remove_prefix(client,message):
    pass
