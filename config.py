import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=os.environ.get("BOT_TOKEN")
API_ID=int(os.environ.get("API_ID", 0))
API_HASH=os.environ.get("API_HASH")
DB_URL=os.environ.get("DB_URL")
LOGS_ID=int(os.environ.get("LOGS_ID"))
