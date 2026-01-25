from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.get_date_handler import get_date

skip_router = Router()



@skip_router.callback_query(F.data == "skip")
async def skip(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  data = await state.get_data()
  await data.get("next_handler")(callback.message, state)