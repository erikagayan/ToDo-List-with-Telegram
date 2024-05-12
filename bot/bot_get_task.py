import aiohttp
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command


class GetTaskForm(StatesGroup):
    waiting_for_task_id = State()


async def get_task_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Please enter the task ID:")
    await state.set_state(GetTaskForm.waiting_for_task_id)


async def get_task_id(message: types.Message, state: FSMContext) -> None:
    task_id = message.text
    if not task_id.isdigit():
        await message.answer("Task ID should be a number. Please enter the task ID:")
        return

    async with aiohttp.ClientSession() as session:
        response = await session.get(f"http://localhost:8000/api/tasks/tasks/{task_id}")
        if response.status == 200:
            task = await response.json()
            if task['telegram_id'] == message.from_user.id:
                task_details = (
                    f"Task ID: {task['id']}\n"
                    f"Title: {task['title']}\n"
                    f"Description: {task['description']}\n"
                    f"Due Date: {task['due_date']}\n"
                    f"Completed: {'Yes' if task['completed'] else 'No'}"
                )
                await message.answer(task_details)
            else:
                await message.answer("This task does not belong to you.")
        else:
            await message.answer("Task not found or error retrieving the task.")
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(get_task_start, Command("get_task"))
    dp.message.register(get_task_id, GetTaskForm.waiting_for_task_id)
