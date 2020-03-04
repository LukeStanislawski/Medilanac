import os
import json
import logging
import random
from flask import Flask, request
from utils.config import Config
from miner.miner_log import MinerLog as Log


chain_id = None
miner_id = None
app = Flask(__name__)


class Server():
    def __init__(self, m_id, c_id, port, m_dir):
        self.m_id = m_id
        self.c_id = c_id
        self.port = port
        self.m_dir = m_dir

        # log.set_up(self.m_id, self.m_dir)

        global chain_id
        global miner_id
        chain_id = self.c_id
        miner_id = self.m_id

        if not Config.display_http:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
        
        self.run()

    def run(self):
        global app
        
        app.run(debug=False, 
            host=Config.miner_server_ip, 
            port=self.port,
            use_reloader=False)



def load_blockchain(die=8):
    fpath = os.path.join(Config.blockchain_dir, chain_id[:8], "blockchain.json")
    blockchain = []

    try:
        with open(fpath) as f:
            blockchain = f.read()
        blockchain = json.loads(blockchain)
    except Exception as e:
        if die > 0:
            return load_blockchain(die=die-1)
        else:
            print("Time to die depleted")
    
    return blockchain



def load_chunk(die=8):
    global plock
    fpath = os.path.join(Config.blockchain_dir, chain_id[:8], "chunks.json")
    chunk = {}

    try:
        with open(fpath) as f:
            chunks = json.loads(f.read())

        if len(chunks) > 0:
            chunk = chunks.pop(random.randint(0, len(chunks)))

        with open(fpath, "w") as f:
            f.write(json.dumps(chunks, indent=4))

    except Exception as e:
        if die > 0:
            return load_chunk(die=die-1)
        else:
            print("Time to die depleted")


    return chunk


@app.route("/block", methods=['POST'])
def get_blockchain():
    global chain_id
    data = json.loads(request.data)
    blockchain = load_blockchain()
    return blockchain[int(data["block_id"])]


@app.route("/blockchain-headders", methods=['POST'])
def get_blockchain_headders():
    global chain_id
    # data = json.loads(request.data)
    blockchain = load_blockchain()
    bc = []
    for b in blockchain:
        nb = {}
        nb["head"] = b["head"]
        bc.append(nb)
    return json.dumps(bc)


@app.route("/get-chunk", methods=['POST'])
def get_chunks():
    global chain_id
    # data = json.loads(request.data)
    chunk = load_chunk()

    if chunk is None:
        return '{"status": "fail"}'
    else:
        return json.dumps(chunk)

    
