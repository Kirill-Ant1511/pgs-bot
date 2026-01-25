import pandas as pd

def to_excel(reports, file_name):
  data = []
  for report in reports:
    plan = report.get("plan")
    plot = report.get("plan").get("plot")
    type_work = report.get("plan").get("typeWork")
    subtype_work = report.get("plan").get("subtypeWork")
    data.append({
      "ID": report.get("id"),
      "Участок": plot.get("name"),
      "Вид работ": type_work.get("name"),
      "Тип работ": subtype_work.get("name"),
      "Требуемый объём": plan.get("volume"),
      "Название выработки": plan.get("productionName"),
      "Факт выполненой работы": report.get("fact"),
      "Дельта": report.get("delta"),
      "Дата отправки": report.get("date"),
      "Отправитель": report.get("whoSend"),
      "Станок": report.get("machine"),
      "Комментарии": report.get("comment")
    })
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False, sheet_name="Отчёты")