import os
import json
from flask import Flask, request
from utils import config


chain_id = None
miner_id = None
app = Flask(__name__)


class Server():
    def __init__(self, m_id, c_id, port):
        self.m_id = m_id
        self.c_id = c_id
        self.port = port
        
        global chain_id
        global miner_id
        chain_id = self.c_id
        miner_id = self.m_id
        
        self.run()

    def run(self):
        global app
        
        app.run(debug=False, host=config.miner_server_ip, port=self.port)



def load_blockchain():
    fpath = os.path.join(config.blockchain_dir, chain_id[:8], "blockchain.json")
    with open(fpath) as f:
        blockchain = f.read()
    return json.loads(blockchain)


def load_chunk():
    fpath = os.path.join(config.blockchain_dir, chain_id[:8], "chunks.json")
    with open(fpath) as f:
        chunks = json.loads(f.read())

    if len(chunks) == 0:
        return None

    chunk = chunks.pop(0)
    with open(fpath, "w") as f:
        f.write(json.dumps(chunks, indent=4))

    return chunk


@app.route("/block", methods=['POST'])
def get_blockchain():
    global chain_id
    data = json.loads(request.data)
    blockchain = load_blockchain()
    return blockchain[int(data["block_id"])]


@app.route("/get-chunk", methods=['POST'])
def get_chunk():
    global chain_id
    # data = json.loads(request.data)
    chunk = load_chunk()

    if chunk is None:
        return '{"status": "fail"}'
    else:
        return json.dumps(chunk)

    