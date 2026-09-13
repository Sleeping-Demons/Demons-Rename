
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


from hydrogram import Client
from config import BOT_TOKEN , API_ID , API_HASH

bot=Client("my_bot",bot_token=BOT_TOKEN,api_hash=API_HASH,api_id=API_ID,plugins=dict(root="plugins"))



def main():

    print("i am started")

    bot.run()


if __name__ == "__main__":
    main()
