import json
from flask import Flask, request
import config

app = Flask(__name__)
chunks = []


@app.route("/retrieve", methods=['POST'])
def get_blockchain():
    global chunks
    data = json.loads(request.data)
    i = 0
    while i < len(chunks) and chunks[i]["head"]["chain_id"] in data["blacklist"]:
        i += 1

    if i < len(chunks):
        return json.dumps(chunks.pop(i), sort_keys=True)
    else:
        return json.dumps([])


@app.route("/submit", methods=['POST'])
def post_blockchain():
    global chunks
    data = json.loads(request.data)
    chunks.append(data)
    print (request.data)

    return '{"status":"accepted"}'


 
if __name__ == "__main__":
	app.run(debug=True, host=config.exchange_ip, port=config.exchange_port)