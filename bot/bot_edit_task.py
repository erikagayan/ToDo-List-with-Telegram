from datetime import datetime
import aiohttp
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command


class EditTaskForm(StatesGroup):
    waiting_for_task_id = State()
    waiting_for_field_choice = State()
    waiting_for_new_value = State()


async def edit_task_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Please enter the task ID you want to edit:")
    await state.set_state(EditTaskForm.waiting_for_task_id)


async def process_task_id(message: types.Message, state: FSMContext) -> None:
    task_id = message.text
    if not task_id.isdigit():
        await message.answer("Task ID should be a number. Please enter the task ID to edit:")
        return

    await state.update_data(task_id=task_id)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Title"), KeyboardButton(text="Description")],
            [KeyboardButton(text="Due Date"), KeyboardButton(text="Completed")]
        ],
        resize_keyboard=True
    )

    await message.answer("Please select the field you want to edit:", reply_markup=keyboard)
    await state.set_state(EditTaskForm.waiting_for_field_choice)


async def process_field_choice(message: types.Message, state: FSMContext) -> None:
    field = message.text.lower()

    if field not in ["title", "description", "due date", "completed"]:
        await message.answer("Invalid choice. Please select a valid field to edit:")
        return

    await state.update_data(field=field)

    field_prompts = {
        "title": "Enter the new title:",
        "description": "Enter the new description:",
        "due date": "Enter the new due date (format YYYY-MM-DD):",
        "completed": "Enter whether the task is completed (yes/no):"
    }
    await message.answer(field_prompts[field], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(EditTaskForm.waiting_for_new_value)


async def process_new_value(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    task_id = data["task_id"]
    field = data["field"]

    new_value = message.text

    task_data = {}

    if field == "due date":
        try:
            due_date = datetime.strptime(new_value, "%Y-%m-%d").date()
        except ValueError:
            await message.answer("The date format is incorrect. Please enter the date in YYYY-MM-DD format.")
            return

        today = datetime.now().date()
        if due_date < today:
            await message.answer(
                "You cannot set a due date in the past. Please enter today's date or a future date."
            )
            return

        task_data["due_date"] = new_value
    elif field == "title":
        task_data["title"] = new_value
    elif field == "description":
        task_data["description"] = new_value
    elif field == "completed":
        task_data["completed"] = new_value.lower() == "yes"

    async with aiohttp.ClientSession() as session:
        response = await session.patch(
            f"http://localhost:8000/api/tasks/tasks/{task_id}/",
            json=task_data
        )

        if response.status == 200:
            await message.answer(
                "The task was successfully updated.",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="/list_tasks"), KeyboardButton(text="/add_task")],
                        [KeyboardButton(text="/edit_task"), KeyboardButton(text="/delete_task")],
                        [KeyboardButton(text="/get_task")]
                    ],
                    resize_keyboard=True
                )
            )
        else:
            await message.answer(
                "Failed to update the task. Please ensure the data is correct.",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="/list_tasks"), KeyboardButton(text="/add_task")],
                        [KeyboardButton(text="/edit_task"), KeyboardButton(text="/delete_task")],
                        [KeyboardButton(text="/get_task")]
                    ],
                    resize_keyboard=True
                )
            )

    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(edit_task_start, Command("edit_task"))
    dp.message.register(process_task_id, EditTaskForm.waiting_for_task_id)
    dp.message.register(process_field_choice, EditTaskForm.waiting_for_field_choice)
    dp.message.register(process_new_value, EditTaskForm.waiting_for_new_value)
