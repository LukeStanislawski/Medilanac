import json
from flask import Flask, request
from utils.config import Config

app = Flask(__name__)
branches = []


@app.route("/submit-miner", methods=['POST'])
def submit_miner():
    # TODO: add validation
    global branches
    data = json.loads(request.data)
    branch = {}
    branch["id"] = data["branch_id"]
    branch["address"] = data["branch_address"]
    branches.append(branch)
    print ("Num miners: {}".format(len(branches)))
    return '{"status":"accepted"}'


@app.route("/get-miners", methods=['POST'])
def get_miners():
    # TODO: add validation
    global branches
    # data = json.loads(request.data)
    return json.dumps(branches)



 
if __name__ == "__main__":
	app.run(debug=True, host=Config.exchange_ip, port=Config.exchange_port)