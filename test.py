import requests

r = requests.post('http://127.0.0.1:8000/api/v1/user/auth', data='{"username":"lurayy","password":"pass"}', headers={'Content-Type':'application/json'})
print(r.json())
token = r.json()['token']
print(token)
send_token = "JWT " + token
r = requests.get('http://127.0.0.1:8000/api/v1/user/csrf')
print(r.json())
csrf = r.json()['x-csrftoken']
headers = {'Content-Type':'application/json', 'Authorization':send_token, "X-Csrftoken":csrf}
r = requests.post('http://127.0.0.1:8000/api/v1/user/current', headers=headers)
print(r.text)