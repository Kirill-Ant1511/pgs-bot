import requests

def create_request(request_type, path, param = None, body = None):
  try:
    if request_type == "GET":
      response = requests.get(path, params=param)
    elif request_type == "POST":
      response = requests.post(path, json=body)
    elif request_type == "DELETE":
      response = requests.delete(path)
    else:
      return None
    if response.status_code != 200:
      print(f"Server error: {response.json()}. Status: {response.status_code}")
      return None
    if request_type != "DELETE":
      return response.json()
    return "deleted"

  except Exception as e:
    print(f"Unexpected error: {e}")
    return None