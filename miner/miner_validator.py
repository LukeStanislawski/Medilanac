import json
import urllib3
import random
from miner.miner_log import MinerLog as Log
from utils.validator import validate_headers
from utils.config import Config
from utils import crypt


class MinerValidator():
    def __init__(self):
        self.miner = None
        self.headers = None
        self.http = urllib3.PoolManager()


    def validate(self, miner):
        """
        Attempts to validate a miner
        
        miner: dictionary containing miner info
        """
        Log.debug("Validating miner {}".format(miner["id"]))
        self.miner = miner
        
        Log.debug("Fetching blockchain headers")
        self.fetch_headers()
        Log.debug("Validating blockchain")
        es = validate_headers(self.headers)
        
        if len(es) > 0:
            Log.debug("Blockchain INVALID:{}".format("\n    ".join(es)))
            return False
        else:
            Log.debug("Blockchain VALID")
            

        if len(self.headers) <= 1:
            Log.debug("Blockchain too short to validate, accepting chain as valid")
        else:
            if not self.validate_miner():
                Log.debug("Miner invalid")
                return False
        

        Log.debug("Miner Valid")
        return True


    def fetch_headers(self):
        """
        Fetches the headers of a miners blockchain
        """
        Log.debug("Fetching headers from {}".format(self.miner["address"]))
        self.headers = []
        timeout = Config.retrieve_headers_timout

        while len(self.headers) == 0 and timeout > 0:
            try:
                Log.debug("Posting to {}".format(self.miner["address"] + "/blockchain-headers"))
                self.http = urllib3.PoolManager()
                r = self.http.request('POST', self.miner["address"] + "/blockchain-headers",
                     headers={'Content-Type': 'application/json'},
                     body="{}", timeout=2.0)
                
                Log.debug("Received response: {}".format(r.data))
                self.headers = json.loads(r.data)
                Log.debug("Parsed response JSON")

            except Exception as e:
                Log.warning("Error when retrieving bc headers:")
                Log.warning(str(e))
                timeout = timeout - 1


    def query_miner(self, qhash):
        """
        Queries the miner for a specific file
        
        qhash: the hash of the file to request
        """
        Log.debug("Fetching rfile from miner at {}".format(self.miner["address"]))
        timeout = Config.query_validity_timeout
        payload = {}
        payload["tree_type"] = "FILE"
        payload["hash"] = qhash
        rfile = None

        while rfile is None and timeout > 0:
            try:
                addr = self.miner["address"] + "/validate"
                Log.debug("Posting to {}".format(addr))
                r = self.http.request('POST',
                        addr,
                        headers={'Content-Type': 'application/json'},
                        body=json.dumps(payload), 
                        timeout=2.0)
                
                Log.debug("Received response: {}".format(r.data))
                rfile = json.loads(r.data)
                Log.debug("Parsed response JSON")

            except Exception as e:
                Log.warning("Error when retrieving bc headers:")
                Log.warning(str(e))
                timeout = timeout - 1

        return rfile


    def validate_miner(self):
        """
        Attempts to validate a miner
        """
        Log.debug("Validating miner")

        hashes = []
        for block in self.headers:
            Log.debug("newBlock")
            if "file_merkle" in block["head"]:
                Log.debug("string is in block")
                Log.debug(json.dumps(block["head"], indent=4))
                hashes.extend(block["head"]["file_merkle"][-1])
            else:
                Log.debug("string is not in block")

        qhash = hashes.pop(random.randint(0,len(hashes)-1))
        Log.debug("Query hash selected: {}".format(qhash[:8]))

        rfile = self.query_miner(qhash)
        Log.debug("Hashing rfile")
        rhash = crypt.hash_filedata(rfile)
        Log.debug("rhash: {}".format(rhash))

        if rhash == qhash:
            Log.debug("Miner passed validation")
            return True
        else:
            Log.debug("Miner failed validation")
            return False
