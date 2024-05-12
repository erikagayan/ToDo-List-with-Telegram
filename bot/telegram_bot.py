import os
import bot_add_task
import bot_get_task
import bot_list_tasks
from typing import Any
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API token not found! Check the .env file")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

"""Bot buttons"""
keyboard_commands = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/list_tasks"), KeyboardButton(text="/add_task")],
        [KeyboardButton(text="/edit_task"), KeyboardButton(text="/delete_task")],
        [KeyboardButton(text="/get_task")]
    ],
    resize_keyboard=True
)


async def on_startup(_) -> None:
    print("The bot is up and running!")


# Start command
@dp.message(Command("start"))
async def send_welcome(message: Message) -> None:
    welcome_text = "Hi! Here's a list of available commands:"
    await message.answer(text=welcome_text, reply_markup=keyboard_commands)


# Add task button
bot_add_task.register_handlers(dp)
bot_list_tasks.register_handlers(dp)
bot_get_task.register_handlers(dp)


if __name__ == '__main__':
    dp.run_polling(bot, on_startup=on_startup)
