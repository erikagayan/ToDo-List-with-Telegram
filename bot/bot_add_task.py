import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any

# Определение состояния для добавления задачи
class TaskForm(StatesGroup):
    title: State = State()
    description: State = State()
    due_date: State = State()


# Начало диалога добавления задачи
async def add_task_start(message: Message, state: FSMContext) -> None:
    await message.answer("Введите название задачи:")
    await state.set_state(TaskForm.title)


# Обработка названия задачи
async def process_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.description)
    await message.answer("Введите описание задачи:")


# Обработка описания задачи
async def process_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(TaskForm.due_date)
    await message.answer("Введите дату выполнения задачи (формат ГГГГ-ММ-ДД):")


# Функция для отправки задачи в API
async def create_task(task_data: Dict[str, Any], telegram_id: int) -> None:
    task_data['telegram_id'] = telegram_id
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://localhost:8000/api/tasks/tasks/', json=task_data)
        print(await response.text())  # Для отладки


# Обработка даты завершения задачи и финализация задачи
async def process_due_date(message: Message, state: FSMContext) -> None:
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("Задача сохранена!")
    await create_task(data, message.from_user.id)


# Регистрация обработчиков
def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(add_task_start, Command("add_task"))
    dp.message.register(process_title, TaskForm.title)
    dp.message.register(process_description, TaskForm.description)
    dp.message.register(process_due_date, TaskForm.due_date)
