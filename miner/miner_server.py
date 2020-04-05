import os
import json
import logging
import random
from flask import Flask, request
from utils.config import Config
from miner.miner_server_log import MinerServerLog as Log
from json.decoder import JSONDecodeError
import threading
from threading import Lock



chain_id = None
miner_id = None
app = Flask(__name__)
plock = None
tlock = Lock()


class Server():
    def __init__(self, m_id, c_id, port, m_dir, lock):
        self.m_id = m_id
        self.c_id = c_id
        self.port = port
        self.m_dir = m_dir
        global plock
        plock = lock

        # log.set_up(self.m_id, self.m_dir)

        global chain_id
        global miner_id
        chain_id = self.c_id
        miner_id = self.m_id
        chain_dir = os.path.join(Config.blockchain_dir, chain_id[:8])
        Log.set_up(miner_id, chain_dir)

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



def load_blockchain(ttl=5):
    Log.debug("Loading blockchain")
    global plock
    fpath = os.path.join(Config.blockchain_dir, chain_id[:8], "blockchain.json")
    blockchain = []

    Log.debug("Acquiring tlock")
    with tlock:
        Log.debug("tlock acquired")
        Log.debug("Acquiring plock")
        plock.acquire()
        Log.debug("plock acquired")
        try:
            with open(fpath) as f:
                blockchain = f.read()
            blockchain = json.loads(blockchain)
            Log.debug("Loaded and parsed blockchain from file")
        except JSONDecodeError as e:
            Log.debug("FAILED: Blockchain failed to load")

        plock.release()
        Log.debug("Plock released")
    Log.debug("tlock released")

    if len(blockchain) == 0:
        if ttl > 0:
            blockchain = load_blockchain(ttl=ttl-1)
        else:
            Log.Debug("TTL expired, returning empty blockchain")

    return blockchain



def load_chunk(ttl=5):
    Log.debug("Loading chunk")
    global plock
    fpath = os.path.join(Config.blockchain_dir, chain_id[:8], "chunks.json")
    chunk = {}
    chunks = []

    Log.debug("Acquiring tlock")
    with tlock:
        Log.debug("tlock acquired")

        Log.debug("Acquiring plock")
        plock.acquire()
        Log.debug("pLock acquired")
        try:
            with open(fpath) as f:
                chunks = json.loads(f.read())
            Log.debug("Loaded and parsed chunks from file")
        except JSONDecodeError as e:
            Log.debug("Failed to load and/or parse data from file")

        
        Log.debug("Chunks loaded: {}".format(len(chunks)))
        if len(chunks) > 0:
            chunk = chunks.pop(random.randint(0, len(chunks) - 1))
            Log.debug("Chunk popped, {} chhunks remaining".format(len(chunks)))

            with open(fpath, "w") as f:
                f.write(json.dumps(chunks, indent=4))
            Log.debug("Remaining chunks written to file")

        Log.debug("Releasing pLock")
        plock.release()
        Log.debug("pLock released")
    Log.debug("tlock released")


    if chunk == {}:
        if ttl > 0:
            return load_chunk(ttl=ttl-1)
        else:
            Log.debug("TTL expired, returning empty chunk")

    return chunk


def get_tids():
    return [x.ident for x in threading.enumerate()]


@app.route("/block", methods=['POST'])
def get_blockchain():
    Log.debug("Recieved request: /block, threads: {}".format(get_tids()))
    global chain_id
    data = json.loads(request.data)
    log.debug("Parsed json request data")
    blockchain = load_blockchain()
    Log.debug("Returning data, threads: {}".format(get_tids()))
    return blockchain[int(data["block_id"])]


@app.route("/blockchain-headers", methods=['POST'])
def get_blockchain_headers():
    Log.debug("Recieved request: /blockchain-headers, threads: {}".format(get_tids()))
    global chain_id
    # data = json.loads(request.data)
    blockchain = load_blockchain()
    bc = []
    for b in blockchain:
        nb = {}
        nb["head"] = b["head"]
        bc.append(nb)
    Log.debug("Returning data, threads: {}".format(get_tids()))
    return json.dumps(bc)


@app.route("/get-chunk", methods=['GET'])
def get_chunks():
    Log.debug("Recieved request: /get-chunk, threads: {}".format(get_tids()))
    global chain_id
    # data = json.loads(request.data)
    chunk = load_chunk()

    if chunk is None:
        Log.debug("Returning data: Failed, threads: {}".format(get_tids()))
        return '{"status": "fail"}'
    else:
        Log.debug("Returning data: Succeeded, threads: {}".format(get_tids()))
        return json.dumps(chunk)

    
