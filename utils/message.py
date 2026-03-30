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

def get_current_date_comment(reports, current_date: datetime):
  if not reports:
    return None
  reports.sort(key=lambda x: x.get("date"))
  current_drill = reports[-1]
  current_drill_date = datetime.strptime(current_drill.get("date"), "%Y-%m-%d")
  if reports != [] and current_drill.get("comment") is not None and current_drill_date.date() == current_date.date():
    return f"Комментарий: {reports[-1].get("comment")}\n\n"
  else:
    return None

def get_current_date_comment_and_prod_name(reports, current_date: datetime, production_name):
  if not reports:
    return None
  reports.sort(key=lambda x: x.get("date"))
  current_drill = reports[-1]
  current_drill_date = datetime.strptime(current_drill.get("date"), "%Y-%m-%d")
  for report in reports:
    drill_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if drill_date.date() == current_date.date() and report.get("plan").get("productionName") == production_name:
      return f"Комментарий: {report.get("comment")}\n\n"
  return None

def get_last_drilling(reports, current_date: datetime):
  result = 0
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.date() == current_date.date():
      result += report.get("fact")
  return result


def all_drilling_by_production(reports, production_name):
  result = 0
  for report in reports:
    if report.get("plan").get("productionName") == production_name:
      result += report.get("fact")
  return result


def get_last_drilling_for_machine(reports, current_date: datetime):
  result = 0
  result_report_plan = []
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.date() == current_date.date():
      result += report.get("fact")
      result_report_plan.append(report.get("plan"))
  return result, result_report_plan

def get_last_month_drilling(reports, current_date: datetime):
  result = 0
  for report in reports:
    report_date = datetime.strptime(report.get("date"), "%Y-%m-%d")
    if report_date.month == current_date.month:
      result += report.get("fact")
  return result

def get_all_drilling(reports):
  return sum([report.get("fact") for report in reports])

def get_production_message(plot_id, current_date: datetime):
  # current_date = datetime(2026, 3, 25) # это удалить
  message = f"{current_date.date()}\n\n"
  type_work = create_request(RequestType.GET.name, entity_url["type_work"] + '/by-name', param={
    "name": "Горно-буровые работы",
  })
  reports = create_request(RequestType.GET.name, entity_url["report"], param={
    "plotId": plot_id,
    "typeWorkId": type_work.get("id"),
    "endDate": current_date.strftime("%Y-%m-%d"),
  })
  machine = get_unique_machine(reports)
  for key, value in machine.items():
    last_drill, last_drill_plan = get_last_drilling_for_machine(value, current_date)
    for drill in last_drill_plan:
      if last_drill != 0:
        all_drilling_production = all_drilling_by_production(value, drill.get("productionName"))
        message += f"Буровая: {key}. Бурение {drill.get("productionName")} - ({drill.get("plot").get("name")}. Проектная глубина: {drill.get("volume"):.2f} м, факт - {all_drilling_production:.2f} м)\n"
      else:
        message += f"Буровая {key}\n"
      message += f"За сутки: {get_last_drilling(value, current_date):.2f} м.\n"
      message += f"За месяц: {get_last_month_drilling(value, current_date):.2f} м.\n"
      message += f"С начала проекта: {get_all_drilling(value):.2f} м.\n"
      comment = get_current_date_comment_and_prod_name(reports, current_date, drill.get("productionName"))
      if comment is None:
        message += "\n"
      else:
        message += comment

  message += "Всего:\n"
  message += f"За сутки: {get_last_drilling(reports, current_date):.2f} м.\n"
  message += f"За месяц: {get_last_month_drilling(reports, current_date):.2f} м.\n"
  message += f"С начала проекта: {get_all_drilling(reports):.2f} м.\n\n"

  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Документация керна скважин"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": current_date.strftime("%Y-%m-%d")
    })
    reports.sort(key=lambda x: x.get("date"))
    message += f"Документация керна:\n"
    message  += f"За сутки: {get_last_drilling(reports, current_date):.2f} {subtype_work.get("unitMetering")}\n"
    message += f"За месяц: {get_last_month_drilling(reports, current_date):.2f} {subtype_work.get("unitMetering")}\n"
    message += f"С начала проекта: {get_all_drilling(reports):.2f} {subtype_work.get("unitMetering")}\n"
    comment = get_current_date_comment(reports, current_date)
    if comment is None:
      message += "\n"
    else:
      message += comment
  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
      "name": "Распиловка керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
        "plotId": plot_id,
        "subtypeWorkId": subtype_work.get("id"),
        "endDate": current_date.strftime("%Y-%m-%d")
    })
    reports.sort(key=lambda x: x.get("date"))
    message += f"Распиловка керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports):.2f} {subtype_work.get("unitMetering")}\n"
    comment = get_current_date_comment(reports, current_date)
    if comment is not None:
      message += comment
    else:
      message += "\n"
  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Отбор керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": current_date.strftime("%Y-%m-%d")
    })
    reports.sort(key=lambda x: x.get("date"))
    message += f"Отбор керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports):.2f} {subtype_work.get("unitMetering")}\n"
    comment = get_current_date_comment(reports, current_date)
    if comment is not None:
      message += comment
    else:
      message += "\n"
  subtype_work = create_request(RequestType.GET.name, entity_url["subtype_work"] + '/by-name', param={
    "name": "Пробоподготовка керновых проб"
  })
  if subtype_work is not None:
    reports = create_request(RequestType.GET.name, entity_url["report"], param={
      "plotId": plot_id,
      "subtypeWorkId": subtype_work.get("id"),
      "endDate": current_date.strftime("%Y-%m-%d")
    })
    reports.sort(key=lambda x: x.get("date"))
    message += f"Пробоподготовка керновых проб:\n"
    message += f"С начала проекта: {get_all_drilling(reports):.2f} {subtype_work.get("unitMetering")}\n"
    comment = get_current_date_comment(reports, current_date)
    if comment is not None:
      message += comment
  return message







