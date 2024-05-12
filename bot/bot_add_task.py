import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any
from datetime import datetime


# Defining the state for adding a task
class TaskForm(StatesGroup):
    title: State = State()
    description: State = State()
    due_date: State = State()


# Beginning of the dialogue box for adding a task
async def add_task_start(message: Message, state: FSMContext) -> None:
    await message.answer("Enter the name of the task:")
    await state.set_state(TaskForm.title)


async def process_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.description)
    await message.answer("Enter a description of the task:")


async def process_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(TaskForm.due_date)
    await message.answer("Enter the date of the task (format YYYYY-MM-DD):")


# Function for sending a task to the API
async def create_task(task_data: Dict[str, Any], telegram_id: int) -> None:
    task_data["telegram_id"] = telegram_id
    async with aiohttp.ClientSession() as session:
        response = await session.post("http://localhost:8000/api/tasks/tasks/", json=task_data)
        print(await response.text())  # To debug


# Process the task end date and finalise the task
async def process_due_date(message: Message, state: FSMContext) -> None:
    # Checking if the date is correct
    try:
        due_date = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("The date format is incorrect. Please enter the date in YYYY-MM-DD format.")
        return

    # Check that the entered date is not earlier than today's date
    today = datetime.now().date()
    if due_date < today:
        await message.answer(
            "You cannot create a task with a date in the past. Please enter today's date or a future date.")
        return

    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("The task is saved!")
    await create_task(data, message.from_user.id)


# Handler registration
def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(add_task_start, Command("add_task"))
    dp.message.register(process_title, TaskForm.title)
    dp.message.register(process_description, TaskForm.description)
    dp.message.register(process_due_date, TaskForm.due_date)
