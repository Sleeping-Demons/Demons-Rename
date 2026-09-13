from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from hydrogram.errors import MessageNotModified
from hydrogram import enums
from .helpers.text import HELP_TEXT , ABOUT_TEXT

Keyboard = [[InlineKeyboardButton("About", callback_data="about_text"),
            InlineKeyboardButton("Help", callback_data="help_text")],
            [InlineKeyboardButton("Update", url="https://t.me/DemonsBots_Support"),
            InlineKeyboardButton("Support", url="https://t.me/sd_botsSupport")],
            [InlineKeyboardButton("Source", url="https://github.com/Sleeping-Demons/Demons-Rename.git")]]



reply_markup = InlineKeyboardMarkup(Keyboard)

START_TEXT = """ I am Kakashi a file renamer bot """

START_IMG= "https://i.ibb.co/5xTJnKpF/image.jpg"

BACK_KEYBOARD = [[InlineKeyboardButton("Back", callback_data="back")]]
REPLY_MARKUP = InlineKeyboardMarkup(BACK_KEYBOARD)
@Client.on_message(filters.command("start") & filters.private)
async def start(client , message):
    await message.reply_photo(photo=START_IMG,caption=START_TEXT, reply_markup=reply_markup)


@Client.on_callback_query()
async def handle_menus(client , callback_query: CallbackQuery):
    data = callback_query.data

    try:
        await callback_query.answer()

        if data == "about_text":
            await callback_query.edit_message_text(text=ABOUT_TEXT, reply_markup=REPLY_MARKUP)

        elif data == "help_text":
            await callback_query.edit_message_text(text=HELP_TEXT , reply_markup=REPLY_MARKUP)

        elif data == "back":
            await callback_query.edit_message_text(START_TEXT,reply_markup=reply_markup)

    except MessageNotModified:
        pass
