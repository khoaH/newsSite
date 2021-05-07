import requests, json, time

url = 'http://127.0.0.1:5000/login'
headers = {'email' : 'bcv@gmail.com', 'password' : '123'}

print('getting token...')
r = requests.get(url, headers=headers)
token = r.json()
print(token)

bearer = 'Bearer ' + token['access_token']
print('Bearer :' + bearer)

print('testing...')
headers_test = {'Authorization' : bearer}
url_test = 'http://127.0.0.1:5000/index'
test_response = requests.get(url_test, headers=headers_test)
print(test_response.json())

print('waiting for token to expire...')
for x in range(5):
    time.sleep(1)
    print(5-x)
# time.sleep(25)
print('done')
test_response_after = requests.get(url_test, headers=headers_test)
print(test_response_after.json())

print('refreshing token')
refresh_url = 'http://127.0.0.1:5000/refresh'
refresh_bearer = 'Bearer ' + token['refresh_token']
print('Refresh bearer: ' + refresh_bearer)
refresh_header = {'Authorization' : refresh_bearer}
refresh_response = requests.post(refresh_url, headers=refresh_header)

refreshed_token = refresh_response.json()
print('Token after refresh:')
print(refreshed_token)

bearer_after_refresh = 'Bearer ' + refreshed_token['access_token']
headers_after_refresh = {'Authorization' : bearer_after_refresh}
refreshed_response = requests.get(url_test, headers=headers_after_refresh)
print('After refresh: ')
print(refreshed_response.json())


