from constants import RequestType, entity_url
from services.api import create_request
from datetime import datetime, timedelta


def get_unique_machine(reports):
  machine = dict()
  for report in reports:
    if report.get("machine") is None:
      continue
    machine[report.get("machine")] = []

  for report in reports:
    if report.get("machine") is None:
      continue
    machine[report.get("machine")].append(report)

  return machine


def get_last_drilling(reports):
  result = 0
  now = datetime.now() - timedelta(days=1)
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.date() == now.date():
      result += report.get("fact")
  return result


def all_drilling_by_production(reports, production_name):
  result = 0
  for report in reports:
    if report.get("plan").get("productionName") == production_name:
      result += report.get("fact")
  return result


def get_last_drilling_for_machine(reports):
  result = 0
  result_report_plan = None
  now = datetime.now() - timedelta(days=1)
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.date() == now.date():
      result += report.get("fact")
      result_report_plan = report.get("plan")
  return result, result_report_plan

def get_last_month_drilling(reports):
  result = 0
  now = datetime.now()
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.month == now.month:
      result += report.get("fact")
  return result

def get_all_drilling(reports):
  return sum([report.get("fact") for report in reports])

def get_production_message(plot_id):
  now = datetime.now() - timedelta(days=1)
  message = f"{now.date()}\n\n"
  type_work = create_request(RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
    "name": "Горно-буровые работы",
  })
  reports = create_request(RequestType.GET.name, entity_url["report"], param={
    "plotId": plot_id,
    "typeWorkId": type_work.get("id"),
    "endDate": now.strftime("%Y-%m-%d"),
  })
  machine = get_unique_machine(reports)
  for key, value in machine.items():
    last_drill, last_drill_plan = get_last_drilling_for_machine(value)
    if last_drill != 0:
      all_drilling_production = all_drilling_by_production(value, last_drill_plan.get("productionName"))
      message += f"Буровая: {key}. Бурение {last_drill_plan.get("productionName")} - ({last_drill_plan.get("plot").get("name")}. Проектная глубина: {last_drill_plan.get("volume")} м, факт - {all_drilling_production} м)\n"
    else:
      message += f"Буровая {key}\n"
    message += f"За сутки: {get_last_drilling(value)} м.\n"
    message += f"За месяц: {get_last_month_drilling(value)} м.\n"
    message += f"С начала проекта: {get_all_drilling(value)} м.\n\n"

  message += "Всего:\n"
  message += f"За сутки: {get_last_drilling(reports)} м.\n"
  message += f"За месяц: {get_last_month_drilling(reports)} м.\n"
  message += f"С начала проекта: {get_all_drilling(reports)} м.\n\n"

  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Документация керна скважин"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": now.strftime("%Y-%m-%d")
    })

    message += f"Документация керна:\n"
    message  += f"За сутки: {get_last_drilling(reports)} м.\n"
    message += f"За месяц: {get_last_month_drilling(reports)} м.\n"
    message += f"С начала проекта: {get_all_drilling(reports)} м.\n\n"

  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
      "name": "Распиловка керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
        "plotId": plot_id,
        "subtypeWorkId": subtype_work.get("id"),
        "endDate": now.strftime("%Y-%m-%d")
    })
    message += f"Распиловка керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports)} м.\n"

  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Отбор керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": now.strftime("%Y-%m-%d")
    })
    message += f"Отбор керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports)} м.\n"

  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Пробоподготовка керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": now.strftime("%Y-%m-%d")
    })
    message += f"Пробопод керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports)} м."
  return message







