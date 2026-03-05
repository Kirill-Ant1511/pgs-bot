import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import services.keyboard_builder as builder
from app.get_date_handler import get_date
from app.keyboards import confirm_kb, skip_kb
from constants import entity_url, RequestType
from middleware.user_middleware import UserMiddleware
from services.api import create_request
from states.ReportState import ReportState

send_report_router = Router()
send_report_router.message.middleware(UserMiddleware())
send_report_router.callback_query.middleware(UserMiddleware())

@send_report_router.message(F.text == "Отправить отчёт по выработкам")
async def send_production_report(message: Message, state: FSMContext):
  await state.clear()
  type_work = create_request(RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
    "name": "Горно-буровые работы"
  })
  await state.update_data(type_work_name=type_work.get("name"), type_work_id=type_work.get("id"), is_production=True)
  await send_report(message, state)

@send_report_router.message(F.text == "Отправить отчёт")
async def send_report(message: Message, state: FSMContext):
    data = await state.get_data()
    if "type_work_id" not in data:
      await state.clear()
    await message.answer("Отправка отчёта")
    plots_kb = builder.planing_plot()
    if plots_kb is None:
      await message.answer("Планы отсутвуют, попробуйте позже")
      return
    await state.set_state(ReportState.plot)
    await message.answer("Выберите участок", reply_markup=plots_kb)



@send_report_router.callback_query(ReportState.plot)
async def get_plot(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  plot_id = callback.data
  plot = create_request(RequestType.GET.name, entity_url["plot"] + f"/{plot_id}")
  await callback.message.edit_text(f"Вы выбрали участок: {plot.get("name")}")
  await state.update_data(plot_id=plot_id, plot_name=plot.get("name"))
  data = await state.get_data()
  if "type_work_id" in data:
    await state.set_state(ReportState.subtype_work)
    subtype_works_kb = builder.planing_subtype_work(data.get("plot_id"), data.get("type_work_id"))
    await callback.message.answer(f"Выбериет тип работы: ", reply_markup=subtype_works_kb)
  else:
    await state.set_state(ReportState.type_work)
    type_works_kb = builder.planing_type_work(plot_id)
    await callback.message.answer(f"Выберите вид работ", reply_markup=type_works_kb)

@send_report_router.callback_query(ReportState.type_work)
async def get_type_work(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  type_work_id = callback.data
  type_work = create_request(RequestType.GET.name, entity_url["type_work"] + f'/{type_work_id}')
  await callback.message.edit_text(f"Вы выбрали вид работы: {type_work.get("name")}")
  await state.update_data(type_work_id=type_work_id, type_work_name=type_work.get("name"))
  await state.set_state(ReportState.subtype_work)
  data = await state.get_data()
  subtype_works_kb = builder.planing_subtype_work(data.get("plot_id"), type_work_id)
  await callback.message.answer(f"Выбериет тип работы: ", reply_markup=subtype_works_kb)


@send_report_router.callback_query(ReportState.subtype_work)
async def get_subtype_work(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  subtype_work_id = callback.data
  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + f'/{subtype_work_id}')
  await callback.message.edit_text(f"Вы выбрали тип работы: {subtype_work.get("name")}")
  await state.update_data(subtype_work_id=subtype_work_id, subtype_work_name=subtype_work.get("name"), unit_metering=subtype_work.get("unitMetering"), next_handler=get_other_data)
  data = await state.get_data()
  if "is_production" in data:
    await state.set_state(ReportState.production_name)
    production_kb = builder.planing_production_name(data.get("plot_id"), data.get("type_work_id"), data.get("subtype_work_id"))
    if production_kb is None or production_kb == []:
      await callback.message.answer("Планы по выработкам отсутвуют, попробуйте позже")
      await state.clear()
      return
    await callback.message.answer(f"Выберите название выработки: ", reply_markup=production_kb)
  else:
    await get_date(callback.message, state)


@send_report_router.callback_query(ReportState.production_name)
async def get_production_name(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  plan = create_request(RequestType.GET.name, entity_url["plan"] + f'/{callback.data}')
  await callback.message.edit_text(f"Вы выбрали выработку {plan.get("productionName")}")
  await state.update_data(plan_id=callback.data, production_name=plan.get("productionName"))
  await get_date(callback.message, state)


async def get_other_data(message: Message, state: FSMContext):
  data = await state.get_data()
  if data.get("type_work_name") == "Горно-буровые работы":
    await state.set_state(ReportState.machine)
    await message.answer("Введите название станка: ")
  else:
    await state.set_state(ReportState.fact)
    await message.answer(f"Введите факт проделанной работы в {data.get("unit_metering")}:")

@send_report_router.message(ReportState.machine)
async def get_machine(message: Message, state: FSMContext):
  logger = logging.getLogger(__name__)
  logger.info(f"Machine message: {message.text}")
  await state.update_data(machine=message.text)
  await state.set_state(ReportState.fact)
  data = await state.get_data()
  await message.answer(f"Введите факт проделанной работы в {data.get("unit_metering")}:")

@send_report_router.message(ReportState.fact)
async def get_fact(message: Message, state: FSMContext):
  logger = logging.getLogger(__name__)
  try:
    logger.info(f"Message fact: {message.text}")
    fact = float(message.text)
    if message.from_user.username is None:
      user = create_request(RequestType.GET.name, entity_url["project_manager"] + f'/{message.from_user.id}')
      logger.info(f"User: {user}")
      who_send = user.get("name")
    else:
      who_send = message.from_user.username
    logger.info(f"Who_send: {who_send}")
    await state.update_data(fact=fact, next_handler=confirm_report_data, who_send=who_send)
    await state.set_state(ReportState.comment)
    await message.answer("Введите комментарий: ", reply_markup=skip_kb)
  except Exception as e:
    logger.error(f"Error: {e}\nString: {message.text}")
    await message.answer("Некорректный формат факта. Введите факт в виде числа")

@send_report_router.message(ReportState.comment)
async def get_comment(message: Message, state: FSMContext):
  logger = logging.getLogger(__name__)
  logger.info(f"Message comment: {message.text}")
  await state.update_data(comment=message.text, next_handler=confirm_report_data)
  await confirm_report_data(message, state)


async def confirm_report_data(message: Message, state: FSMContext):
  data = await state.get_data()
  if "comment" in data:
    comment = data.get("comment")
  else:
    comment = None
  if "machine" in data:
    machine = data.get("machine")
  else:
    machine = None
  if "production_name" in data:
    production_name = data.get("production_name")
  else:
    production_name = None
  await state.update_data(comment=comment, machine=machine, production_name=production_name)
  if data.get("type_work_name") == "Горно-буровые работы":
    await message.answer(f"""
Отправка отчёта:
  Участок: {data.get("plot_name")}
  Вид работы: {data.get("type_work_name")}
  Тип работы: {data.get("subtype_work_name")}
  Факт: {data.get("fact")}
  Дата: {data.get("date")}
  Комментарий: {comment}
  Станок: {machine}
  Название выработки: {production_name}
    """, reply_markup=confirm_kb)
  else:
    await message.answer(
      f"""
Отправка отчёта:
  Участок: {data.get("plot_name")}
  Вид работы: {data.get("type_work_name")}
  Тип работы: {data.get("subtype_work_name")}
  Факт: {data.get("fact")}
  Дата: {data.get("date")}
  Комментарий: {comment}
        """, reply_markup=confirm_kb)





