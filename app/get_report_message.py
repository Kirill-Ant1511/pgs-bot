from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import services.keyboard_builder as builder
from constants import RequestType, entity_url
from services.api import create_request
from states.ReportState import GetReportMessage
from utils.message import get_production_message

get_report_message_router = Router()


async def get_message(message: Message, state: FSMContext):
  await state.set_state(GetReportMessage.plot)
  plots_kb = builder.planing_plot()
  await message.answer("Выберите участок: ", reply_markup=plots_kb)

@get_report_message_router.callback_query(GetReportMessage.plot)
async def get_plot(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  plot_id = callback.data
  plot = create_request(RequestType.GET.name, entity_url["plot"] + f"/{plot_id}")
  await state.update_data(plot_id=plot_id, plot_name=plot.get("name"))
  await callback.message.edit_text(f"Вы выбрали участок: {plot.get('name')}")
  result = get_production_message(plot_id)
  await callback.message.answer(result)







