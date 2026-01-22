import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()


bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()



async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
  asyncio.run(main())