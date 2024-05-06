import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


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


# For add task button
class TaskForm(StatesGroup):
    title = State()
    description = State()
    due_date = State()


@dp.message(Command("add_task"))
async def add_task_start(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(TaskForm.title)


# Handler for processing the title of the task
@dp.message(TaskForm.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.description)
    await message.answer("Введите описание задачи:")


# Handler for processing the description of the task
@dp.message(TaskForm.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(TaskForm.due_date)
    await message.answer("Введите дату выполнения задачи (формат ГГГГ-ММ-ДД):")


# Handler for processing the due date of the task
async def create_task(task_data, telegram_id):
    task_data['telegram_id'] = telegram_id
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://localhost:8000/api/tasks/tasks/', json=task_data)
        print(await response.text())  # Для отладки

@dp.message(TaskForm.due_date)
async def process_due_date(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("Задача сохранена!")
    # Отправляем данные вместе с Telegram ID пользователя
    await create_task(data, message.from_user.id)

#

if __name__ == '__main__':
    dp.run_polling(bot, on_startup=on_startup)
