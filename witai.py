from wit import Wit
import json

try:
    with open("config.json") as f :
        access_token = json.load(f)['witai']
except:
    print("open config.json error")

def send(request, response):
    print(response['text'])

actions = {
    'send': send,
}

client = Wit(access_token=access_token, actions=actions)
resp = client.message('Turn on the light in my bedroom')
print('Yay, got Wit.ai response: ' + str(resp))