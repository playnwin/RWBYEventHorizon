import requests, pprint
from imgurpython import ImgurClient
from tokens import imgur_client_key, imgur_client_secret

client_id = imgur_client_key
client_secret = imgur_client_secret
pin = '57f7841a94'

client = ImgurClient(client_id, client_secret)

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')
print(authorization_url)
pin = input('What was the pin? ')
params = {"client_id": client_id,
          "client_secret": client_secret,
          "grant_type": "pin",
          "pin": pin}

url = r"https://api.imgur.com/oauth2/token/"

# make sure the data is sent with the POST request, along with disabling the
# SSL verification, potential security warning

r = requests.post(url, data=params)
j = r.json()
print("The exchangePinForTokens API response:", pprint.pprint(j))

# add the access_token to the headers as
# Authorization: Bearer YOUR_ACCESS_TOKEN
access_token = j['access_token']
refresh_token = j['refresh_token']
print('Access token: ', access_token)
print('Refresh token: ', refresh_token)