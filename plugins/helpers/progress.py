import math
import time
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancle", callback_data="cancle_rename")]
           ])

async def progress_baar(current,total,ud_type,message,start):
    now = time.time()
    diff = now - start

    if round(diff % 3.0) == 0 or current == total:

        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        eta  = round((total - current) / speed) if speed > 0 else 0

        completed_blocks = math.floor(percentage / 10)
        remaining_blocks = 10 - completed_blocks
        progress_bar = "█" * completed_blocks + "░" * remaining_blocks

        string = (
		f"**{ud_type}**\n"
		f"[{progress_bar}] **{percentage:.1f}%**\n"
                f"📁 **Progress:** {humanbytes(current)} / {humanbytes(total)}\n"
                f"⚡ **Speed:** {humanbytes(speed)}/s\n"
                f"⏱️ **ETA:** {TimeFormatter(eta)}"
        )

        try:
            await message.edit_text(string,reply_markup=keyboard)
        except Exception:
            pass

def humanbytes(size):
    if not size:
        return ""

    power = 2**10
    n = 0
    size_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {size_labels[n]}"

def TimeFormatter(seconds):
    minutes,seconds = divmod(int(seconds),60)
    hours,minutes = divmod(int(minutes),60)
    days,hours = divmod(hours,24)
    tmp = ((f"{days}d, ") if days else "") + \
          ((f"{hours}h, ") if hours else "") + \
          ((f"{minutes}m, ") if minutes else "") + \
          ((f"{seconds}s, ") if seconds else "")
    return tmp[:-2] if tmp else "0s"

