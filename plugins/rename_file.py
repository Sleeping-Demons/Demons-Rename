import asyncio
from hydrogram import Client , filters
from hydrogram.errors import FloodWait, RPCError
from hydrogram.enums import ParseMode
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os
from db import get_caption,get_thumb,get_suffix,get_prefix
from config import LOGS_ID
from .helpers.progress import progress_baar
import time
from db import get_caption

channel_id = LOGS_ID
MAX_CONCURRENT_TASK = 10
Semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASK)


async def send_media(client,chat_id,media,thumb,caption,orignal_message,progress=None,progress_args=None):

    if orignal_message.video:
        video_obj = orignal_message.video
        return await orignal_message.reply_video(video=media,
                thumb=thumb,
                caption=caption,
                duration=video_obj.duration if video_obj else None,
                width=video_obj.width if video_obj else None,
                height=video_obj.height if video_obj else None,
                supports_streaming=True,
                progress=progress,
                progress_args=progress_args)
    elif orignal_message.audio:
        audio_obj = orignal_message.audio
        return await orignal_message.reply_audio(audio=media,
                thumb=thumb,
                caption=caption,
                duration=audio_obj.duration if audio_obj else None,
                progress=progress,
                progress_args=progress_args)
    else:
        return await orignal_message.reply_document(document=media,thumb=thumb,caption=caption,progress=progress,progress_args=progress_args)

async def orignal_name(orignal_message):
    if orignal_message.video:
        return orignal_message.video.file_name
    elif orignal_message.audio:
        full_name=orignal_message.audio.file_name
        real_name=os.path.splitext(full_name)[0]
        return real_name
    else:
        full_name=orignal_message.document.file_name
        real_name=os.path.splitext(full_name)[0]
        return real_name

user_step={}

keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancle", callback_data="cancle_rename")]
           ])



@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def file_name(client,message):
    user_id = message.from_user.id

    old_name = await orignal_name(message)

    prompt_msg = await message.reply_text(f"Please <b>reply to this message</b> with the new name for your file. \n\n Old File Name :- <code>{old_name}</code>",
        reply_to_message_id=message.id,
        parse_mode=ParseMode.HTML)

    active_key = (user_id,prompt_msg.id)
    user_step[active_key] = {"media_message":message,
                         "prompt_message_id":prompt_msg.id,
                         "is_cancelled" : False,
                         "current_status_message" : prompt_msg}

async def strict_progress(current, total, client, user_id,task_key, phase_text, msg, start_time):

    if task_key in user_step and user_step[task_key].get("is_cancelled"):
        try:
            client.stop_transmission()
        except:
            pass
        return

    print(
    f"{time.time():.2f} [{user_id}] "
    f"{phase_text}: {current}/{total}"
)

    if msg and start_time:
        await progress_baar(current, total, phase_text, msg, start_time)

@Client.on_callback_query(filters.private & (filters.regex("cancle_rename")))
async def cancle_handler(client : Client, callback_query : CallbackQuery):
    user_id  = callback_query.from_user.id
    clicked_msg_id = callback_query.message.id

    target_key = None

    for key , data in user_step.items():
        if key[0] == user_id and data.get("current_status_message_id") == clicked_message_id:
            target_key = key
            break

    if not target_key:
        for key in list(user_step.keys()):
            if key[0] == user_id:
                target_key = key
                break

    if target_key and target_key in user_step:
        user_step[target_key]["is_cancelled"] = True

        try:
           await client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=clicked_message_id)
           await callback_query.message.reply_text("opration cancelled by user")
           await callback_query.message.delete()

        except:
            pass

        del user_step[target_key]
        await callback_query.answer("Process cancelled succesfully")
    
    else:
         await callback_query.answer("no active process to cancle", show_alert=True)




async def process_rename_worker(client,message,active_key,user_id,new_name,prompt_message_id):


    async with Semaphore:
        msg = await message.reply_text("Downloading file, please wait...", reply_markup=keyboard)


        try:
            await client.delete_messages(chat_id=message.chat.id,messages_id=prompt_message_id)
            await message.delete()

        except:
            pass

        custom_caption = await get_caption(user_id)
        user_step[active_key]["current_status_message_id"] = msg.id
        user_step[active_key]["current_status_message"] = msg
        media_message = user_step[active_key]["media_message"]
        start_time = time.time()

        file_path = None
        new_file_path = None

        try:
            print(f"{time.time():.2f} [{user_id}] DOWNLOAD START")
            file_path = await client.download_media(media_message,progress=strict_progress,progress_args=(client,user_id,active_key,"Downloading",msg,start_time))
            print(f"{time.time():.2f} [{user_id}] DOWNLOAD END")
            await msg.edit_text("downloading completed now renaming...",reply_markup=keyboard)



            if  user_step[active_key].get("is_cancelled" or not file_path):
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                await msg.edit_text("process cancelled 💢💢")
                await asyncio.sleep(3)
                await msg.delete()
                return

            ext = os.path.splitext(file_path)[1]


            prefix_text = await get_prefix(user_id)
            prefix_text = " ".join(prefix_text) if prefix_text else ""
            suffix_text = await get_suffix(user_id)
            suffix_text = " ".join(suffix_text) if suffix_text else ""
            new_file_path=f"{prefix_text} {new_name}{f' {suffix_text}' if suffix_text else ''}{ext}"
            thumb = await get_thumb(user_id)
            thumb = str(thumb) if thumb else None
            renamed = os.rename(file_path,new_file_path)


            if  user_step[active_key].get("is_cancelled" or not file_path):
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                await msg.edit_text("process cancelled 💢💢")
                await asyncio.sleep(3)
                await msg.delete()
                return

            start_time = time.time()
            print(f"{time.time():.2f} [{user_id}] UPLOAD START")
            await send_media(client,
                chat_id=message.chat.id,
                media=new_file_path,
                thumb=thumb,
                caption=custom_caption if custom_caption else new_file_path ,
                orignal_message=message,
                progress=strict_progress,
                progress_args=(client, user_id, active_key, "Uploading",msg,start_time))
            print(f"[{user_id}] UPLOAD END")
            await msg.delete()
            if os.path.exists(new_file_path):
                os.remove(new_file_path)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except RPCError as e:
            await client.send_message(chat_id=channel_id,text=f"Error : {e}")







@Client.on_message(filters.private & filters.text)
async def rename(client,message):
    user_id = message.from_user.id
    active_key = None

    for key , data in user_step.items():
        if key[0] == user_id and message.reply_to_message and message.reply_to_message_id == data.get(str("prompt_message_id")):
            active_key = key
            break

    if not active_key:
        return

    new_name = message.text
    prompt_message_id = user_step[active_key]["prompt_message_id"]

    asyncio.create_task(process_rename_worker(client,message,active_key,user_id,new_name,prompt_message_id))

