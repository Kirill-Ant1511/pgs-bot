from aiogram import Router, F
from aiogram.types import Message

send_report_router = Router()


@send_report_router.message(F.text == "Отправить отчёт")
async def send_report(message: Message):
    await message.answer("Отправка отчёта")

