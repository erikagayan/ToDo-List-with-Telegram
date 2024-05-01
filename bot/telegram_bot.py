import aiohttp
from aiogram import Bot, Dispatcher
from telegram_api.models import TelegramUser
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
    username = message.from_user.username
    if username is None:
        await message.answer(
            "Извините, но ваш аккаунт Telegram не имеет username. Пожалуйста, установите username в настройках Telegram для использования этой функции.")
        return

    # Сохраняем username в контексте состояния
    await state.update_data(username=username)
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


async def get_telegram_user_by_username(username):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'http://localhost:8000/api/telegram_users/?username={username}')
        if response.status == 200:
            data = await response.json()
            if data:
                return TelegramUser(**data[0])
        return None

# Handler for processing the due date of the task
async def create_task(task_data):
    async with aiohttp.ClientSession() as session:
        # Получаем username из контекста состояния
        username = task_data.get('username')
        if username is None:
            print("Не удалось получить username пользователя.")
            return

        # Поиск пользователя по username
        telegram_user = await get_telegram_user_by_username(username)
        if telegram_user is None:
            print(f"Пользователь с username {username} не найден.")
            return

        # Создание задачи, связанной с пользователем
        task_data['user'] = telegram_user.user.id
        response = await session.post('http://localhost:8000/api/tasks/tasks/', json=task_data)
        if response.status == 201:
            print("Задача успешно создана")
        else:
            print("Ошибка при создании задачи", response.status)


@dp.message(TaskForm.due_date)
async def process_due_date(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("Задача сохранена!")
    # Send data to the server
    await create_task(data)


if __name__ == '__main__':
    dp.run_polling(bot, on_startup=on_startup)
