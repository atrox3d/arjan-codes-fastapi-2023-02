import requests

print(requests.get('http://127.0.0.1:8000').json())
print(requests.get('http://127.0.0.1:8000/items/0').json())
print(requests.get('http://127.0.0.1:8000/items/55').json())
print(requests.get('http://127.0.0.1:8000/items?name=Nails').json())
