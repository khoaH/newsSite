import requests

url = 'https://firebasestorage.googleapis.com/v0/b/imgapi-144fe.appspot.com/o/img%2F1.jpg?alt=media&token=cdecafe8-9db0-4b02-8ecc-55cf40a96fb7'
r = requests.get(url)
open('test_img_response.jpg', 'wb').write(r.content)