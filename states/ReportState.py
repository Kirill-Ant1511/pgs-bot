from aiogram.fsm.state import StatesGroup, State


class ReportState(StatesGroup):
  plot = State()
  type_work = State()
  subtype_work = State()
  production_name = State()
  fact = State()
  comment = State()
  date = State()
  machine = State()

class GetReportState(StatesGroup):
  report_type = State()
  filters = State()
  start_date = State()
  end_date = State()
  plot = State()
  type_work = State()
  subtype_work = State()