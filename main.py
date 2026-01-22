import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from app.keyboards import main_menu
from services.project_manager import get_project_managers

load_dotenv()


bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
  project_managers = get_project_managers()
  if project_managers == None:
    await message.answer("Здравствуйте!", reply_markup=main_menu)
  elif:


async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
  asyncio.run(main())