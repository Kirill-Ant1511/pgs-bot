from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Основные кнопки
send_report_button = [KeyboardButton(text="Отправить отчёт")]
send_production_report_button = [KeyboardButton(text="Отправить отчёт по выработкам")]
cancel_last_action_button = [KeyboardButton(text="Отменить последние действие")]
get_reports_button = [KeyboardButton(text="Выгрузка отчётов")]
# Основаная клавиатура
main_menu = ReplyKeyboardMarkup(keyboard=[send_report_button, send_production_report_button, cancel_last_action_button], resize_keyboard=True)

pm_menu = ReplyKeyboardMarkup(keyboard=[send_report_button, send_production_report_button, get_reports_button, cancel_last_action_button], resize_keyboard=True)



# ДОПОЛНИТЕЛЬНЫЕ КНОПКИ
get_date_today = InlineKeyboardButton(text="Сегодня", callback_data="today")
get_date_yesterday = InlineKeyboardButton(text="Вчера", callback_data="yesterday")
cancel_action = [InlineKeyboardButton(text="Отменить❌", callback_data="cancel")]
confirm_action = [InlineKeyboardButton(text="Подтвердить✅", callback_data="confirm")]
skip_button = [InlineKeyboardButton(text="Пропустить⏭️", callback_data="skip")]

# Кнопки для получения выработок
general_report_button = [InlineKeyboardButton(text="📑Общие отчёты", callback_data="general_report")]
production_report_button = [InlineKeyboardButton(text="📊По выработкам", callback_data="production_report")]
message_report_button = [InlineKeyboardButton(text="💬Сообщение по выработкам", callback_data="message_report")]

# Фильтры для получения отчётности
all_reports = [InlineKeyboardButton(text="📑Всю отчётность", callback_data="all_report")]
by_date = [InlineKeyboardButton(text="📆По дате", callback_data="by_date")]
by_plot = [InlineKeyboardButton(text="📍По участку", callback_data="by_plot")]
by_plan = [InlineKeyboardButton(text="👷🏻По виду работ", callback_data="by_plan")]
by_plan_and_date = [InlineKeyboardButton(text="👷🏻+📆По выду работ и дате", callback_data="by_plan_and_date")]
by_plot_and_date = [InlineKeyboardButton(text="📍+📆По участку и дате", callback_data="by_plot_and_date")]




# Дополнительные клавиатуры
date_kb = InlineKeyboardMarkup(inline_keyboard=[[get_date_today, get_date_yesterday]])
confirm_kb = InlineKeyboardMarkup(inline_keyboard=[cancel_action, confirm_action])
skip_kb = InlineKeyboardMarkup(inline_keyboard=[skip_button])
get_report_kb = InlineKeyboardMarkup(inline_keyboard=[general_report_button, production_report_button, message_report_button])
filter_get_report_kb = InlineKeyboardMarkup(inline_keyboard=[all_reports, by_date, by_plot, by_plan, by_plan_and_date, by_plot_and_date])