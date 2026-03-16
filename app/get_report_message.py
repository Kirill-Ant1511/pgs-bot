from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import services.keyboard_builder as builder
from constants import RequestType, entity_url
from middleware.pm_middleware import PmMiddleware
from services.api import create_request
from states.ReportState import GetReportMessage
from utils.message import get_production_message

get_report_message_router = Router()
get_report_message_router.message.middleware(PmMiddleware())
get_report_message_router.callback_query.middleware(PmMiddleware())


async def get_message(message: Message, state: FSMContext, user_id: int):
  await state.set_state(GetReportMessage.plot)
  plots_kb = builder.planing_plot(user_id)
  if plots_kb is None:
    await message.answer("Вы не привязаны ни к одному из участков. Или планов по вашему участку ещё нету.")
    return
  await message.answer("Выберите участок: ", reply_markup=plots_kb)

@get_report_message_router.callback_query(GetReportMessage.plot)
async def get_date(callback: CallbackQuery, state: FSMContext):
  plot_id = callback.data
  plot = create_request(RequestType.GET.name, entity_url["plot"] + f"/{plot_id}")
  await state.set_state(GetReportMessage.date)
  await state.update_data(plot_id=plot_id, plot_name=plot.get("name"))
  kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="За сегодня", callback_data="from_today"),
    InlineKeyboardButton(text="За вчера", callback_data="from_yesterday")
  ]])
  await callback.message.edit_text("За какой день вы хотите выгрузить отчёт", reply_markup=kb)


@get_report_message_router.callback_query(GetReportMessage.date)
async def get_plot(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  if callback.data == "from_today":
    current_date = datetime.now()
  elif callback.data == "from_yesterday":
    current_date = datetime.now() - timedelta(days=1)
  else:
    current_date = datetime.now()
  date = await state.get_data()
  result = get_production_message(date.get("plot_id"), current_date)
  await callback.message.edit_text(result)







