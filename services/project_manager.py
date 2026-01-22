import os
import requests

url = os.getenv("URL") + '/project-manager'

def get_project_managers():
  try:
    response = requests.get(url)
    if response.status_code != 200:
      print(f"Server error: {response.json()}")
      return None
    return response.json()
  except Exception as e:
    print(f"Unexpected error: {e}")
    return None
