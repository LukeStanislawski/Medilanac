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
from utils.crypt import hash_filedata



chain_id = None
miner_id = None
app = Flask(__name__)
plock = None
tlock = Lock()


class Server():
    def __init__(self, m_id, c_id, port, m_dir, lock):
        """
        m_id: Miner ID
        c_id: Miner chain ID
        prot: Port for the server to run on
        m_dir: Path to miner directory
        lock: The process lock used for parallellism with miner main process
        """
        self.m_id = m_id
        self.c_id = c_id
        self.port = port
        self.m_dir = m_dir
        global plock
        plock = lock

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
        """
        Starts the miner server
        """
        global app
        
        app.run(debug=False, 
            host=Config.miner_server_ip, 
            port=self.port,
            use_reloader=False)



def load_blockchain(ttl=8):
    """
    Loads the current blockchain from file

    ttl: time to live (attempts to try and read blockchain before failing)
    """
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
            Log.debug("TTL expired, returning empty blockchain")

    return blockchain



def load_chunk(ttl=8):
    """
    Loadd and pops a chunk from file and writes back remaining list
    
    ttl: time to live (attempts to try and read chunks before failing)
    """
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
    """
    Returns a list of thread ids
    """
    return [x.ident for x in threading.enumerate()]


@app.route("/block", methods=['POST'])
def get_blockchain():
    """
    Triggered when a miner requests a specific block from chain
    """
    Log.debug("Received request: /block, threads: {}".format(get_tids()))
    global chain_id
    data = json.loads(request.data)
    log.debug("Parsed json request data")
    blockchain = load_blockchain()
    Log.debug("Returning data, threads: {}".format(get_tids()))
    return blockchain[int(data["block_id"])]


@app.route("/blockchain-headers", methods=['POST'])
def get_blockchain_headers():
    """
    Triggered when a miner requests blockchain headers
    """
    Log.debug("Received request: /blockchain-headers, threads: {}".format(get_tids()))
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
    """
    Triggered when a miner requests a chunk
    """
    Log.debug("Received request: /get-chunk, threads: {}".format(get_tids()))
    global chain_id
    # data = json.loads(request.data)
    chunk = load_chunk()

    if chunk is None:
        Log.debug("Returning data: Failed, threads: {}".format(get_tids()))
        return '{"status": "fail"}'
    else:
        Log.debug("Returning data: Succeeded, threads: {}".format(get_tids()))
        return json.dumps(chunk)

    
@app.route("/validate", methods=['POST'])
def validate():
    """
    Triggered when a miner requests a specific file for validation
    """
    Log.debug("Received request: /validate, threads: {}".format(get_tids()))
    global chain_id
    Log.debug(request.data)
    data = json.loads(request.data)
    blockchain = load_blockchain()

    if data["tree_type"] == "FILE":
        for block in blockchain:
            if type(block["body"]) is list:
                for d in block["body"]:
                    if hash_filedata(d) == data["hash"]:
                        Log.debug("Found file with hash {}, threads: {}".format(data["hash"][:8], get_tids()))
                        return json.dumps(d, sort_keys=True)


    Log.debug("Could not find file with hash {}, threads: {}".format(data["hash"][:8], get_tids()))
    return "ERROR"
