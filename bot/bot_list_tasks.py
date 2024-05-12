import aiohttp
from aiogram import Dispatcher, types
from aiogram.filters import Command


async def list_tasks(message: types.Message) -> None:
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        # Query all tasks, then filter them by telegram_id
        response = await session.get("http://localhost:8000/api/tasks/tasks/")
        if response.status == 200:
            tasks = await response.json()
            user_tasks = [task for task in tasks if task['telegram_id'] == telegram_id]
            if user_tasks:
                tasks_text = "\n".join(
                    f"{idx + 1}. {task['title']}: {task['description']} (Due: {task['due_date']})"
                    for idx, task in enumerate(user_tasks)
                )
            else:
                tasks_text = "You have no tasks."
            await message.answer(tasks_text)
        else:
            await message.answer("Failed to retrieve tasks. Please try again later.")


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(list_tasks, Command("list_tasks"))
