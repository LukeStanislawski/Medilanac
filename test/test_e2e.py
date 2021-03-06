import sys, os, shutil
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import pytest
import json
import time
from utils.config import Config
from utils.crypt import hash_block
from miner.miner import Miner
from multiprocessing import Process
from exchange import Exchange
from reconstruct import reconstruct


def test_e2e():
    """
    Run an end-to-end test of the timulation including branch reconstruction
    """
    initialise()
    end_thresh = 2

    # Start exchange server
    p_ex = Process(target=Exchange)
    p_ex.start()
    print("Giving server time to start up")
    time.sleep(1.5)
    print("Ready or not here I come")

    # Start miner processes
    ps = []
    for i in range(Config.num_miners):
        p = Process(target=Miner, args=[i, 5001 + i, True])
        p.start()
        ps.append(p)

    # Wait for miner processes to finish generating blockchains
    for i, p in enumerate(ps):
        p.join()

    # Stop server
    p_ex.terminate()
    print("Blockchain generation complete")


    # Check each blockchain can be reconstructed
    # from the other blockchains 
    # (excluding the last blocks)
    for chain in os.listdir(Config.blockchain_dir):
        with open(os.path.join(Config.blockchain_dir, chain, "blockchain.json")) as f:
            bc_o = json.loads(f.read())
        
        print("Reconstructing chain on {}".format(chain))
        r_bc = reconstruct(chain, buf=1)

        if end_thresh != 0:
            bc = bc_o[:-1 * end_thresh]
        else:
            bc = bc_o
            
        print([x["head"]["id"] if "head" in x else -1 for x in bc_o])
        assert len(r_bc) >= len(bc), "Chunks for some blocks could not be found (even ignoring the last {} block(s): rbc={}, bc={}".format(end_thresh, [x["head"]["id"] if "head" in x else -1 for x in r_bc], [x["head"]["id"] if "head" in x else -1 for x in bc_o])
        r_bc = r_bc[:len(bc)]
    
        for b, r_b in zip(bc, r_bc):
            hash_b = hash_block(b, attrs=["head", "body"])
            hash_r_b = hash_block(r_b, attrs=["head", "body"])
            assert hash_b == hash_r_b, "Hash of reconstructed block {} on chain {}.. does not match original".format(i, chain)


def initialise():
    """
    Set params of simulation
    """
    Config.num_miners = 5
    Config.num_blocks = 8
    Config.num_foreign_chunks = 7
    Config.ec_k = 3
    Config.ec_m = 5
    Config.blockchain_dir = os.path.abspath(os.path.join(Config.test_data_dir, "blockchain"))
    
    empty_dir()


def empty_dir():
    """
    Removes all files from test blockchain dir
    """
    if not os.path.exists(Config.blockchain_dir):
        os.makedirs(Config.blockchain_dir)
    else:
        folder = Config.blockchain_dir

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    test_e2e()