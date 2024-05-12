import aiohttp
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command


class DeleteTaskForm(StatesGroup):
    waiting_for_task_id = State()


async def delete_task_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Please enter the task ID to delete:")
    await state.set_state(DeleteTaskForm.waiting_for_task_id)


async def delete_task_id(message: types.Message, state: FSMContext) -> None:
    task_id = message.text
    if not task_id.isdigit():
        await message.answer("Task ID should be a number. Please enter the task ID to delete:")
        return

    async with aiohttp.ClientSession() as session:
        response = await session.delete(f"http://localhost:8000/api/tasks/tasks/{task_id}")
        if response.status == 204:
            await message.answer(f"Task ID {task_id} has been successfully deleted.")
        elif response.status == 404:
            await message.answer(f"Task ID {task_id} was not found.")
        else:
            await message.answer(f"Failed to delete task ID {task_id}. Please try again later.")
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(delete_task_start, Command("delete_task"))
    dp.message.register(delete_task_id, DeleteTaskForm.waiting_for_task_id)
