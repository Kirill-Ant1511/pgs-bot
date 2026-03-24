from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from constants import RequestType, entity_url
from services.api import create_request

logger = logging.getLogger(__name__)

def planing_plot(user_id, is_production=False):
  plots = create_request(RequestType.GET.name, entity_url["plot"] + '/planing')
  plots.sort(key=lambda x: x.get("name"))
  if plots is None:
    logger.info("Plans absent")
    return None
  user = create_request(RequestType.GET.name, entity_url["project_manager"] + f'/{user_id}')
  if user is None or user.get("plots") == [] or user.get("plots") is None:
    logger.info(f"User {user_id} has no plots")
    return None
  plot_ids = {item['id'] for item in user.get("plots")}
  user_plots = [item for item in plots if item['id'] in plot_ids]
  if user_plots == [] or user_plots is None:
    logger.info(f"User {user_id} has no plots")
    return None
  keyboard = InlineKeyboardBuilder()
  if user_plots is None:
    return None
  for plot in user_plots:
    keyboard.add(InlineKeyboardButton(text=f"{plot.get("name")}", callback_data=f"{plot.get("id")}"))
  keyboard.adjust(1)
  return keyboard.as_markup()

def planing_type_work(plot_id, is_production=False):
  type_works = create_request(RequestType.GET.name, entity_url["type_work"] + '/planing', param={"plotId": str(plot_id)})
  type_works.sort(key=lambda x: x.get("name"))
  keyboard = InlineKeyboardBuilder()
  if type_works is None:
    return None
  for type_work in type_works:
    if not is_production:
      if type_work.get("code") == "BHBUR":
        continue
    keyboard.add(InlineKeyboardButton(text=f"{type_work.get('name')}", callback_data=f"{type_work.get('id')}"))
  if len(list(keyboard.buttons)) == 0:
    return None
  keyboard.adjust(1)
  return keyboard.as_markup()

def planing_subtype_work(plot_id, type_work_id):
  subtype_works = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/planing', param={"plotId": str(plot_id), "typeWorkId": str(type_work_id)})
  subtype_works.sort(key=lambda x: x.get("name"))
  keyboard = InlineKeyboardBuilder()
  if subtype_works is None:
    return None
  for subtype_work in subtype_works:
    keyboard.add(InlineKeyboardButton(text=f"{subtype_work.get('name')}", callback_data=f"{subtype_work.get('id')}"))
  keyboard.adjust(1)
  return keyboard.as_markup()


def planing_production_name(plot_id, type_work_id, subtype_work_id):
  plans = create_request(RequestType.GET.name, entity_url["plan"], param={"plotId": int(plot_id), "typeWorkId": int(type_work_id), "subtypeWorkId": int(subtype_work_id), "isActive": True})
  plans.sort(key=lambda x: x.get("productionName"))
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








