from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants import RequestType, entity_url
from services.api import create_request

confirm_router = Router()




@confirm_router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
  await callback.message.edit_text("Отменено")
  await state.clear()

@confirm_router.callback_query(F.data == "confirm")
async def send_report(callback: CallbackQuery, state: FSMContext):
  data = await state.get_data()
  if "plan_id" not in data:
    plan = create_request(RequestType.GET.name, entity_url["plan"], param={
      "plotId": str(data.get("plot_id")),
      "typeWorkId": str(data.get("type_work_id")),
      "subtypeWorkId": str(data.get("subtype_work_id")),
      "productionName": ""
    })
    result = create_request(
      RequestType.POST.name, entity_url["report"], body={
        "planId": float(plan[0].get("id")),
        "whoSend": str(data.get("who_send")),
        "fact": float(data.get("fact")),
        "date": str(data.get("date")),
        "comment": data.get("comment"),
        "machine": data.get("machine")
      })
  else:
    result = create_request(
      RequestType.POST.name, entity_url["report"], body={
        "planId": int(data.get("plan_id")),
        "whoSend": data.get("who_send"),
        "fact": float(data.get("fact")),
        "date": str(data.get("date")),
        "comment": data.get("comment"),
        "machine": data.get("machine")
      })

  if result is None:
    await callback.message.edit_text("Не удалось отправить отчёт")
    await state.clear()
  else:
    await callback.message.edit_text("Отчёт отправлен")
    await state.clear()