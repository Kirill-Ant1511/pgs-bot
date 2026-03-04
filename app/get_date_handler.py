from datetime import datetime, timedelta
import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.keyboards import date_kb
from states.ReportState import ReportState

get_date_router = Router()


async def get_date(message: Message, state: FSMContext):
  await message.answer("Введите дату в формате yyyy-mm-dd(например 2025-12-31): ", reply_markup=date_kb)
  await state.set_state(ReportState.date)


@get_date_router.message(ReportState.date)
async def get_date_handler(message: Message, state: FSMContext):
  logger = logging.getLogger(__name__)
  try:
    logger.info(f"Message date: {message.text}")
    date = datetime.strptime(message.text, "%Y-%m-%d")
    await state.update_data(date=date.date())
    data = await state.get_data()
    await message.answer(f"Вы ввели дату: {date.date()}")
    await  data.get("next_handler")(message, state)
  except Exception as e:
    logger.error(f"Message date: {message.text}\nError: {e}")
    await message.answer("Некорректный формат даты. Введите дату в формате yyyy-mm-dd(например 2025-12-31)")


@get_date_router.callback_query(F.data == "today")
async def get_today_date(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  date = datetime.now()
  await callback.message.edit_text(f"Вы выбрали дату: {date.date()}")
  await state.update_data(date=date.date())
  data = await state.get_data()
  await data.get("next_handler")(callback.message, state)

@get_date_router.callback_query(F.data == "yesterday")
async def get_yesterday_date(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  date = datetime.now() - timedelta(days=1)
  await callback.message.edit_text(f"Вы выбрали дату: {date.date()}")
  await state.update_data(date=date.date())
  data = await state.get_data()
  await data.get("next_handler")(callback.message, state)