# bot_add_task.py

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiohttp

# Определение состояния для добавления задачи
class TaskForm(StatesGroup):
    title = State()
    description = State()
    due_date = State()


# Начало диалога добавления задачи
async def add_task_start(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(TaskForm.title)


# Обработка названия задачи
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.description)
    await message.answer("Введите описание задачи:")


# Обработка описания задачи
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(TaskForm.due_date)
    await message.answer("Введите дату выполнения задачи (формат ГГГГ-ММ-ДД):")


# Функция для отправки задачи в API
async def create_task(task_data, telegram_id):
    task_data['telegram_id'] = telegram_id
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://localhost:8000/api/tasks/tasks/', json=task_data)
        print(await response.text())  # Для отладки


# Обработка даты завершения задачи и финализация задачи
async def process_due_date(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("Задача сохранена!")
    await create_task(data, message.from_user.id)


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(add_task_start, Command("add_task"))
    dp.message.register(process_title, TaskForm.title)
    dp.message.register(process_description, TaskForm.description)
    dp.message.register(process_due_date, TaskForm.due_date)
