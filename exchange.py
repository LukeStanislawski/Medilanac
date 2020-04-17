import json
import logging
from flask import Flask, request
from utils.config import Config

app = Flask(__name__)
branches = []


class Exchange():
    """
    Class to initialise and run an exchange server

    display_http: If true, all http requests recieved will be printed in real time
    """
    def __init__(self, display_http=False):
        global app

        if not display_http:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

        app.run(debug=False, 
            host=Config.exchange_ip, 
            port=Config.exchange_port,
            use_reloader=False)



@app.route("/submit-miner", methods=['POST'])
def submit_miner():
    """
    Listens for announcements of existence from miners
    """
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
    """
    Return the list of known miners
    """
    global branches
    # data = json.loads(request.data)
    return json.dumps(branches)


@app.route("/reset", methods=['GET'])
def reset():
    """
    Allows the triggering of the wiping of exchange memory, resetting list of known miners
    """
    global branches
    branches = []
    print("Exchange reset")
    return "SUCCESS"

 
if __name__ == "__main__":
	E = Exchange(display_http=False)