import os.path

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
import services.keyboard_builder as builder
from app.get_report_message import get_message
from app.keyboards import get_report_kb, filter_get_report_kb
from constants import RequestType, entity_url
from middleware.pm_middleware import PmMiddleware
from services.api import create_request
from states.ReportState import GetReportState
from datetime import datetime

from utils.to_excel import to_excel

get_report_router = Router()
get_report_router.callback_query.middleware(PmMiddleware())
get_report_router.message.middleware(PmMiddleware())

@get_report_router.message(F.text == "Выгрузка отчётов")
async def get_reports(message: Message, state: FSMContext):
  await state.set_state(GetReportState.report_type)
  await message.answer("Какую отчётность вы хотите получить?", reply_markup=get_report_kb)


@get_report_router.callback_query(GetReportState.report_type)
async def get_report_type(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  if callback.data == "message_report":
    await get_message(callback.message, state)
    return
  await state.update_data(report_type=callback.data)
  await state.set_state(GetReportState.filters)
  await callback.message.edit_text("Выберите фильтр для получения отчётности: ", reply_markup=filter_get_report_kb)

@get_report_router.callback_query(GetReportState.filters)
async def init_filters(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  await state.update_data(
    filter=callback.data,
    plan_id=None, plot_id=None,
    type_work_id=None,
    subtype_work_id=None,
    start_date=None,
    end_date=None,
    first_filter=None,
    second_filter=None
  )
  if callback.data == "by_date":
    await state.update_data(first_filter=None, second_filter="date")
  elif callback.data == "by_plot":
    await state.update_data(first_filter="plot", second_filter=None)
  elif callback.data == "by_plan":
    await state.update_data(first_filter="plan", second_filter=None)
  elif callback.data == "by_plan_and_date":
    await state.update_data(first_filter="plan", second_filter="date")
  elif callback.data == "by_plot_and_date":
    await state.update_data(first_filter="plot", second_filter="date")
  await get_data_filter(callback.message, state)

# Основная функция для разветвления получения отчётов
async def get_data_filter(message: Message, state: FSMContext):
  data = await state.get_data()
  if data.get("first_filter") == "plan" or data.get("first_filter") == "plot":
    await get_plot(message, state)
    return
  elif data.get("second_filter") == "date":
    await get_date_by_reports(message, state)
    return
  if data.get("report_type") == "production_report":
    type_work = create_request(
      RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
        "name": "Горно-буровые работы"
      })
    await state.update_data(type_work_id=type_work.get("id"))

  if data.get("first_filter") is None and data.get("second_filter") is None:
    await message.answer("Производится выгрузка отчётов...")
    reports = create_request(
      RequestType.GET.name, entity_url["report"], param={
        "plotId": data.get("plot_id"),
        "typeWorkId": data.get("type_work_id"),
        "subtypeWorkId": data.get("subtype_work_id"),
        "startDate": data.get("start_date"),
        "endDate": data.get("end_date"),
      })
    file_name = "report.xlsx"
    to_excel(reports, file_name)
    await state.clear()
    if os.path.exists(file_name):
      try:
        await message.answer_document(FSInputFile(file_name))
      except Exception as e:
        print(e)
        await message.reply(f"Ошибка при отправке файла")
    else:
      await message.reply("Файл не найден.")
      return
    await message.answer("Отчетность выгружена")
  else:
    print("Error. Data =", data.get("first_filter"), data.get("second_filter"))
    await message.answer("Произошла ошибка попробуйте позже")



# Получение дат
async def get_date_by_reports(message: Message, state: FSMContext):
  await state.set_state(GetReportState.start_date)
  await message.answer("Введите начальную дату в формате yyyy-mm-dd(например 2025-12-31):")


@get_report_router.message(GetReportState.start_date)
async def get_start_date(message: Message, state: FSMContext):
  try:
    start_date = datetime.strptime(message.text, "%Y-%m-%d")
    await state.update_data(start_date=start_date.date())
    await state.set_state(GetReportState.end_date)
    await message.answer(f"Вы ввели начальную дату: {start_date.date()}")
    await message.answer("Введите конечную дату в формате yyyy-mm-dd(на 2025-12-31):")
  except Exception as e:
    print(e)
    await message.answer("Некорректный формат даты. Введите дату в виде yyyy-mm-dd")

@get_report_router.message(GetReportState.end_date)
async def get_end_date(message: Message, state: FSMContext):
  try:
    end_date = datetime.strptime(message.text, "%Y-%m-%d")
    await state.update_data(end_date=end_date.date(), second_filter=None)
    await message.answer(f"Вы ввели конечную дату: {end_date.date()}")
    await get_data_filter(message, state)
  except Exception as e:
    print(e)
    await message.answer("Некорректный формат даты. Введите дату в виде yyyy-mm-dd")




# Получение участка и плана
async def get_plot(message: Message, state: FSMContext):
  await state.set_state(GetReportState.plot)
  plots_kb = builder.planing_plot()
  await message.answer("Выберите участок: ", reply_markup=plots_kb)

@get_report_router.callback_query(GetReportState.plot)
async def get_plot_id(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  plot_id = callback.data
  await state.update_data(plot_id=plot_id)
  data = await state.get_data()
  if data.get("first_filter") != "plan":
    await state.update_data(first_filter=None)
    await get_data_filter(callback.message, state)
    return

  if data.get("report_type") == "production_report":
    type_work = create_request(
      RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
        "name": "Горно-буровые работы"
      })
    await state.update_data(type_work_id=type_work.get("id"), type_work_name=type_work.get("name"))
    await state.set_state(GetReportState.subtype_work)
    subtype_works_kb = builder.planing_subtype_work(data.get("plot_id"), type_work.get("id"))
    await callback.message.answer(f"Выбериет тип работы: ", reply_markup=subtype_works_kb)
  else:
    await state.set_state(GetReportState.type_work)
    type_work_kb = builder.planing_type_work(plot_id)
    await callback.message.edit_text("Выберите вид работы: ", reply_markup=type_work_kb)

@get_report_router.callback_query(GetReportState.type_work)
async def get_type_work(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  type_work_id = callback.data
  await state.update_data(type_work_id=type_work_id)
  data = await state.get_data()
  await state.set_state(GetReportState.subtype_work)
  subtype_work_kb = builder.planing_subtype_work(data.get("plot_id"), type_work_id)
  await callback.message.edit_text("Выбериет тип работы: ", reply_markup=subtype_work_kb)

@get_report_router.callback_query(GetReportState.subtype_work)
async def get_subtype_work(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  subtype_work_id = callback.data
  await state.update_data(subtype_work_id=subtype_work_id, first_filter=None)
  await get_data_filter(callback.message, state)

