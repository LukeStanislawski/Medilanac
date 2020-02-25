import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from miner.miner import Miner
from utils.validator import validate_headders

def test_blochain_heads():
	print("starting..")
	m = Miner(0, 0, test=True)
	print("init miners")
	m.blockchain.append(m.gen_genesis())
	m.blockchain.append(m.gen_new_block())
	r = validate_headders(m.blockchain)
	print(r)
	assert r == True, "test failed"


test_blochain_heads()
