import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'

url = "http://127.0.0.1:5000"
r = requests.get(url)
print r.status_code
print r.json()


r = requests.get("http://127.0.0.1:5000/todo/api/v1.0/tasks")
print r.status_code
print r.json()


r = requests.post(url="http://127.0.0.1:5000/todo/api/v1.0/tasks", json={"title": "Read a book"})
print r.status_code
print r.json()