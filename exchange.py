import json
import logging
from flask import Flask, request
from utils.config import Config

app = Flask(__name__)
branches = []


class Exchange():
    def __init__(self, display_http=False):
        global app

        if not display_http:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

        app.run(debug=True, 
            host=Config.exchange_ip, 
            port=Config.exchange_port,
            use_reloader=False)



@app.route("/submit-miner", methods=['POST'])
def submit_miner():
    # TODO: add validation
    global branches
    data = json.loads(request.data)
    branch = {}
    branch["id"] = data["branch_id"]
    branch["address"] = data["branch_address"]
    branches.append(branch)
    print ("Exchange: Num miners: {}".format(len(branches)))
    return '{"status":"accepted"}'


@app.route("/get-miners", methods=['POST'])
def get_miners():
    # TODO: add validation
    global branches
    # data = json.loads(request.data)
    return json.dumps(branches)

 
if __name__ == "__main__":
	E = Exchange(display_http=False)