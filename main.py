import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

from app.confirm_handler import confirm_router
from app.get_date_handler import get_date_router
from app.get_report_handler import get_report_router
from app.get_report_message import get_report_message_router
from app.keyboards import main_menu, pm_menu
from app.send_report_handler import send_report_router
from app.skip_handler import skip_router
from constants import RequestType, entity_url
from services.api import create_request

load_dotenv()

session = AiohttpSession(proxy="socks5://pgs_user:pgs_pass@185.192.23.116:1080")
bot = Bot(os.getenv("BOT_TOKEN"), session=session)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
  project_managers = create_request(RequestType.GET.value, entity_url["project_manager"] + f"/{message.chat.id}")
  print(project_managers)
  if project_managers is None:
    await message.answer("Здравствуйте! Вы не зарегестрированы, попросите вас зарегестрировать перед использованием бота")
  elif project_managers.get("role") == 'USER':
    await message.answer(f"Здравствуйте, {project_managers.get("name")}!", reply_markup=main_menu)
  elif project_managers.get("role") == 'PM':
    await message.answer(f"Здравствуйте, {project_managers.get("name")}!", reply_markup=pm_menu)

@dp.message(F.text == "Отменить последние действие")
async def cancel_last_action(message: Message, state: FSMContext):
  await state.clear()
  await message.answer("Действие отменено")


async def main():
  dp.include_routers(send_report_router, skip_router, get_date_router, confirm_router, get_report_router, get_report_message_router)
  await dp.start_polling(bot)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
  asyncio.run(main())