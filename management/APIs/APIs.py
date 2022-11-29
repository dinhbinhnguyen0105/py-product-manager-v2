import requests
import json


URL = "https://script.google.com/macros/s/AKfycbwTQaOFOcowKjBx1fKpbPcpqebLrHa2a8zUmx0XKCJJs2G03iGs3ncNk0v2u1TumAmkng/exec?"

def POST(wsName, action, payload):
    headers = { 'Content-Type': 'application/json' }
    payload = json.dumps(payload)
    if action == 'add':
        url = URL + f'wsname={wsName}&action={action}'
        response = requests.request('POST', url, headers=headers, data=payload)
        return response.text

def GET(wsname, action):
    url = URL + f'wsname={wsname}&action={action}'
    try:
        response = requests.request("GET", url)
        return response.json()
    except TimeoutError as e:
        print(e)
        GET(wsname, action)

def DELETE(id):
    url = URL + f'wsname=products&action=delete&id={id}'
    try:
        response = requests.request('GET', url)
        return response.json()
    except TimeoutError as e:
        print(e)
        DELETE(id)