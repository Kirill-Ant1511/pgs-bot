from constants import RequestType, entity_url
from services.api import create_request
from datetime import datetime


def get_unique_machine(reports):
  machine = dict()
  machine_and_production = dict()
  for report in reports:
    if report.get("machine") is None:
      continue
    machine[report.get("machine")] = []
    machine_and_production[f"{report.get("machine")} - {report.get("plan").get("productionName")}"] = []

  for report in reports:
    if report.get("machine") is None:
      continue
    machine[report.get("machine")].append(report)
    machine_and_production[f"{report.get("machine")} - {report.get("plan").get("productionName")}"].append(report)
  return machine, machine_and_production


def get_last_drilling(reports):
  result = 0
  now = datetime.now()
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.date() == now.date():
      result += report.get("fact")
  return result

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
  now = datetime.now()
  message = f"{now.date()}\n\n"
  type_work = create_request(RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
    "name": "Горно-буровые работы"
  })
  reports = create_request(RequestType.GET.name, entity_url["report"], param={
    "plotId": plot_id,
    "typeWorkId": type_work.get("id"),
  })
  machine, machine_and_production = get_unique_machine(reports)
  for key, value in machine.items():
    message += f"Буровая {key}\n"
    message += f"За сутки: {get_last_drilling(value)} м.\n"
    message += f"За месяц: {get_last_month_drilling(value)} м.\n"
    message += f"С начала проекта: {get_all_drilling(value)} м.\n\n"

  for key, value in machine_and_production.items():
    last_drill = get_last_drilling(value)
    if last_drill == 0:
      continue
    message += f"Буровая: {key} - ({value[0].get("plan").get("plot").get("name")}. Проектная глубина: {value[0].get("plan").get("volume")}м)\n"
    message += f"За сутки: {last_drill} м.\n"
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
    })
    message += f"Пробопод керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports)} м."
  return message







