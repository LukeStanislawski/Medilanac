import json
from flask import Flask, request
import config

app = Flask(__name__)
blocks = []


@app.route("/retieve", methods=['POST'])
def get_blockchain():
    global blocks
    data = json.loads(request.data)
    return json.dumps(blocks.pop(0))


@app.route("/submit", methods=['POST'])
def post_blockchain():
    global blocks
    submitted_blocks = json.loads(request.data)
    # blocks.extend(submitted_blocks)
    print (json.dumps(submitted_blocks))
    print(len(json.dumps(submitted_blocks)))
    return '{"status":"accepted"}'


 
if __name__ == "__main__":
	app.run(debug=True, host=config.exchange_ip, port=config.exchange_port)