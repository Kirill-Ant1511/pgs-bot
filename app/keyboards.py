from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


send_report_button = [KeyboardButton(text="Отправить отчёт")]
send_production_report_button = [KeyboardButton(text="Отправить отчёт по выработкам")]
cancel_last_action_button = [KeyboardButton(text="Отменить последние действие")]
get_reports_button = [KeyboardButton(text="Выгрузка отчётов")]
# Основаная клавиатура
main_menu = ReplyKeyboardMarkup(keyboard=[send_report_button, send_production_report_button, cancel_last_action_button])

pm_menu = ReplyKeyboardMarkup(keyboard=[send_report_button, send_production_report_button, get_reports_button, cancel_last_action_button])