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
                        #print msg
                        if 'message' in msg:
                            if 'text' in msg['message']:
                                print msg['message']['text']
                return "ok"
            except Exception as ex:
                print ex
    return "bad request!", 400

@app.errorhandler(404)
def page_not_found(error):
    return "Page Not Found!", 404

if __name__ == "__main__":
    app.run()