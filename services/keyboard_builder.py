from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import RequestType, entity_url
from services.api import create_request


def planing_plot():
  plots = create_request(RequestType.GET.name, entity_url["plot"] + '/planing')
  keyboard = InlineKeyboardBuilder()
  if plots is None:
    return None
  for plot in plots:
    keyboard.add(InlineKeyboardButton(text=f"{plot.get("name")}", callback_data=f"{plot.get("id")}"))
  keyboard.adjust(1)
  return keyboard.as_markup()

def planing_type_work(plot_id):
  type_works = create_request(RequestType.GET.name, entity_url["type_work"] + '/planing', param={"plotId": str(plot_id)})
  keyboard = InlineKeyboardBuilder()
  if type_works is None:
    return None
  for type_work in type_works:
    keyboard.add(InlineKeyboardButton(text=f"{type_work.get('name')}", callback_data=f"{type_work.get('id')}"))
  keyboard.adjust(1)
  return keyboard.as_markup()

def planing_subtype_work(plot_id, type_work_id):
  subtype_works = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/planing', param={"plotId": str(plot_id), "typeWorkId": str(type_work_id)})
  keyboard = InlineKeyboardBuilder()
  if subtype_works is None:
    return None
  for subtype_work in subtype_works:
    keyboard.add(InlineKeyboardButton(text=f"{subtype_work.get('name')}", callback_data=f"{subtype_work.get('id')}"))
  keyboard.adjust(1)
  return keyboard.as_markup()


def planing_production_name(plot_id, type_work_id, subtype_work_id):
  plans = create_request(RequestType.GET.name, entity_url["plan"], param={"plotId": int(plot_id), "typeWorkId": int(type_work_id), "subtypeWorkId": int(subtype_work_id)})
  keyboard = InlineKeyboardBuilder()
  flag = False
  for plan in plans:
    if plan.get("productionName") != "":
      flag = True
      break
  if not flag:
    return None
  if plans is None:
    return None
  for plan in plans:
    if plan.get("productionName") == "":
      continue
    keyboard.add(InlineKeyboardButton(text=f"{plan.get('productionName')}", callback_data=f"{plan.get('id')}"))
  keyboard.adjust(1)
  return keyboard.as_markup()








