from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

test_router = Router()



@test_router.message(F.text == "test")
async def test(message: Message):
  await message.answer("Test", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Test 1", callback_data="test 1"),
    InlineKeyboardButton(text="Test 2", callback_data="test 2"),
  ]]))

@test_router.callback_query(F.data == "test 1")
async def test(callback: CallbackQuery):
  await callback.answer("test 3")

@test_router.callback_query(F.data == "test 2")
async def test(callback: CallbackQuery):
  await callback.answer("test 4")


@test_router.callback_query(F.data == "test 3")
async def test(callback: CallbackQuery):
  await callback.message.answer("Вызвался тест 1 и из него тест 3")

@test_router.callback_query(F.data == "test 4")
async def test(callback: CallbackQuery):
  await callback.message.answer("Вызвался тест 2 и из него тест 4")