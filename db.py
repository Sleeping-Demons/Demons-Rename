from pymongo import AsyncMongoClient
from config import DB_URL


client=AsyncMongoClient(DB_URL)

db=client["rename_bot"]
USERS=db["users"]

async def add_user(user_id):
    await USERS.insert_one({"user_id":user_id})

async def get_users():
    users = await USERS.count_documents({})
    return users

async def add_caption(user_id,caption):
    await USERS.update_one({"user_id":user_id},
				{"$set":{"caption":caption}}
				)

async def get_caption(user_id):
    user = await USERS.find_one({"user_id":user_id},{"caption":1})
    return user.get("caption") if user else None

async def del_caption(user_id):
    await USERS.update_one({"user_id":user_id},
				{"$unset":{"caption":""}}
				)

async def set_user_state(user_id,state:str):
    await USERS.update_one({"user_id":user_id},
				{"$set":{"state":state}},upsert=True)

async def get_user_state(user_id):
    users = await USERS.find_one({"user_id":user_id})
    return users.get("state") if users else None


async def set_thumb(user_id,img_id):
    await USERS.update_one({"user_id":user_id},
				{"$set":{"img_id":img_id}}
				)
async def get_thumb(user_id):
    user = await USERS.find_one({"user_id":user_id},{"img_id":1})
    return user.get("img_id") if user else None

async def del_thumb(user_id):
    await USERS.update_one({"user_id":user_id},{"$unset":{"img_id":""}})

async def set_thumb_state(user_id,state:str):
    await USERS.update_one({"user_id":user_id},
                                {"$set":{"thumb_state":state}},upsert=True)

async def get_thumb_state(user_id):
    users = await USERS.find_one({"user_id":user_id})
    return users.get("thumb_state") if users else None

async def set_suffix(user_id,suffix_text):
    await USERS.update_one({"user_id":user_id},
				{"$set":{"suffix":suffix_text}}
				)

async def get_suffix(user_id):
    user = await USERS.find_one({"user_id":user_id},{"suffix":1})
    return user.get("suffix") if user else None

async def del_suffix(user_id):
    await USERS.update_one({"user_id":user_id},{"$unset":{"suffix":""}})



async def set_prefix(user_id,prefix_text):
    await USERS.update_one({"user_id":user_id},
                                {"$set":{"prefix":prefix_text}}
                                )

async def get_prefix(user_id):
    user = await USERS.find_one({"user_id":user_id},{"prefix":1})
    return user.get("prefix") if user else None

async def del_prefix(user_id):
    await USERS.update_one({"user_id":user_id},{"$unset":{"prefix":""}})

