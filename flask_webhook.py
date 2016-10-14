
from messengerbot import MessengerClient, messages, attachments, templates, elements
import json

#read messenger/witai token
try:
    with open("config.json") as f :
        configs = json.load(f)
        messenger_token = configs['fb_page_access_token']
        wit_token = configs['witai']
except:
    print("open config.json error")

# Manually initialize Messenger client
messenger = MessengerClient(access_token=messenger_token)

#init wit.ai
from wit import Wit
def send(request, response):
    print(response['text'])

actions = {
    'send': send,
}

wit_client = Wit(access_token=wit_token, actions=actions)

from flask import Flask,request
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello God!"

@app.route("/messenger_hook", methods=['GET', 'POST'])
def messenger_get():
    if request.method == "GET":
        token = request.args.get('hub.verify_token')
        if token != "dahuaxiyou":
            return "illegal token", 400
        challenge = request.args.get('hub.challenge')
        if challenge is None:
            return "bad request", 400
        return request.args.get('hub.challenge')

    elif request.method == "POST":
        if(request.is_json):
            try:
                data = request.get_json()
                #print data
                #print data['entry']
                entries = data['entry']
                for entry in entries:
                    msgs = entry['messaging']
                    for msg in msgs:
                        sender_id = msg['sender']['id']
                        recipient = messages.Recipient(recipient_id=sender_id)
                        #print msg
                        if 'message' in msg:
                            if 'text' in msg['message']:
                                #print msg['message']['text']
                                #send text to witai
                                wit_resp = wit_client.message(msg['message']['text'])
                                print "wit response:" , wit_resp['entities']
                                # Send text message
                                message = messages.Message(text=json.dumps(wit_resp['entities']))
                                messenger_req = messages.MessageRequest(recipient, message)
                                messenger.send(messenger_req)
                return "ok"
            except Exception as ex:
                print ex
                message = messages.Message(text="bad request")
                messenger_req = messages.MessageRequest(recipient, message)
                messenger.send(messenger_req)
    return "bad request!"

@app.errorhandler(404)
def page_not_found(error):
    return "Page Not Found!", 404

if __name__ == "__main__":
    app.run()