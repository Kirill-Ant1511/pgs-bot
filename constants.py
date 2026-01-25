from enum import Enum

host = "http://localhost:8080"

entity_url = {
  "project_manager": host + '/project-manager',
  "plot": host + '/plot',
  "report": host + '/report',
  "type_work": host + '/type-work',
  "subtype_work": host + '/subtype-work',
  "plan": host + "/plan",
}

class RequestType(Enum):
  GET = "GET"
  POST = "POST"
  DELETE = "DELETE"
