import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
import asyncio

API_TOKEN = '6999401311:AAHwxbf7VUQHCBYMLujabw_t46NDgNhL2K8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


#buttons
keyboard_commands = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/list_tasks"), KeyboardButton(text="/add_task")],
        [KeyboardButton(text="/edit_task"), KeyboardButton(text="/delete_task")],
        [KeyboardButton(text="/get_task")]
    ],
    resize_keyboard=True
)


async def on_startup(_):
    print("Бот запущен!")


@dp.message(Command("start"))
async def send_welcome(message: Message):
    welcome_text = "Привет! Вот список доступных команд:"
    await message.answer(text=welcome_text, reply_markup=keyboard_commands)


if __name__ == '__main__':
    dp.run_polling(bot, on_startup=on_startup)
